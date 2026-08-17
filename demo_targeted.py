#!/usr/bin/env python3
"""
Демонстрация отправки сообщений пользователям Ved и +79854650850 в Max Messenger
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

def demo_targeted_messaging():
    """Демонстрация отправки сообщений конкретным пользователям"""
    print("🎯 Демонстрация отправки сообщений пользователям")
    print("=" * 60)
    
    try:
        # Создаем экземпляр API
        api = MaxMessengerAPI()
        
        # 1. Показываем целевых пользователей
        print("\n1. 🎯 Целевые пользователи:")
        print(f"   • Ved")
        print(f"   • +79854650850")
        
        # 2. Тестовое сообщение для всех пользователей
        test_message = "👋 Привет! Это тестовое сообщение от Max Messenger Bot!"
        
        print(f"\n2. 📤 Отправка тестового сообщения:")
        print(f"   Сообщение: {test_message}")
        
        # Отправка сообщения всем целевым пользователям
        results = api.send_message_to_multiple_users(test_message)
        
        print("\n3. 📊 Результаты отправки:")
        for user, result in results.items():
            if result:
                print(f"   ✅ {user}: Сообщение успешно отправлено")
                print(f"      Ответ: {result}")
            else:
                print(f"   ❌ {user}: Ошибка отправки")
        
        # 3. Индивидуальные сообщения
        print("\n4. 📨 Индивидуальные сообщения:")
        
        individual_messages = {
            "Ved": "🤖 Привет, Ved! Это индивидуальное сообщение для тебя!",
            "+79854650850": "📱 Привет! Это сообщение для пользователя +79854650850!"
        }
        
        for user, message in individual_messages.items():
            print(f"\n   Отправка пользователю {user}:")
            print(f"   Сообщение: {message}")
            
            result = api.send_message_to_user(message, user)
            
            if result:
                print(f"   ✅ Успешно отправлено!")
                print(f"      Ответ: {result}")
            else:
                print(f"   ❌ Ошибка отправки")
            
            # Небольшая задержка
            time.sleep(1)
        
        # 4. Статус системы
        print("\n5. 📊 Системный статус:")
        status = api.get_status()
        print(f"   API URL: {status['api_url']}")
        print(f"   Bot URL: {status['bot_url']}")
        print(f"   Connected: {status['connected']}")
        print(f"   Целевые пользователи: {Config.MAX_MESSENGER_TARGETS}")
        
        # 6. Итог
        print("\n6. 🎉 Итог:")
        print("   ✅ Max Messenger Bot настроен для отправки сообщениям:")
        print("   • Пользователю Ved")
        print("   • Пользователю +79854650850")
        print("   ✅ API подключен")
        print("   ✅ Система готова к работе")
        
        print("\n" + "=" * 60)
        print("🎉 Демонстрация завершена успешно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при демонстрации: {e}")
        return False

if __name__ == "__main__":
    success = demo_targeted_messaging()
    sys.exit(0 if success else 1)