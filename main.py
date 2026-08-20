import sys
import os
import logging

sys.path.insert(0, os.path.dirname(__file__))

from src.config import Config
from src.max_api import MaxAPI
from src.telegram_bot import TelegramBot
from src.hermes_agent import HermesAgent
from src.sync import Sync


def main():
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL, logging.INFO),
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("bot.log", encoding="utf-8"),
        ],
    )
    logger = logging.getLogger("main")

    logger.info("=== Hermes Bridge Bot starting ===")
    Config.print_status()

    max_api = MaxAPI()
    telegram_bot = TelegramBot()
    hermes = HermesAgent()
    sync = Sync(max_api, telegram_bot, hermes)

    bot_info = max_api.get_me()
    if bot_info:
        logger.info(f"MAX bot ready: {bot_info.get('first_name')} (@{bot_info.get('username')})")
    else:
        logger.warning("MAX bot connection failed — check MAX_BOT_TOKEN")

    telegram_bot.build(on_message=sync.on_message)
    max_api.start_polling(on_message=sync.on_message)

    logger.info("=== Bot is running. Press Ctrl+C to stop. ===")

    try:
        telegram_bot.app.run_polling(drop_pending_updates=True)
    except KeyboardInterrupt:
        pass
    finally:
        max_api.stop_polling()
        logger.info("Done.")


if __name__ == "__main__":
    main()
