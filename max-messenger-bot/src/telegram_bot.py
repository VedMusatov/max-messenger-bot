import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, filters
from telegram import Update, Bot
from typing import Optional
from .config import Config

logger = logging.getLogger(__name__)

class TelegramBot:
    """Telegram бот для голосового общения"""
    
    def __init__(self):
        self.token = Config.TELEGRAM_BOT_TOKEN
        self.chat_id = Config.TELEGRAM_CHAT_ID
        self.bot = Bot(token=self.token)
        self.updater = None
        
        if not self.token or not self.chat_id:
            logger.error("Telegram bot token or chat ID not configured")
            raise ValueError("Telegram bot configuration incomplete")
    
    def start(self):
        """Запуск Telegram бота"""
        try:
            self.updater = Updater(token=self.token, use_context=True)
            
            # Добавляем обработчики
            dispatcher = self.updater.dispatcher
            
            # Команды
            dispatcher.add_handler(CommandHandler("start", self.start_command))
            dispatcher.add_handler(CommandHandler("help", self.help_command))
            
            # Обработка текстовых сообщений
            dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.text_message))
            
            # Обработка голосовых сообщений
            dispatcher.add_handler(MessageHandler(filters.VOICE, self.voice_message))
            
            # Обработка фото
            dispatcher.add_handler(MessageHandler(filters.PHOTO, self.photo_message))
            
            # Обработка ошибок
            dispatcher.add_error_handler(self.error_handler)
            
            logger.info("✅ Telegram bot started successfully")
            
        except Exception as e:
            logger.error(f"Error starting Telegram bot: {e}")
            raise
    
    def start_command(self, update: Update, context: CallbackContext):
        """Обработка команды /start"""
        try:
            welcome_message = f"""
🤖 {Config.BOT_NAME}
Версия: {Config.BOT_VERSION}

Я бот для мессенджера Max Messenger с поддержкой голосового общения!

📱 Функции:
• Отправка сообщений в Max Messenger
• Прием сообщений из Max Messenger
• Голосовое общение
• Обработка фото

🔧 Команды:
• /help - помощь
• /status - статус бота
• /test - тестовое сообщение
            """
            
            update.message.reply_text(welcome_message)
            logger.info(f"Sent welcome message to {update.message.chat_id}")
            
        except Exception as e:
            logger.error(f"Error in start_command: {e}")
    
    def help_command(self, update: Update, context: CallbackContext):
        """Обработка команды /help"""
        try:
            help_message = """
📚 Помощь по боту Max Messenger

🔧 Основные команды:
• /start - начать работу
• /help - эта справка
• /status - текущий статус
• /test - отправить тестовое сообщение

💬 Формат сообщений:
• Просто отправьте текстовое сообщение - оно будет переслано в Max Messenger
• Отправьте голосовое сообщение - оно будет преобразовано в текст
• Отправьте фото - оно будет сохранено и переслано

🎯 Интеграция:
• Бот работает с Max Messenger
• Поддерживает голосовое общение
• Логирует все сообщения
            """
            
            update.message.reply_text(help_message)
            logger.info(f"Sent help message to {update.message.chat_id}")
            
        except Exception as e:
            logger.error(f"Error in help_command: {e}")
    
    def text_message(self, update: Update, context: CallbackContext):
        """Обработка текстовых сообщений"""
        try:
            text = update.message.text
            chat_id = update.message.chat_id
            
            logger.info(f"Received text message from {chat_id}: {text}")
            
            # Здесь можно добавить логику отправки в Max Messenger
            # Пока просто отправляем подтверждение
            response = f"✅ Получено сообщение: {text}"
            update.message.reply_text(response)
            
        except Exception as e:
            logger.error(f"Error in text_message: {e}")
            update.message.reply_text("❌ Произошла ошибка при обработке сообщения")
    
    def voice_message(self, update: Update, context: CallbackContext):
        """Обработка голосовых сообщений"""
        try:
            voice_file = update.message.voice
            chat_id = update.message.chat_id
            
            logger.info(f"Received voice message from {chat_id}")
            
            # Получаем файл голосового сообщения
            voice_file_info = voice_file.get_file()
            voice_url = voice_file_info.file_path
            
            # Здесь можно добавить логику распознавания речи
            # Пока просто отправляем подтверждение
            response = f"✅ Получено голосовое сообщение\\nДлительность: {voice_file.duration} секунд"
            update.message.reply_text(response)
            
        except Exception as e:
            logger.error(f"Error in voice_message: {e}")
            update.message.reply_text("❌ Произошла ошибка при обработке голосового сообщения")
    
    def photo_message(self, update: Update, context: CallbackContext):
        """Обработка фото сообщений"""
        try:
            photo_file = update.message.photo[-1]  # Получаем фото наилучшего качества
            chat_id = update.message.chat_id
            
            logger.info(f"Received photo message from {chat_id}")
            
            # Получаем файл фото
            photo_file_info = photo_file.get_file()
            photo_url = photo_file_info.file_path
            
            # Здесь можно добавить логику обработки фото
            # Пока просто отправляем подтверждение
            response = f"✅ Получено фото\\nРазмер: {photo_file.width}x{photo_file.height}"
            update.message.reply_text(response)
            
        except Exception as e:
            logger.error(f"Error in photo_message: {e}")
            update.message.reply_text("❌ Произошла ошибка при обработке фото")
    
    def error_handler(self, update: Update, context: CallbackContext):
        """Обработчик ошибок"""
        logger.error(f"Update {update} caused error {context.error}")
    
    def send_message(self, text: str, chat_id: str = None) -> bool:
        """Отправка сообщения в Telegram"""
        try:
            target_chat_id = chat_id or self.chat_id
            
            self.bot.send_message(
                chat_id=target_chat_id,
                text=text
            )
            
            logger.info(f"Message sent to {target_chat_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False
    
    def send_voice(self, voice_file_path: str, chat_id: str = None) -> bool:
        """Отправка голосового сообщения в Telegram"""
        try:
            target_chat_id = chat_id or self.chat_id
            
            with open(voice_file_path, 'rb') as voice_file:
                self.bot.send_voice(
                    chat_id=target_chat_id,
                    voice=voice_file
                )
            
            logger.info(f"Voice message sent to {target_chat_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending voice message: {e}")
            return False
    
    def start_polling(self):
        """Запуск опроса сообщений"""
        if self.updater:
            self.updater.start_polling()
            logger.info("🔄 Telegram bot polling started")
    
    def stop(self):
        """Остановка бота"""
        if self.updater:
            self.updater.stop()
            logger.info("🛑 Telegram bot stopped")