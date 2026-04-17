from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from telegram.ext import CallbackContext

from backend import database as db

if TYPE_CHECKING:
    from telegram.ext import Application

logger = logging.getLogger(__name__)

RECOVERY_INTERVAL = 60


def _format_time(row: dict) -> str:
    local = row.get("remind_at_local", "")
    if local:
        try:
            dt = datetime.fromisoformat(local)
            return dt.strftime("%d/%m/%Y %H:%M")
        except ValueError:
            return local
    try:
        dt = datetime.fromisoformat(row["remind_at"])
        return dt.strftime("%d/%m/%Y %H:%M UTC")
    except ValueError:
        return row["remind_at"]


def _format_reminder(row: dict) -> str:
    lines = [
        f"🔔 <b>{row['title']}</b>",
    ]
    if row.get("description"):
        lines.append(f"\n{row['description']}")
    lines.append(f"\n⏰ {_format_time(row)}")
    return "\n".join(lines)


async def _send_reminder(context: CallbackContext) -> None:
    """JobQueue callback — отправляет одно напоминание."""
    data = context.job.data
    reminder_id = data["id"]
    user_id = data["user_id"]

    try:
        await context.bot.send_message(
            chat_id=user_id,
            text=_format_reminder(data),
            parse_mode="HTML",
        )
        await db.mark_sent(reminder_id)
        logger.info("Sent reminder %d to user %d", reminder_id, user_id)
    except Exception:
        logger.exception("Failed to send reminder %d", reminder_id)


async def _recover_unsent(context: CallbackContext) -> None:
    """Периодическая проверка — подбирает пропущенные напоминания (после рестарта)."""
    due = await db.get_due_reminders()
    for reminder in due:
        job_name = f"reminder_{reminder['id']}"
        existing = context.job_queue.get_jobs_by_name(job_name)
        if existing:
            continue
        context.job_queue.run_once(
            _send_reminder,
            when=0,
            data=reminder,
            name=job_name,
        )
        logger.info("Recovered missed reminder %d", reminder["id"])


def schedule_reminder(app: Application, reminder: dict) -> None:
    """Ставит напоминание в JobQueue на точное время."""
    remind_at = datetime.fromisoformat(reminder["remind_at"])
    if remind_at.tzinfo is None:
        remind_at = remind_at.replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)
    delay = max((remind_at - now).total_seconds(), 0)

    job_name = f"reminder_{reminder['id']}"
    existing = app.job_queue.get_jobs_by_name(job_name)
    for job in existing:
        job.schedule_removal()

    app.job_queue.run_once(
        _send_reminder,
        when=delay,
        data=reminder,
        name=job_name,
    )
    logger.info("Scheduled reminder %d in %.0fs", reminder["id"], delay)


def setup_scheduler(app: Application) -> None:
    """Запускает периодическую проверку пропущенных напоминаний."""
    app.job_queue.run_repeating(
        _recover_unsent,
        interval=RECOVERY_INTERVAL,
        first=0,
        name="recover_unsent",
    )
    logger.info("Recovery scheduler started (interval=%ds)", RECOVERY_INTERVAL)
