from __future__ import annotations

import aiosqlite
from datetime import datetime, timezone
from typing import List

from backend.config import DB_PATH

_SCHEMA = """
CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    remind_at TEXT NOT NULL,
    remind_at_local TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    is_sent INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_reminders_user ON reminders(user_id);
CREATE INDEX IF NOT EXISTS idx_reminders_due ON reminders(is_sent, remind_at);
"""

_MIGRATIONS = [
    "ALTER TABLE reminders ADD COLUMN remind_at_local TEXT NOT NULL DEFAULT '';",
]


async def get_db() -> aiosqlite.Connection:
    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row
    return db


async def init_db() -> None:
    db = await get_db()
    try:
        await db.executescript(_SCHEMA)
        for migration in _MIGRATIONS:
            try:
                await db.execute(migration)
            except Exception:
                pass
        await db.commit()
    finally:
        await db.close()


async def create_reminder(
    user_id: int, title: str, description: str, remind_at: datetime,
    remind_at_local: str = "",
) -> dict:
    db = await get_db()
    try:
        remind_at_str = remind_at.astimezone(timezone.utc).isoformat()
        created_at_str = datetime.now(timezone.utc).isoformat()
        cursor = await db.execute(
            "INSERT INTO reminders (user_id, title, description, remind_at, remind_at_local, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, title, description, remind_at_str, remind_at_local, created_at_str),
        )
        await db.commit()
        row = await (
            await db.execute("SELECT * FROM reminders WHERE id = ?", (cursor.lastrowid,))
        ).fetchone()
        return dict(row)
    finally:
        await db.close()


async def get_reminders(user_id: int) -> List[dict]:
    db = await get_db()
    try:
        rows = await (
            await db.execute(
                "SELECT * FROM reminders WHERE user_id = ? ORDER BY remind_at ASC",
                (user_id,),
            )
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        await db.close()


async def delete_reminder(reminder_id: int, user_id: int) -> bool:
    db = await get_db()
    try:
        cursor = await db.execute(
            "DELETE FROM reminders WHERE id = ? AND user_id = ?",
            (reminder_id, user_id),
        )
        await db.commit()
        return cursor.rowcount > 0
    finally:
        await db.close()


async def get_due_reminders() -> List[dict]:
    now = datetime.now(timezone.utc).isoformat()
    db = await get_db()
    try:
        rows = await (
            await db.execute(
                "SELECT * FROM reminders WHERE is_sent = 0 AND remind_at <= ?",
                (now,),
            )
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        await db.close()


async def mark_sent(reminder_id: int) -> None:
    db = await get_db()
    try:
        await db.execute(
            "UPDATE reminders SET is_sent = 1 WHERE id = ?", (reminder_id,)
        )
        await db.commit()
    finally:
        await db.close()
