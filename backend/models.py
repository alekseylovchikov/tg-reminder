from datetime import datetime, timezone
from pydantic import BaseModel, field_validator


class ReminderCreate(BaseModel):
    user_id: int
    title: str
    description: str = ""
    remind_at: datetime
    remind_at_local: str = ""

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Title cannot be empty")
        return v

    @field_validator("remind_at")
    @classmethod
    def remind_at_in_future(cls, v: datetime) -> datetime:
        now = datetime.now(timezone.utc)
        compare = v if v.tzinfo else v.replace(tzinfo=timezone.utc)
        if compare <= now:
            raise ValueError("Reminder time must be in the future")
        return v


class ReminderResponse(BaseModel):
    id: str
    user_id: int
    title: str
    description: str
    remind_at: str
    remind_at_local: str
    created_at: str
    is_sent: bool
