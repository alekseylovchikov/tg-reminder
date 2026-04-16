from __future__ import annotations

import hashlib
import hmac
import json
from typing import Optional
from urllib.parse import parse_qs

from backend.config import BOT_TOKEN


def validate_init_data(init_data: str) -> Optional[int]:
    """Validate Telegram WebApp initData and return user_id or None."""
    parsed = parse_qs(init_data, keep_blank_values=True)

    if "hash" not in parsed:
        return None

    received_hash = parsed.pop("hash")[0]

    data_check_pairs = sorted(
        f"{k}={v[0]}" for k, v in parsed.items()
    )
    data_check_string = "\n".join(data_check_pairs)

    secret_key = hmac.new(
        b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256
    ).digest()
    calculated_hash = hmac.new(
        secret_key, data_check_string.encode(), hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(calculated_hash, received_hash):
        return None

    if "user" not in parsed:
        return None

    try:
        user_data = json.loads(parsed["user"][0])
        return user_data.get("id")
    except (json.JSONDecodeError, KeyError):
        return None
