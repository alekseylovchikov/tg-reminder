from __future__ import annotations

from typing import List, TYPE_CHECKING

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from backend.auth import validate_init_data
from backend.models import ReminderCreate, ReminderResponse
from backend.scheduler import schedule_reminder
from backend import database as db

if TYPE_CHECKING:
    from telegram.ext import Application


def _get_user_id(authorization: str) -> int:
    user_id = validate_init_data(authorization)
    if user_id is None:
        raise HTTPException(401, "Invalid initData")
    return user_id


def create_api(bot_app: Application) -> FastAPI:
    app = FastAPI(title="TG Reminder API")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    dist_path = Path(__file__).parent.parent / "frontend" / "dist"

    @app.get("/api/reminders", response_model=List[ReminderResponse])
    async def list_reminders(authorization: str = Header()):
        user_id = _get_user_id(authorization)
        rows = await db.get_reminders(user_id)
        return [_row_to_response(r) for r in rows]

    @app.post("/api/reminders", response_model=ReminderResponse, status_code=201)
    async def add_reminder(body: ReminderCreate, authorization: str = Header()):
        user_id = _get_user_id(authorization)
        row = await db.create_reminder(
            user_id=user_id,
            title=body.title,
            description=body.description,
            remind_at=body.remind_at,
            remind_at_local=body.remind_at_local,
        )
        schedule_reminder(bot_app, row)
        return _row_to_response(row)

    @app.delete("/api/reminders/{reminder_id}", status_code=204)
    async def remove_reminder(reminder_id: int, authorization: str = Header()):
        user_id = _get_user_id(authorization)
        deleted = await db.delete_reminder(reminder_id, user_id)
        if not deleted:
            raise HTTPException(404, "Reminder not found")
        for job in bot_app.job_queue.get_jobs_by_name(f"reminder_{reminder_id}"):
            job.schedule_removal()

    if dist_path.exists():
        app.mount("/", StaticFiles(directory=str(dist_path), html=True), name="static")

    return app


def _row_to_response(row: dict) -> ReminderResponse:
    return ReminderResponse(
        id=row["id"],
        user_id=row["user_id"],
        title=row["title"],
        description=row["description"],
        remind_at=row["remind_at"],
        remind_at_local=row.get("remind_at_local", ""),
        created_at=row["created_at"],
        is_sent=bool(row["is_sent"]),
    )
