import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.environ["BOT_TOKEN"]
WEBAPP_URL: str = os.environ.get("WEBAPP_URL", "http://localhost:5173")
MONGO_URI: str = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB: str = os.environ.get("MONGO_DB", "tg_reminder")
API_HOST: str = os.environ.get("API_HOST", "0.0.0.0")
API_PORT: int = int(os.environ.get("PORT", os.environ.get("API_PORT", "8080")))
PROXY_URL: str = os.environ.get("PROXY_URL", "")
CONNECT_TIMEOUT: float = float(os.environ.get("CONNECT_TIMEOUT", "30"))
READ_TIMEOUT: float = float(os.environ.get("READ_TIMEOUT", "30"))
