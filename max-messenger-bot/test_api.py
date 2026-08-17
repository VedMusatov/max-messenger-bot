#!/usr/bin/env python3
"""
Тестовый скрипт для проверки Max Messenger API
"""

import sys
import os
import logging

# Добавляем src в путь для импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.max_messenger_api import MaxMessengerAPI
from src.config import Config

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_api():
    """Тестирование Max Messenger API"""
    print("🔍 Тестирование Max Messenger API")
    
    try:
        # Создаем экземпляр API
        api = MaxMessengerAPI()
        
        # Проверяем соединение
        print("🌐 Проверка соединения с API...")
        if api.test_connection():
            print("✅ Соединение установлено успешно")
        else:
            print("⚠️ Соединение не удалось")
        
        # Получаем информацию о API
        print("\n📋 Получение информации о API...")
        api_info = api.get_api_info()
        if api_info:
            print("✅ Информация о API получена:")
            print(f"   {api_info}")
        else:
            print("❌ Не удалось получить информацию о API")
        
        # Получаем информацию о боте
        print("\n🤖 Получение информации о боте...")
        bot_info = api.get_bot_info()
        if bot_info:
            print("✅ Информация о боте получена:")
            print(f"   {bot_info}")
        else:
            print("❌ Не удалось получить информацию о боте")
        
        # Тест отправки сообщения
        print("\n📤 Тест отправки сообщения...")
        test_message = "👋 Привет из тестового скрипта!"
        result = api.send_message(test_message)
        if result:
            print("✅ Сообщение отправлено успешно:")
            print(f"   {result}")
        else:
            print("❌ Не удалось отправить сообщение")
        
        # Тест получения обновлений
        print("\n🔄 Тест получения обновлений...")
        updates = api.get_updates()
        if updates:
            print("✅ Обновления получены:")
            print(f"   {updates}")
        else:
            print("❌ Не удалось получить обновления")
        
        print("\n🎉 Тестирование завершено!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        return False

if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1)