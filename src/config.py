import os
import logging
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

class Config:
    """Конфигурация бота Max Messenger"""
    
    # Max Messenger API
    MAX_MESSENGER_API_URL = os.getenv('MAX_MESSENGER_API_URL', 'https://maxmessenger.com/api')
    MAX_MESSENGER_BOT_URL = os.getenv('MAX_MESSENGER_BOT_URL', 'https://maxmessenger.com/bot')
    
    # Telegram Bot
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
    
    # Bot settings
    BOT_NAME = os.getenv('BOT_NAME', 'MaxMessengerBot')
    BOT_VERSION = os.getenv('BOT_VERSION', '1.0.0')
    
    # Max Messenger targets
    MAX_MESSENGER_TARGETS = os.getenv('MAX_MESSENGER_TARGETS', 'Ved').split(',')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'bot.log')
    
    # Development
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    TEST_MODE = os.getenv('TEST_MODE', 'False').lower() == 'true'
    
    @classmethod
    def validate_config(cls):
        """Валидация конфигурации"""
        required_vars = [
            'TELEGRAM_BOT_TOKEN',
            'TELEGRAM_CHAT_ID'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required configuration variables: {', '.join(missing_vars)}")
        
        return True

# Настройка логирования
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)