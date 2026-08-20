import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class Config:
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

    # MAX Messenger
    MAX_BOT_TOKEN = os.getenv("MAX_BOT_TOKEN", "")
    MAX_API_BASE = "https://platform-api2.max.ru"

    # AI Agent (Hermes)
    HERMES_PROVIDER = os.getenv("HERMES_PROVIDER", "openrouter")
    HERMES_API_KEY = os.getenv("HERMES_API_KEY", "")
    HERMES_MODEL = os.getenv("HERMES_MODEL", "meta-llama/llama-3.1-8b-instruct:free")
    HERMES_LOCAL_URL = os.getenv("HERMES_LOCAL_URL", "http://localhost:11434/v1")

    # System
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    @classmethod
    def validate(cls):
        errors = []
        if not cls.TELEGRAM_BOT_TOKEN:
            errors.append("TELEGRAM_BOT_TOKEN")
        if not cls.MAX_BOT_TOKEN:
            errors.append("MAX_BOT_TOKEN")
        if cls.HERMES_PROVIDER != "local" and not cls.HERMES_API_KEY:
            errors.append(f"HERMES_API_KEY (provider={cls.HERMES_PROVIDER})")
        if errors:
            logger.warning(f"Missing config: {', '.join(errors)}")
            return False
        return True

    @classmethod
    def print_status(cls):
        tg = "OK" if cls.TELEGRAM_BOT_TOKEN else "MISSING"
        mx = "OK" if cls.MAX_BOT_TOKEN else "MISSING"
        ai = "OK" if cls.HERMES_API_KEY or cls.HERMES_PROVIDER == "local" else "MISSING"
        logger.info(f"Config status - Telegram: {tg}, MAX: {mx}, Hermes({cls.HERMES_PROVIDER}): {ai}")
