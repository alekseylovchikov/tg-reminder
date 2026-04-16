import pytest
import pytest_asyncio
from datetime import datetime, timezone, timedelta

from backend.database import (
    init_db,
    create_reminder,
    get_reminders,
    delete_reminder,
    get_due_reminders,
    mark_sent,
)


@pytest_asyncio.fixture(autouse=True)
async def _init():
    await init_db()


@pytest.mark.asyncio
async def test_create_and_get():
    future = datetime.now(timezone.utc) + timedelta(hours=1)
    row = await create_reminder(123, "Test", "Desc", future)
    assert row["title"] == "Test"
    assert row["user_id"] == 123
    assert row["is_sent"] == 0

    reminders = await get_reminders(123)
    assert len(reminders) == 1
    assert reminders[0]["id"] == row["id"]


@pytest.mark.asyncio
async def test_get_reminders_isolation():
    future = datetime.now(timezone.utc) + timedelta(hours=1)
    await create_reminder(1, "A", "", future)
    await create_reminder(2, "B", "", future)

    assert len(await get_reminders(1)) == 1
    assert len(await get_reminders(2)) == 1
    assert len(await get_reminders(999)) == 0


@pytest.mark.asyncio
async def test_delete():
    future = datetime.now(timezone.utc) + timedelta(hours=1)
    row = await create_reminder(10, "Del", "", future)

    assert await delete_reminder(row["id"], 10) is True
    assert await delete_reminder(row["id"], 10) is False
    assert len(await get_reminders(10)) == 0


@pytest.mark.asyncio
async def test_delete_wrong_user():
    future = datetime.now(timezone.utc) + timedelta(hours=1)
    row = await create_reminder(10, "Mine", "", future)

    assert await delete_reminder(row["id"], 999) is False
    assert len(await get_reminders(10)) == 1


@pytest.mark.asyncio
async def test_due_reminders():
    past = datetime.now(timezone.utc) - timedelta(minutes=5)
    future = datetime.now(timezone.utc) + timedelta(hours=1)

    await create_reminder(1, "Due", "", past)
    await create_reminder(1, "Not due", "", future)

    due = await get_due_reminders()
    assert len(due) == 1
    assert due[0]["title"] == "Due"


@pytest.mark.asyncio
async def test_mark_sent():
    past = datetime.now(timezone.utc) - timedelta(minutes=5)
    row = await create_reminder(1, "Due", "", past)

    await mark_sent(row["id"])

    due = await get_due_reminders()
    assert len(due) == 0

    reminders = await get_reminders(1)
    assert reminders[0]["is_sent"] == 1
