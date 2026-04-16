import hashlib
import hmac
import json
from urllib.parse import urlencode

import pytest

from backend.auth import validate_init_data
from backend.config import BOT_TOKEN


def _make_init_data(user_id: int, tamper: bool = False) -> str:
    user = json.dumps({"id": user_id, "first_name": "Test"})
    params = {"user": user, "auth_date": "1700000000", "query_id": "AAHtest"}

    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(params.items())
    )
    secret = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
    h = hmac.new(secret, data_check_string.encode(), hashlib.sha256).hexdigest()

    if tamper:
        h = "0" * 64

    params["hash"] = h
    return urlencode(params)


def test_valid_init_data():
    data = _make_init_data(42)
    assert validate_init_data(data) == 42


def test_tampered_hash():
    data = _make_init_data(42, tamper=True)
    assert validate_init_data(data) is None


def test_missing_hash():
    assert validate_init_data("user=test&auth_date=123") is None


def test_empty_string():
    assert validate_init_data("") is None
