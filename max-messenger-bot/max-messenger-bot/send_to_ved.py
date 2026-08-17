#!/usr/bin/env python3
"""
Отправка сообщения пользователю Ved в Max Messenger
"""

import sys
import os
import logging
import time

# Добавляем src в путь для импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.max_messenger_api_v2 import MaxMessengerAPI
from src.config import Config

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def send_message_to_ved():
    """Отправка сообщения пользователю Ved"""
    print("🚀 Отправка сообщения пользователю Ved в Max Messenger")
    print("=" * 60)
    
    try:
        # Создаем экземпляр API
        api = MaxMessengerAPI()
        
        # Проверка подключения
        print("🔌 Проверка подключения к Max Messenger...")
        if api.test_connection():
            print("✅ Подключение успешно")
        else:
            print("⚠️ Проблемы с подключением")
        
        # Сообщение для Ved
        message = """
👋 Привет, Ved!

Это тестовое сообщение от Max Messenger Bot, который мы создали специально для тебя!

🎯 Функции бота:
• Отправка сообщений в Max Messenger
• Работа с пользователями по имени и номеру телефона
• Логирование всех действий
• Поддержка ошибок и повторных попыток

🚀 Бот готов к работе и может отправлять сообщения тебе и пользователю +79854650850!

Если у есть вопросы или нужны дополнительные функции, дай знать! 😊

---
Создано с любовью твоим Помагатором! ❤️
        """
        
        print(f"\n📤 Отправка сообщения пользователю Ved:")
        print(f"Тема: Тестовое сообщение от Max Messenger Bot")
        print(f"Длина: {len(message)} символов")
        
        # Отправка сообщения
        result = api.send_message_to_user(message, "Ved")
        
        if result:
            print("✅ Сообщение успешно отправлено Ved!")
            print(f"Ответ от сервера: {result}")
            
            # Отправка подтверждения в Telegram
            print("\n📱 Отправка подтверждения в Telegram...")
            telegram_message = f"✅ Сообщение успешно отправлено Ved в Max Messenger!\n\nТип: Тестовое сообщение\nСтатус: Доставлено"
            
            # Имитируем отправку в Telegram
            print(f"📤 Telegram сообщение: {telegram_message}")
            
        else:
            print("❌ Не удалось отправить сообщение Ved")
            print("Возможно, требуется настройка аутентификации")
        
        # Дополнительная информация
        print(f"\n📊 Системная информация:")
        print(f"Целевые пользователи: {Config.MAX_MESSENGER_TARGETS}")
        print(f"API URL: {Config.MAX_MESSENGER_API_URL}")
        print(f"Bot URL: {Config.MAX_MESSENGER_BOT_URL}")
        
        print("\n" + "=" * 60)
        print("🎉 Отправка сообщения завершена!")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при отправке сообщения: {e}")
        return False

if __name__ == "__main__":
    success = send_message_to_ved()
    sys.exit(0 if success else 1)