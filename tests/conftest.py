import os
import pytest

os.environ.setdefault("BOT_TOKEN", "000000000:AAFakeTestTokenForTestingOnly1234567")
os.environ.setdefault("DB_PATH", ":memory:")


@pytest.fixture(autouse=True)
def _use_memory_db(monkeypatch: pytest.MonkeyPatch):
    import tempfile, os
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    monkeypatch.setattr("backend.config.DB_PATH", path)
    monkeypatch.setattr("backend.database.DB_PATH", path)
    yield
    os.unlink(path)
