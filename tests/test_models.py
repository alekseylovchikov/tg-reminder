import pytest
from datetime import datetime, timezone, timedelta
from pydantic import ValidationError

from backend.models import ReminderCreate


def test_valid_reminder():
    future = datetime.now(timezone.utc) + timedelta(hours=1)
    r = ReminderCreate(user_id=1, title="Test", remind_at=future)
    assert r.title == "Test"
    assert r.description == ""


def test_empty_title_rejected():
    future = datetime.now(timezone.utc) + timedelta(hours=1)
    with pytest.raises(ValidationError, match="Title cannot be empty"):
        ReminderCreate(user_id=1, title="   ", remind_at=future)


def test_past_time_rejected():
    past = datetime.now(timezone.utc) - timedelta(hours=1)
    with pytest.raises(ValidationError, match="future"):
        ReminderCreate(user_id=1, title="Late", remind_at=past)


def test_title_stripped():
    future = datetime.now(timezone.utc) + timedelta(hours=1)
    r = ReminderCreate(user_id=1, title="  Hello  ", remind_at=future)
    assert r.title == "Hello"
