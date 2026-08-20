import logging
import requests
from typing import Optional, List

from .config import Config

logger = logging.getLogger(__name__)

PROVIDERS = {
    "openrouter": {
        "url": "https://openrouter.ai/api/v1/chat/completions",
        "key_prefix": "Bearer ",
    },
    "openai": {
        "url": "https://api.openai.com/v1/chat/completions",
        "key_prefix": "Bearer ",
    },
    "claude": {
        "url": "https://api.anthropic.com/v1/messages",
        "key_prefix": "x-api-key: ",
    },
    "local": {
        "url": "",  # set from HERMES_LOCAL_URL
        "key_prefix": "Bearer ",
    },
}


class HermesAgent:
    def __init__(self):
        self.provider = Config.HERMES_PROVIDER
        self.api_key = Config.HERMES_API_KEY
        self.model = Config.HERMES_MODEL
        self.history = {}  # chat_id -> list of messages
        self.system_prompt = (
            "Ты — AI-ассистент Hermes. Ты общаешься с пользователем через "
            "Telegram и MAX мессенджеры. Отвечай на русском языке, "
            "кратко и по делу. Если сообщение короткое — ответь коротко."
        )

    def _get_url(self) -> str:
        if self.provider == "local":
            return Config.HERMES_LOCAL_URL + "/chat/completions"
        info = PROVIDERS.get(self.provider)
        if not info:
            raise ValueError(f"Unknown provider: {self.provider}")
        return info["url"]

    def _get_headers(self) -> dict:
        if self.provider == "claude":
            return {
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            }
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def chat(self, chat_id: str, user_text: str) -> str:
        """Send message to AI and get response"""
        if not self.api_key and self.provider != "local":
            return "[AI not configured — set HERMES_API_KEY]"

        chat_key = str(chat_id)
        if chat_key not in self.history:
            self.history[chat_key] = []

        self.history[chat_key].append({"role": "user", "content": user_text})

        if len(self.history[chat_key]) > 20:
            self.history[chat_key] = self.history[chat_key][-20:]

        try:
            if self.provider == "claude":
                return self._call_claude(chat_key)
            else:
                return self._call_openai_compatible(chat_key)
        except Exception as e:
            logger.error(f"Hermes error: {e}")
            self.history[chat_key].pop()
            return f"[AI error: {e}]"

    def _call_openai_compatible(self, chat_key: str) -> str:
        url = self._get_url()
        headers = self._get_headers()
        messages = [{"role": "system", "content": self.system_prompt}] + self.history[chat_key]

        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 1024,
            "temperature": 0.7,
        }

        r = requests.post(url, headers=headers, json=payload, timeout=30)
        if r.status_code == 200:
            data = r.json()
            reply = data["choices"][0]["message"]["content"].strip()
            self.history[chat_key].append({"role": "assistant", "content": reply})
            return reply
        else:
            logger.error(f"AI API {r.status_code}: {r.text[:200]}")
            return f"[AI API error {r.status_code}]"

    def _call_claude(self, chat_key: str) -> str:
        url = self._get_url()
        headers = self._get_headers()
        messages = self.history[chat_key]

        payload = {
            "model": self.model,
            "max_tokens": 1024,
            "system": self.system_prompt,
            "messages": messages,
        }

        r = requests.post(url, headers=headers, json=payload, timeout=30)
        if r.status_code == 200:
            data = r.json()
            reply = data["content"][0]["text"].strip()
            self.history[chat_key].append({"role": "assistant", "content": reply})
            return reply
        else:
            logger.error(f"Claude API {r.status_code}: {r.text[:200]}")
            return f"[AI API error {r.status_code}]"

    def clear_history(self, chat_id: str):
        self.history.pop(str(chat_id), None)
