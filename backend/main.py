import asyncio
import logging

import uvicorn

from backend.api import create_api
from backend.bot import create_bot
from backend.config import API_HOST, API_PORT
from backend.database import init_db, close_db
from backend.scheduler import setup_scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    await init_db()
    logger.info("Database initialized")

    bot_app = create_bot()
    api_app = create_api(bot_app)

    async with bot_app:
        setup_scheduler(bot_app)
        await bot_app.start()
        await bot_app.updater.start_polling()
        logger.info("Bot polling started")

        config = uvicorn.Config(api_app, host=API_HOST, port=API_PORT, log_level="info")
        server = uvicorn.Server(config)

        try:
            await server.serve()
        finally:
            await bot_app.updater.stop()
            await bot_app.stop()
            await close_db()
            logger.info("Shutdown complete")


if __name__ == "__main__":
    asyncio.run(main())
