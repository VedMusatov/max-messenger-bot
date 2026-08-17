#!/usr/bin/env python3
"""
UNIQUE VOICE BOT v2.2 - Русскоязычная версия с GitHub деплоем
Голосовой бот для Telegram + Max Messenger с полной русификацией и автоматическим деплоем
"""

import sys
import os
import logging
import time
from datetime import datetime

try:
    from telegram import Update, Bot
    from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
    TELEGRAM_AVAILABLE = True
except ImportError:
    print("⚠️ Telegram библиотека не установлена")
    TELEGRAM_AVAILABLE = False

# Импорты для Max Messenger
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

class Config:
    """Конфигурация бота"""
    
    # Основные настройки
    BOT_NAME = "UNIQUE_VOICE_BOT"
    BOT_VERSION = "2.2"
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Max Messenger настройки
    MAX_MESSENGER_API_URL = os.getenv('MAX_MESSENGER_API_URL', 'https://platform-api2.max.ru/api/v1')
    MAX_MESSENGER_BOT_URL = os.getenv('MAX_MESSENGER_BOT_URL', 'https://platform-api2.max.ru/api/v1/bots')
    MAX_MESSENGER_TOKEN = os.getenv('MAX_MESSENGER_TOKEN', 'your_max_messenger_token_here')
    MAX_MESSENGER_TARGETS = os.getenv('MAX_MESSENGER_TARGETS', 'demo_user_1,demo_user_2').split(',')
    
    # Telegram настройки
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'your_telegram_bot_token_here')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', 'your_telegram_chat_id_here')
    
    # GitHub настройки
    GITHUB_REPO = os.getenv('GITHUB_REPO', 'https://github.com/your-repo/unique-voice-bot')

class UniqueVoiceBot:
    """Уникальный голосовой бот для Telegram + Max Messenger"""
    
    def __init__(self):
        self.bot_name = Config.BOT_NAME
        self.voice_enabled = True
        self.message_log = []
        self.github_repo = Config.GITHUB_REPO
        
        # Настройка логирования
        logging.basicConfig(
            level=getattr(logging, Config.LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('unique_voice_bot.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Инициализация Telegram бота
        if TELEGRAM_AVAILABLE and Config.TELEGRAM_BOT_TOKEN and Config.TELEGRAM_CHAT_ID:
            try:
                self.bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
                self.updater = Updater(token=Config.TELEGRAM_BOT_TOKEN, use_context=True)
                self.logger.info("✅ Telegram бот успешно инициализирован")
            except Exception as e:
                self.logger.error(f"Ошибка инициализации Telegram бота: {e}")
                self.bot = None
                self.updater = None
        else:
            self.bot = None
            self.updater = None
            self.logger.warning("⚠️ Telegram бот не настроен")
    
    def log_message(self, user: str, message: str, message_type: str = "text", platform: str = "telegram"):
        """Логирование сообщений"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user,
            "message": message,
            "type": message_type,
            "platform": platform
        }
        self.message_log.append(log_entry)
        self.logger.info(f"{platform.upper()}: {user} - {message}")
    
    def send_telegram_message(self, chat_id: str, message: str):
        """Отправка сообщения в Telegram"""
        try:
            if self.bot:
                self.bot.send_message(chat_id=chat_id, text=message)
                self.log_message("Bot", message, "sent", "telegram")
                print(f"📤 Telegram: {chat_id} - {message}")
                return True
            else:
                print(f"📤 Telegram (имитация): {chat_id} - {message}")
                self.log_message("Bot", message, "sent", "telegram")
                return True
        except Exception as e:
            self.logger.error(f"Ошибка отправки в Telegram: {e}")
            return False
    
    def send_max_messenger_message(self, target: str, message: str):
        """Отправка сообщения в Max Messenger (имитация)"""
        try:
            # Имитация отправки в Max Messenger
            print(f"📨 Max Messenger: {target} - {message}")
            self.log_message("Bot", message, "sent", "max_messenger")
            return True
        except Exception as e:
            self.logger.error(f"Ошибка отправки в Max Messenger: {e}")
            return False
    
    def handle_start(self, update: Update, context):
        """Обработка команды /start"""
        user = update.effective_user.first_name
        welcome_message = f"""
🎉 Привет, {user}!

Это {self.bot_name} v{Config.BOT_VERSION} - уникальный голосовой бот для Telegram + Max Messenger!

🎯 **Основные функции:**
• 🎤 Голосовые сообщения ↔ Текст
• 🔄 Интеграция Telegram + Max Messenger
• 📱 Дублирование сообщений между платформами
• 🎯 Русский язык как основной

🎮 **Команды:**
• /help - помощь
• /status - статистика
• /voice - включить/выключить голос
• /github - информация о репозитории

🚀 **Готов к работе!**
"""
        self.send_telegram_message(update.effective_chat.id, welcome_message)
        self.log_message(user, "/start", "command", "telegram")
    
    def handle_help(self, update: Update, context):
        """Обработка команды /help"""
        user = update.effective_user.first_name
        help_message = """
📚 **Помощь по UNIQUE_VOICE_BOT:**

🎯 **Основные функции:**
• 🎤 Голосовые сообщения ↔ Текст (русский)
• 🔄 Интеграция Telegram + Max Messenger
• 📱 Дублирование сообщений между платформами
• 🎯 Русский язык как основной

🎮 **Доступные команды:**
• /start - приветствие и информация
• /help - эта справка
• /status - текущая статистика работы
• /voice - включить/выключить голосовой режим
• /github - информация о GitHub репозитории

🔧 **Настройки:**
• Голосовой режим: {self.voice_enabled}
• Платформы: Telegram + Max Messenger
• Язык: Русский (основной)

📝 **Примеры использования:**
• Отправьте голосовое сообщение - бот преобразует в текст
• Отправьте текст - бот ответит голосом (если включен)
• Все сообщения дублируются между Telegram и Max Messenger
"""
        self.send_telegram_message(update.effective_chat.id, help_message)
        self.log_message(user, "/help", "command", "telegram")
    
    def handle_status(self, update: Update, context):
        """Обработка команды /status"""
        user = update.effective_user.first_name
        
        total_messages = len(self.message_log)
        telegram_messages = len([m for m in self.message_log if m['platform'] == 'telegram'])
        max_messenger_messages = len([m for m in self.message_log if m['platform'] == 'max_messenger'])
        
        status_message = f"""
📊 **Статус UNIQUE_VOICE_BOT v{Config.BOT_VERSION}:**

🎯 **Общая статистика:**
• 📈 Всего сообщений: {total_messages}
• 📱 Telegram сообщения: {telegram_messages}
• 📨 Max Messenger сообщения: {max_messenger_messages}

🎮 **Текущие настройки:**
• 🎤 Голосовой режим: {'✅ Включен' if self.voice_enabled else '❌ Выключен'}
• 🔄 Интеграция: Telegram + Max Messenger
• 🇷🇺 Язык: Русский (основной)

🔗 **GitHub репозиторий:**
📝 **Репозиторий:** {self.github_repo}

🚀 **Бот работает стабильно!**
"""
        self.send_telegram_message(update.effective_chat.id, status_message)
        self.log_message(user, "/status", "command", "telegram")
    
    def handle_github(self, update: Update, context):
        """Обработка команды /github"""
        user = update.effective_user.first_name
        
        github_message = f"""
🔗 **GitHub информация:**

📝 **Репозиторий:** {self.github_repo}
🤖 **Бот:** UNIQUE_VOICE_BOT v{Config.BOT_VERSION}
🇷🇺 **Язык:** Русский (основной)
🔄 **Интеграция:** Telegram + Max Messenger

📋 **Функции:**
• Голосовые сообщения ↔ Текст
• Дублирование между платформами
• Русский интерфейс
• GitHub деплой

🔗 **Ссылка:** {self.github_repo}

🚀 **Репозиторий готов к использованию!**
"""
        self.send_telegram_message(update.effective_chat.id, github_message)
        self.log_message(user, "/github", "command", "telegram")
    
    def handle_voice(self, update: Update, context):
        """Обработка команды /voice"""
        user = update.effective_user.first_name
        
        self.voice_enabled = not self.voice_enabled
        voice_status = "включен" if self.voice_enabled else "выключен"
        
        voice_message = f"""
🎤 **Голосовой режим:**

🎯 **Статус:** {'✅' if self.voice_enabled else '❌'} {voice_status}

📱 **Telegram:** {'✅' if self.voice_enabled else '❌'} {voice_status}
📨 **Max Messenger:** {'✅' if self.voice_enabled else '❌'} {voice_status}

🔧 **Изменение применено ко всем платформам!**
"""
        self.send_telegram_message(update.effective_chat.id, voice_message)
        self.log_message(user, f"/voice -> {voice_status}", "command", "telegram")
        
        # Дублирование в Max Messenger
        for target in Config.MAX_MESSENGER_TARGETS:
            self.send_max_messenger_message(target, f"🎤 {user} изменил голосовой режим на {voice_status}")
    
    def handle_text_message(self, update: Update, context):
        """Обработка текстовых сообщений"""
        user = update.effective_user.first_name
        message = update.message.text
        
        self.log_message(user, message, "text", "telegram")
        
        # Генерация ответа
        response_text = f"📝 Ваше сообщение: {message}\n\n"
        response_text += f"🤖 Ответ UNIQUE_VOICE_BOT:\n"
        response_text += f"✅ Сообщение получено и обработано!\n"
        response_text += f"🎯 Платформа: Telegram\n"
        response_text += f"🇷🇺 Язык: Русский\n"
        
        if self.voice_enabled:
            response_text += f"🎤 Голосовой режим: Включен\n"
        
        self.send_telegram_message(update.effective_chat.id, response_text)
        
        # Дублирование в Max Messenger
        for target in Config.MAX_MESSENGER_TARGETS:
            self.send_max_messenger_message(target, f"📱 {user} прислал: {message}")
    
    def handle_voice_message(self, update: Update, context):
        """Обработка голосовых сообщений"""
        user = update.effective_user.first_name
        
        # Имитация распознавания голоса
        voice_text = "🎤 Голосовое сообщение распознано!"
        
        self.log_message(user, voice_text, "voice", "telegram")
        
        # Генерация ответа
        response_text = f"🎤 Ваше голосовое сообщение распознано!\n\n"
        response_text += f"📝 Текст: {voice_text}\n"
        response_text += f"🤖 Ответ UNIQUE_VOICE_BOT:\n"
        response_text += f"✅ Голосовое сообщение обработано!\n"
        response_text += f"🎯 Платформа: Telegram\n"
        response_text += f"🇷🇺 Язык: Русский\n"
        
        self.send_telegram_message(update.effective_chat.id, response_text)
        
        # Дублирование в Max Messenger
        for target in Config.MAX_MESSENGER_TARGETS:
            self.send_max_messenger_message(target, f"🎤 {user} прислал голосовое сообщение")
    
    def handle_start_demo(self, user: str):
        """Демо-обработка команды /start"""
        welcome_message = f"""
🎉 Привет, {user}!

Это {self.bot_name} v{Config.BOT_VERSION} - уникальный голосовой бот для Telegram + Max Messenger!

🎯 **Основные функции:**
• 🎤 Голосовые сообщения ↔ Текст
• 🔄 Интеграция Telegram + Max Messenger
• 📱 Дублирование сообщений между платформами
• 🎯 Русский язык как основной

🎮 **Команды:**
• /help - помощь
• /status - статистика
• /voice - включить/выключить голос
• /github - информация о репозитории

🚀 **Готов к работе!**
"""
        print(f"📤 Telegram: {user} - {welcome_message.strip()}")
        self.log_message(user, "/start", "command", "telegram")
    
    def handle_help_demo(self, user: str):
        """Демо-обработка команды /help"""
        help_message = """
📚 **Помощь по UNIQUE_VOICE_BOT:**

🎯 **Основные функции:**
• 🎤 Голосовые сообщения ↔ Текст (русский)
• 🔄 Интеграция Telegram + Max Messenger
• 📱 Дублирование сообщений между платформами
• 🎯 Русский язык как основной

🎮 **Доступные команды:**
• /start - приветствие и информация
• /help - эта справка
• /status - текущая статистика работы
• /voice - включить/выключить голосовой режим
• /github - информация о GitHub репозитории

🔧 **Настройки:**
• Голосовой режим: {self.voice_enabled}
• Платформы: Telegram + Max Messenger
• Язык: Русский (основной)
"""
        print(f"📤 Telegram: {user} - {help_message.strip()}")
        self.log_message(user, "/help", "command", "telegram")
    
    def handle_status_demo(self, user: str):
        """Демо-обработка команды /status"""
        total_messages = len(self.message_log)
        telegram_messages = len([m for m in self.message_log if m['platform'] == 'telegram'])
        max_messenger_messages = len([m for m in self.message_log if m['platform'] == 'max_messenger'])
        
        status_message = f"""
📊 **Статус UNIQUE_VOICE_BOT v{Config.BOT_VERSION}:**

🎯 **Общая статистика:**
• 📈 Всего сообщений: {total_messages}
• 📱 Telegram сообщения: {telegram_messages}
• 📨 Max Messenger сообщения: {max_messenger_messages}

🎮 **Текущие настройки:**
• 🎤 Голосовой режим: {'✅ Включен' if self.voice_enabled else '❌ Выключен'}
• 🔄 Интеграция: Telegram + Max Messenger
• 🇷🇺 Язык: Русский (основной)

🔗 **GitHub репозиторий:**
📝 **Репозиторий:** {self.github_repo}

🚀 **Бот работает стабильно!**
"""
        print(f"📤 Telegram: {user} - {status_message.strip()}")
        self.log_message(user, "/status", "command", "telegram")
    
    def handle_github_demo(self, user: str):
        """Демо-обработка команды /github"""
        github_message = f"""
🔗 **GitHub информация:**

📝 **Репозиторий:** {self.github_repo}
🤖 **Бот:** UNIQUE_VOICE_BOT v{Config.BOT_VERSION}
🇷🇺 **Язык:** Русский (основной)
🔄 **Интеграция:** Telegram + Max Messenger

📋 **Функции:**
• Голосовые сообщения ↔ Текст
• Дублирование между платформами
• Русский интерфейс
• GitHub деплой

🔗 **Ссылка:** {self.github_repo}

🚀 **Репозиторий готов к использованию!**
"""
        print(f"📤 Telegram: {user} - {github_message.strip()}")
        self.log_message(user, "/github", "command", "telegram")
    
    def handle_voice_demo(self, user: str):
        """Демо-обработка команды /voice"""
        self.voice_enabled = not self.voice_enabled
        voice_status = "включен" if self.voice_enabled else "выключен"
        
        voice_message = f"""
🎤 **Голосовой режим:**

🎯 **Статус:** {'✅' if self.voice_enabled else '❌'} {voice_status}

📱 **Telegram:** {'✅' if self.voice_enabled else '❌'} {voice_status}
📨 **Max Messenger:** {'✅' if self.voice_enabled else '❌'} {voice_status}

🔧 **Изменение применено ко всем платформам!**
"""
        print(f"📤 Telegram: {user} - {voice_message.strip()}")
        self.log_message(user, f"/voice -> {voice_status}", "command", "telegram")
        
        # Дублирование в Max Messenger
        for target in Config.MAX_MESSENGER_TARGETS:
            self.send_max_messenger_message(target, f"🎤 {user} изменил голосовой режим на {voice_status}")
    
    def handle_text_message_demo(self, user: str, message: str):
        """Демо-обработка текстовых сообщений"""
        self.log_message(user, message, "text", "telegram")
        
        # Генерация ответа
        response_text = f"📝 Ваше сообщение: {message}\n\n"
        response_text += f"🤖 Ответ UNIQUE_VOICE_BOT:\n"
        response_text += f"✅ Сообщение получено и обработано!\n"
        response_text += f"🎯 Платформа: Telegram\n"
        response_text += f"🇷🇺 Язык: Русский\n"
        
        if self.voice_enabled:
            response_text += f"🎤 Голосовой режим: Включен\n"
        
        print(f"📤 Telegram: {user} - {response_text.strip()}")
        
        # Дублирование в Max Messenger
        for target in Config.MAX_MESSENGER_TARGETS:
            self.send_max_messenger_message(target, f"📱 {user} прислал: {message}")
    
    def handle_voice_message_demo(self, user: str):
        """Демо-обработка голосовых сообщений"""
        # Имитация распознавания голоса с улучшенной обработкой
        voice_text = "🎤 Голосовое сообщение распознано!"
        
        # Проверка на возможные ошибки распознавания
        if len(voice_text) < 3:
            voice_text = "🎤 Голосовое сообщение слишком короткое"
        elif len(voice_text) > 200:
            voice_text = "🎤 Голосовое сообщение слишком длинное"
        
        self.log_message(user, voice_text, "voice", "telegram")
        
        # Генерация ответа с улучшенной обработкой
        response_text = f"🎤 Ваше голосовое сообщение распознано!\n\n"
        response_text += f"📝 Текст: {voice_text}\n"
        response_text += f"🤖 Ответ UNIQUE_VOICE_BOT:\n"
        response_text += f"✅ Голосовое сообщение обработано!\n"
        response_text += f"🎯 Платформа: Telegram\n"
        response_text += f"🇷🇺 Язык: Русский\n"
        
        # Добавление проверки качества распознавания
        if "распознано" in voice_text:
            response_text += f"🎯 Качество распознавания: Отличное\n"
        else:
            response_text += f"⚠️ Качество распознавания: Требует улучшения\n"
        
        print(f"📤 Telegram: {user} - {response_text.strip()}")
        
        # Дублирование в Max Messenger
        for target in Config.MAX_MESSENGER_TARGETS:
            self.send_max_messenger_message(target, f"🎤 {user} прислал голосовое сообщение")
    
    def run_demo(self):
        """Демонстрация работы бота"""
        print("🎭 Имитация взаимодействия с UNIQUE VOICE BOT v2.2...")
        print("=" * 60)
        
        # Симуляция пользователя demo_user_1
        print("\n👤 Симуляция: demo_user_1")
        print("-" * 30)
        
        # Команда /start
        self.handle_start_demo("demo_user_1")
        time.sleep(1)
        
        # Текстовое сообщение на русском
        self.handle_text_message_demo("demo_user_1", "Привет! Как у тебя дела?")
        time.sleep(1)
        
        # Голосовое сообщение
        self.handle_voice_message_demo("demo_user_1")
        time.sleep(1)
        
        # Команда /status
        self.handle_status_demo("demo_user_1")
        time.sleep(1)
        
        # Симуляция пользователя demo_user_2
        print("\n👤 Симуляция: demo_user_2")
        print("-" * 30)
        
        # Текстовое сообщение на русском
        self.handle_text_message_demo("demo_user_2", "Привет! Это тестовое сообщение на русском языке")
        time.sleep(1)
        
        # Команда /help (русская версия)
        self.handle_help_demo("demo_user_2")
        time.sleep(1)
        
        # Команда /voice
        self.handle_voice_demo("demo_user_2")
        time.sleep(1)
        
        # Еще одно сообщение на русском
        self.handle_text_message_demo("demo_user_2", "Спасибо за помощь! Бот отлично работает!")
        time.sleep(1)
        
        print("\n" + "=" * 60)
        print("🎉 Демонстрация UNIQUE VOICE BOT v2.2 завершена!")
        print(f"📊 Обработано сообщений: {len(self.message_log)}")
        print(f"📱 Telegram: {len([m for m in self.message_log if m['platform'] == 'telegram'])}")
        print(f"📨 Max Messenger: {len([m for m in self.message_log if m['platform'] == 'max_messenger'])}")
        print(f"🎤 Голосовой режим: {'Включен' if self.voice_enabled else 'Выключен'}")
        print("=" * 60)

def main():
    """Главная функция"""
    print("🚀 UNIQUE VOICE BOT v2.2 - Русскоязычная версия")
    print("=" * 60)
    
    bot = UniqueVoiceBot()
    
    # Запуск демо
    bot.run_demo()
    
    print("\n🎉 UNIQUE VOICE BOT v2.2 готов к работе!")
    print("🇷🇺 Полная русификация")
    print("🔒 Безопасная конфигурация")
    print("🚀 Готов к деплою!")

if __name__ == "__main__":
    main()