import requests
import json
import logging
import time
from typing import Dict, Any, Optional
from .config import Config

logger = logging.getLogger(__name__)

class MaxMessengerAPI:
    """Улучшенный API клиент для Max Messenger"""
    
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
        
        # Токен аутентификации (если будет нужен)
        self.auth_token = None
        
        # Повторные попытки
        self.max_retries = 3
        self.retry_delay = 2
    
    def _make_request(self, method: str, url: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Вспомогательный метод для запросов с повторными попытками"""
        for attempt in range(self.max_retries):
            try:
                response = self.session.request(method, url, headers=self.headers, **kwargs)
                
                if response.status_code == 200:
                    try:
                        return response.json()
                    except json.JSONDecodeError:
                        return {'status': 'success', 'content': response.text[:500]}
                elif response.status_code == 401:
                    logger.error("Authentication required")
                    return None
                elif response.status_code == 404:
                    logger.error("Endpoint not found")
                    return None
                elif response.status_code == 405:
                    logger.error("Method not allowed")
                    return None
                else:
                    logger.warning(f"Request failed: {response.status_code}")
                    
            except Exception as e:
                logger.error(f"Request attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    
        return None
    
    def get_api_info(self) -> Optional[Dict[str, Any]]:
        """Получение информации о API"""
        return self._make_request('GET', self.api_url)
    
    def get_bot_info(self) -> Optional[Dict[str, Any]]:
        """Получение информации о боте"""
        return self._make_request('GET', self.bot_url)
    
    def send_message(self, message: str, chat_id: str = None) -> Optional[Dict[str, Any]]:
        """Отправка сообщения"""
        payload = {
            'message': message,
            'bot_name': Config.BOT_NAME,
            'timestamp': int(time.time())
        }
        
        if chat_id:
            payload['chat_id'] = chat_id
        
        return self._make_request('POST', f"{self.bot_url}/send", json=payload)
    
    def send_message_to_user(self, message: str, user: str) -> Optional[Dict[str, Any]]:
        """Отправка сообщения конкретному пользователю"""
        try:
            payload = {
                'message': message,
                'bot_name': Config.BOT_NAME,
                'target_user': user,
                'timestamp': int(time.time())
            }
            
            response = self._make_request('POST', f"{self.bot_url}/send_to_user", json=payload)
            
            if response:
                logger.info(f"Message sent to {user}: {message}")
                return response
            else:
                logger.error(f"Failed to send message to {user}")
                return None
                
        except Exception as e:
            logger.error(f"Error sending message to {user}: {e}")
            return None
    
    def send_message_to_multiple_users(self, message: str, users: list = None) -> Dict[str, Any]:
        """Отправка сообщения нескольким пользователям"""
        if users is None:
            users = Config.MAX_MESSENGER_TARGETS
        
        results = {}
        
        for user in users:
            result = self.send_message_to_user(message, user)
            results[user] = result
        
        return results
    
    def get_updates(self) -> Optional[Dict[str, Any]]:
        """Получение обновлений от бота"""
        return self._make_request('GET', f"{self.bot_url}/updates")
    
    def test_connection(self) -> bool:
        """Тестовое соединение с API"""
        info = self.get_api_info()
        return info is not None
    
    def get_status(self) -> Dict[str, Any]:
        """Получение статуса API"""
        return {
            'api_url': self.api_url,
            'bot_url': self.bot_url,
            'connected': self.test_connection(),
            'api_info': self.get_api_info(),
            'bot_info': self.get_bot_info()
        }
    
    def simulate_message(self, message: str) -> Dict[str, Any]:
        """Имитация отправки сообщения для тестирования"""
        logger.info(f"Simulating message: {message}")
        
        # Возвращаем имитированный ответ
        return {
            'success': True,
            'message': message,
            'timestamp': int(time.time()),
            'bot_response': f"Echo: {message}",
            'simulated': True
        }