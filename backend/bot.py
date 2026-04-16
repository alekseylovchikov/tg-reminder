from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.request import HTTPXRequest

from backend.config import BOT_TOKEN, WEBAPP_URL, PROXY_URL, CONNECT_TIMEOUT, READ_TIMEOUT


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="📋 Мои напоминания",
                    web_app=WebAppInfo(url=WEBAPP_URL),
                )
            ]
        ]
    )
    await update.message.reply_text(
        "Привет! Я бот-напоминалка.\n\n"
        "Нажми кнопку ниже, чтобы открыть приложение и создать напоминание.",
        reply_markup=keyboard,
    )


def create_bot() -> Application:
    builder = Application.builder().token(BOT_TOKEN)

    request_kwargs = {
        "connect_timeout": CONNECT_TIMEOUT,
        "read_timeout": READ_TIMEOUT,
    }
    if PROXY_URL:
        request_kwargs["proxy"] = PROXY_URL

    builder = builder.request(HTTPXRequest(**request_kwargs))

    app = builder.build()
    app.add_handler(CommandHandler("start", start))
    return app
