from __future__ import annotations

from datetime import datetime, timezone
from typing import List

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from backend.config import MONGO_URI, MONGO_DB

_client: AsyncIOMotorClient | None = None
_db: AsyncIOMotorDatabase | None = None


def _get_db() -> AsyncIOMotorDatabase:
    assert _db is not None, "Call init_db() first"
    return _db


def _doc_to_dict(doc: dict) -> dict:
    doc["id"] = str(doc.pop("_id"))
    return doc


async def init_db() -> None:
    global _client, _db
    _client = AsyncIOMotorClient(MONGO_URI)
    _db = _client[MONGO_DB]

    coll = _db.reminders
    await coll.create_index("user_id")
    await coll.create_index([("is_sent", 1), ("remind_at", 1)])


async def close_db() -> None:
    global _client, _db
    if _client:
        _client.close()
        _client = None
        _db = None


async def create_reminder(
    user_id: int,
    title: str,
    description: str,
    remind_at: datetime,
    remind_at_local: str = "",
) -> dict:
    coll = _get_db().reminders
    doc = {
        "user_id": user_id,
        "title": title,
        "description": description,
        "remind_at": remind_at.astimezone(timezone.utc).isoformat(),
        "remind_at_local": remind_at_local,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "is_sent": False,
    }
    result = await coll.insert_one(doc)
    doc["_id"] = result.inserted_id
    return _doc_to_dict(doc)


async def get_reminders(user_id: int) -> List[dict]:
    coll = _get_db().reminders
    cursor = coll.find({"user_id": user_id}).sort("remind_at", 1)
    return [_doc_to_dict(doc) async for doc in cursor]


async def delete_reminder(reminder_id: str, user_id: int) -> bool:
    coll = _get_db().reminders
    try:
        oid = ObjectId(reminder_id)
    except Exception:
        return False
    result = await coll.delete_one({"_id": oid, "user_id": user_id})
    return result.deleted_count > 0


async def get_due_reminders() -> List[dict]:
    now = datetime.now(timezone.utc).isoformat()
    coll = _get_db().reminders
    cursor = coll.find({"is_sent": False, "remind_at": {"$lte": now}})
    return [_doc_to_dict(doc) async for doc in cursor]


async def mark_sent(reminder_id: str) -> None:
    coll = _get_db().reminders
    await coll.update_one({"_id": ObjectId(reminder_id)}, {"$set": {"is_sent": True}})
