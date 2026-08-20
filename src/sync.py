import logging
from .max_api import MaxAPI
from .telegram_bot import TelegramBot
from .hermes_agent import HermesAgent

logger = logging.getLogger(__name__)


class Sync:
    """Bridge: Telegram <-> Hermes AI <-> MAX"""

    def __init__(self, max_api: MaxAPI, telegram_bot: TelegramBot, hermes: HermesAgent):
        self.max = max_api
        self.tg = telegram_bot
        self.hermes = hermes
        self.max_user_ids = set()

    def on_message(self, event: dict):
        """Handle incoming message from any platform"""
        platform = event["platform"]
        msg_type = event["type"]
        text = event.get("text", "")
        chat_id = event.get("chat_id")
        user = event.get("user", {})

        if msg_type == "start":
            logger.info(f"Bridge: start from {platform} user={user.get('first_name', '?')} chat={chat_id}")
            if platform == "max" and chat_id:
                self.max_user_ids.add(chat_id)
            return

        if not text:
            return

        logger.info(f"Bridge: {platform} -> AI: {text[:80]}")

        ai_reply = self.hermes.chat(chat_id, text)

        if platform == "telegram":
            self.tg.send_message(ai_reply, chat_id)
            for uid in self.max_user_ids:
                self.max.send_message(uid, ai_reply)
        elif platform == "max":
            self.max.send_message(chat_id, ai_reply)
            if self.tg.default_chat_id:
                self.tg.send_message(ai_reply)

        logger.info(f"Bridge: AI replied ({len(ai_reply)} chars) to {platform}+other")
