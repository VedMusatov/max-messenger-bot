import requests
import json
import logging
from typing import Dict, Any, Optional
from .config import Config

logger = logging.getLogger(__name__)

class MaxMessengerAPI:
    """API клиент для Max Messenger"""
    
    def __init__(self):
        self.api_url = Config.MAX_MESSENGER_API_URL
        self.bot_url = Config.MAX_MESSENGER_BOT_URL
        self.session = requests.Session()
        
        # Заголовки для запросов
        self.headers = {
            'User-Agent': 'MaxMessengerBot/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def get_api_info(self) -> Optional[Dict[str, Any]]:
        """Получение информации о API"""
        try:
            response = self.session.get(self.api_url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                # Проверяем, есть ли JSON ответ
                try:
                    return response.json()
                except json.JSONDecodeError:
                    # Если не JSON, возвращаем текст
                    return {'status': 'success', 'content': response.text[:500]}
            else:
                logger.error(f"API info request failed: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting API info: {e}")
            return None
    
    def get_bot_info(self) -> Optional[Dict[str, Any]]:
        """Получение информации о боте"""
        try:
            response = self.session.get(self.bot_url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                try:
                    return response.json()
                except json.JSONDecodeError:
                    return {'status': 'success', 'content': response.text[:500]}
            else:
                logger.error(f"Bot info request failed: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting bot info: {e}")
            return None
    
    def send_message(self, message: str, chat_id: str = None) -> Optional[Dict[str, Any]]:
        """Отправка сообщения"""
        try:
            payload = {
                'message': message,
                'bot_name': Config.BOT_NAME
            }
            
            if chat_id:
                payload['chat_id'] = chat_id
            
            response = self.session.post(
                f"{self.bot_url}/send",
                json=payload,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Send message failed: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return None
    
    def get_updates(self) -> Optional[Dict[str, Any]]:
        """Получение обновлений от бота"""
        try:
            response = self.session.get(
                f"{self.bot_url}/updates",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Get updates failed: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting updates: {e}")
            return None
    
    def test_connection(self) -> bool:
        """Тестовое соединение с API"""
        try:
            info = self.get_api_info()
            if info:
                logger.info("✅ Max Messenger API connection successful")
                return True
            else:
                logger.warning("⚠️ Max Messenger API connection failed")
                return False
                
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False