import logging
from typing import Callable
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from .config import Config

logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self):
        self.token = Config.TELEGRAM_BOT_TOKEN
        self.default_chat_id = Config.TELEGRAM_CHAT_ID
        self.app = None
        self._on_message = None

    def build(self, on_message: Callable):
        self._on_message = on_message
        self.app = Application.builder().token(self.token).build()

        self.app.add_handler(CommandHandler("start", self._cmd_start))
        self.app.add_handler(CommandHandler("help", self._cmd_help))
        self.app.add_handler(CommandHandler("status", self._cmd_status))
        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self._on_text)
        )
        self.app.add_handler(
            MessageHandler(filters.VOICE | filters.AUDIO, self._on_voice)
        )

    def send_message(self, text: str, chat_id: str = None) -> bool:
        target = chat_id or self.default_chat_id
        if not target or not self.app or not self.app.bot:
            return False
        import asyncio
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                future = pool.submit(
                    asyncio.run,
                    self.app.bot.send_message(chat_id=target, text=text),
                )
                future.result(timeout=10)
            return True
        else:
            asyncio.run(self.app.bot.send_message(chat_id=target, text=text))
            return True

    async def _cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        user = update.effective_user
        logger.info(f"Telegram /start from {user.first_name} (chat={chat_id})")

        text = (
            f"Привет, {user.first_name}!\n\n"
            "Я Hermes Bridge Bot.\n"
            "Отправляй мне сообщения — я отвечу через AI.\n"
            "Также я синхронизирую переписку с MAX.\n\n"
            "Команды:\n"
            "/help — помощь\n"
            "/status — статус бота"
        )
        await update.message.reply_text(text)

        if self._on_message:
            self._on_message({
                "platform": "telegram",
                "type": "start",
                "chat_id": chat_id,
                "user": user,
                "text": "",
            })

    async def _cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Hermes Bridge Bot\n\n"
            "Отправь текст — я отвечу с помощью AI.\n"
            "Синхронизация: Telegram <-> MAX\n\n"
            "/start — начать\n"
            "/status — статус"
        )

    async def _cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        from .config import Config as C
        tg = "OK" if C.TELEGRAM_BOT_TOKEN else "MISSING"
        mx = "OK" if C.MAX_BOT_TOKEN else "MISSING"
        ai = "OK" if (C.HERMES_API_KEY or C.HERMES_PROVIDER == "local") else "MISSING"
        await update.message.reply_text(
            f"Статус:\nTelegram: {tg}\nMAX: {mx}\nAI ({C.HERMES_PROVIDER}): {ai}"
        )

    async def _on_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        chat_id = update.effective_chat.id
        user = update.effective_user
        logger.info(f"Telegram msg from {user.first_name}: {text[:80]}")

        if self._on_message:
            self._on_message({
                "platform": "telegram",
                "type": "message",
                "chat_id": chat_id,
                "user": user,
                "text": text,
            })

    async def _on_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Голосовые сообщения пока не поддерживаются. Отправь текстом."
        )
