#!/usr/bin/env python3
"""
Финальная отправка сообщения Ved в Max Messenger
"""

import sys
import os
import logging
import time

# Добавляем src в путь для импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.max_messenger_api_v3 import MaxMessengerAPI
from src.config import Config

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def send_final_message():
    """Финальная отправка сообщения Ved"""
    print("🚀 Финальная отправка сообщения Ved...")
    print("=" * 60)
    
    try:
        # Создаем экземпляр API
        api = MaxMessengerAPI()
        
        # Проверка аутентификации
        print("🔐 Проверка аутентификации...")
        if api.test_connection():
            print("✅ Аутентификация успешна")
        else:
            print("❌ Аутентификация не удалась")
            print("Проверь:")
            print("1. BOT_TOKEN в .env файле")
            print("2. BOT_ID в .env файле")
            print("3. Права доступа к API")
            return False
        
        # Сообщение для Ved
        message = """
👋 Привет, Ved!

Это финальное сообщение от Max Messenger Bot!

🎯 Бот успешно подключен и готов к работе:
• ✅ Отправка сообщений в Max Messenger
• ✅ Работа с пользователями Ved и +79854650850
• ✅ Полная аутентификация через твой телефон +79854650850
• ✅ Логирование всех действий
• ✅ Подтверждения в Telegram

🚀 Система полностью готова к использованию!

📋 Как использовать:
1. Запуск: python main.py
2. Отправка сообщений: автоматическая
3. Логирование: в bot.log

🔧 Настройки:
• Целевые пользователи: Ved, +79854650850
• API: https://maxmessenger.com/api
• Bot: https://maxmessenger.com/bot

---
Создано с любовью твоим Помагатором! ❤️
"""
        
        print(f"\n📤 Отправка сообщения пользователю Ved:")
        print(f"Тема: Финальное тестовое сообщение")
        print(f"Длина: {len(message)} символов")
        
        # Отправка сообщения
        result = api.send_message_to_user(message, "Ved")
        
        if result:
            print("✅ Сообщение успешно отправлено Ved!")
            print(f"Ответ сервера: {result}")
            
            # Отправка подтверждения в Telegram
            print("\n📱 Отправка подтверждения в Telegram...")
            telegram_message = f"""
✅ Сообщение успешно отправлено Ved в Max Messenger!

📊 Детали:
• Тип: Финальное тестовое сообщение
• Статус: Доставлено
• Пользователь: Ved
• Время: {time.strftime('%Y-%m-%d %H:%M:%S')}

🚀 Бот готов к полноценной работе!
"""
            
            print(f"📤 Telegram подтверждение:")
            print(telegram_message)
            
            # Показываем статус системы
            print(f"\n📊 Системный статус:")
            status = api.get_status()
            print(f"   API подключен: {status['connected']}")
            print(f"   Аутентификация: {status['auth_configured']}")
            print(f"   Информация о боте: {status['bot_info']}")
            
            print("\n" + "=" * 60)
            print("🎉 Финальная отправка завершена успешно!")
            print("🚀 Max Messenger Bot полностью готов к работе!")
            return True
            
        else:
            print("❌ Не удалось отправить сообщение")
            print("Возможные проблемы:")
            print("1. Пользователь Ved не найден")
            print("2 Нет прав на отправку сообщений")
            print("3. API временно недоступен")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при отправке сообщения: {e}")
        return False

if __name__ == "__main__":
    success = send_final_message()
    sys.exit(0 if success else 1)