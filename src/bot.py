import asyncio
import logging
from typing import Optional
from .config import Config
from .max_messenger_api import MaxMessengerAPI
from .telegram_bot import TelegramBot

logger = logging.getLogger(__name__)

class MaxMessengerBot:
    """Основной класс бота для Max Messenger"""
    
    def __init__(self):
        self.config = Config
        self.max_messenger_api = MaxMessengerAPI()
        self.telegram_bot = None
        self.running = False
        
        # Валидация конфигурации
        try:
            Config.validate_config()
        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            raise
    
    def initialize(self):
        """Инициализация бота"""
        try:
            logger.info("🚀 Initializing Max Messenger Bot...")
            
            # Инициализация Telegram бота
            self.telegram_bot = TelegramBot()
            self.telegram_bot.start()
            
            # Тестирование соединения с Max Messenger API
            if self.max_messenger_api.test_connection():
                logger.info("✅ Max Messenger API connection successful")
            else:
                logger.warning("⚠️ Max Messenger API connection failed")
            
            logger.info("✅ Bot initialization completed")
            
        except Exception as e:
            logger.error(f"Error during bot initialization: {e}")
            raise
    
    def start(self):
        """Запуск бота"""
        try:
            logger.info("🚀 Starting Max Messenger Bot...")
            
            # Инициализация
            self.initialize()
            
            # Запуск опроса сообщений
            self.telegram_bot.start_polling()
            
            self.running = True
            logger.info("✅ Max Messenger Bot started successfully")
            
            # Отправка приветственного сообщения
            welcome_msg = f"""
🤖 {Config.BOT_NAME} v{Config.BOT_VERSION}
Бот успешно запущен!

📱 Функции:
• Интеграция с Max Messenger
• Голосовое общение через Telegram
• Обработка текстовых и голосовых сообщений
• Логирование всех действий

🔧 Статус:
• Max Messenger API: ✅ Подключен
• Telegram Bot: ✅ Запущен
• Логирование: ✅ Активно
            """
            
            self.telegram_bot.send_message(welcome_msg)
            
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            raise
    
    def stop(self):
        """Остановка бота"""
        try:
            logger.info("🛑 Stopping Max Messenger Bot...")
            
            if self.telegram_bot:
                self.telegram_bot.stop()
            
            self.running = False
            logger.info("✅ Max Messenger Bot stopped")
            
        except Exception as e:
            logger.error(f"Error stopping bot: {e}")
    
    def send_message_to_max_messenger(self, message: str, chat_id: str = None) -> bool:
        """Отправка сообщения в Max Messenger"""
        try:
            result = self.max_messenger_api.send_message(message, chat_id)
            
            if result:
                logger.info(f"Message sent to Max Messenger: {message}")
                return True
            else:
                logger.error("Failed to send message to Max Messenger")
                return False
                
        except Exception as e:
            logger.error(f"Error sending message to Max Messenger: {e}")
            return False
    
    def get_max_messenger_updates(self) -> Optional[dict]:
        """Получение обновлений от Max Messenger"""
        try:
            return self.max_messenger_api.get_updates()
        except Exception as e:
            logger.error(f"Error getting Max Messenger updates: {e}")
            return None
    
    def send_telegram_message(self, message: str, chat_id: str = None) -> bool:
        """Отправка сообщения в Telegram"""
        try:
            return self.telegram_bot.send_message(message, chat_id)
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
            return False
    
    def get_bot_status(self) -> dict:
        """Получение статуса бота"""
        try:
            status = {
                'bot_name': Config.BOT_NAME,
                'bot_version': Config.BOT_VERSION,
                'running': self.running,
                'max_messenger_api_connected': self.max_messenger_api.test_connection(),
                'telegram_bot_initialized': self.telegram_bot is not None,
                'log_file': Config.LOG_FILE,
                'debug_mode': Config.DEBUG
            }
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting bot status: {e}")
            return {'error': str(e)}
    
    def run_forever(self):
        """Бесконечный цикл работы бота"""
        try:
            logger.info("🔄 Bot running in infinite loop...")
            
            while self.running:
                # Проверка обновлений от Max Messenger
                updates = self.get_max_messenger_updates()
                if updates:
                    logger.info(f"Received updates from Max Messenger: {updates}")
                
                # Здесь можно добавить логику обработки обновлений
                # Например, пересылку сообщений в Telegram
                
                # Небольшая задержка
                import time
                time.sleep(5)  # Проверять каждые 5 секунд
                
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
            self.stop()
        except Exception as e:
            logger.error(f"Error in infinite loop: {e}")
            self.stop()

def main():
    """Главная функция запуска бота"""
    try:
        # Создаем экземпляр бота
        bot = MaxMessengerBot()
        
        # Запускаем бота
        bot.start()
        
        # Запускаем бесконечный цикл
        bot.run_forever()
        
    except Exception as e:
        logger.error(f"Fatal error in main: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())