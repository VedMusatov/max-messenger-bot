import os
import time
import logging
import threading
import requests
from typing import Optional, Callable

from .config import Config

logger = logging.getLogger(__name__)

# SSL certificate for platform-api2.max.ru (Russian MinTsifry CA)
_CERT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "certs")
_CERT_FILE = os.path.join(_CERT_DIR, "mintrusted_root_ca.pem")


def _find_cert():
    if os.path.isfile(_CERT_FILE):
        return _CERT_FILE
    return True


class MaxAPI:
    """Real MAX Messenger API client (platform-api2.max.ru)"""

    def __init__(self):
        self.base_url = Config.MAX_API_BASE
        self.token = Config.MAX_BOT_TOKEN
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": self.token,
            "Content-Type": "application/json",
        })
        self.verify = _find_cert()
        self._polling = False
        self._marker = None
        self._on_message = None

    def get_me(self) -> Optional[dict]:
        """GET /me - info about the bot"""
        try:
            r = self.session.get(f"{self.base_url}/me", timeout=10, verify=self.verify)
            if r.status_code == 200:
                data = r.json()
                logger.info(f"MAX bot: {data.get('first_name')} (@{data.get('username')}) id={data.get('user_id')}")
                return data
            logger.error(f"MAX /me failed: {r.status_code} {r.text[:200]}")
        except Exception as e:
            logger.error(f"MAX /me error: {e}")
        return None

    def send_message(self, user_id: int, text: str, format: str = None) -> Optional[dict]:
        """POST /messages - send message to user"""
        try:
            payload = {"text": text}
            if format:
                payload["format"] = format
            r = self.session.post(
                f"{self.base_url}/messages",
                params={"user_id": user_id},
                json=payload,
                timeout=10,
                verify=self.verify,
            )
            if r.status_code == 200:
                logger.info(f"MAX -> user {user_id}: sent ({len(text)} chars)")
                return r.json()
            logger.error(f"MAX send failed: {r.status_code} {r.text[:200]}")
        except Exception as e:
            logger.error(f"MAX send error: {e}")
        return None

    def send_to_chat(self, chat_id: int, text: str, format: str = None) -> Optional[dict]:
        """POST /messages - send message to chat/channel"""
        try:
            payload = {"text": text}
            if format:
                payload["format"] = format
            r = self.session.post(
                f"{self.base_url}/messages",
                params={"chat_id": chat_id},
                json=payload,
                timeout=10,
                verify=self.verify,
            )
            if r.status_code == 200:
                logger.info(f"MAX -> chat {chat_id}: sent ({len(text)} chars)")
                return r.json()
            logger.error(f"MAX send_to_chat failed: {r.status_code} {r.text[:200]}")
        except Exception as e:
            logger.error(f"MAX send_to_chat error: {e}")
        return None

    def get_updates(self, marker=None, timeout=30, types=None) -> Optional[dict]:
        """GET /updates - long polling"""
        try:
            params = {"timeout": timeout}
            if marker is not None:
                params["marker"] = marker
            if types:
                params["types"] = ",".join(types)
            r = self.session.get(
                f"{self.base_url}/updates",
                params=params,
                timeout=timeout + 10,
                verify=self.verify,
            )
            if r.status_code == 200:
                return r.json()
            logger.error(f"MAX /updates failed: {r.status_code} {r.text[:200]}")
        except Exception as e:
            logger.error(f"MAX /updates error: {e}")
        return None

    def start_polling(self, on_message: Callable):
        """Start long polling in background thread"""
        self._on_message = on_message
        self._polling = True
        t = threading.Thread(target=self._poll_loop, daemon=True, name="max-polling")
        t.start()
        logger.info("MAX polling started")

    def stop_polling(self):
        self._polling = False
        logger.info("MAX polling stopped")

    def _poll_loop(self):
        while self._polling:
            try:
                data = self.get_updates(marker=self._marker, timeout=30)
                if data and "updates" in data:
                    self._marker = data.get("marker")
                    for update in data["updates"]:
                        self._handle_update(update)
                else:
                    time.sleep(1)
            except Exception as e:
                logger.error(f"MAX poll loop error: {e}")
                time.sleep(5)

    def _handle_update(self, update: dict):
        update_type = update.get("update_type")
        if update_type not in ("message_created", "bot_started", "bot_added"):
            logger.debug(f"MAX update ignored: {update_type}")
            return

        if update_type in ("bot_started", "bot_added"):
            user = update.get("user", {})
            chat_id = update.get("chat_id")
            logger.info(f"MAX: bot started/added by {user.get('first_name')} (chat={chat_id})")
            if self._on_message:
                self._on_message({
                    "platform": "max",
                    "type": "start",
                    "chat_id": chat_id,
                    "user": user,
                    "text": "",
                })
            return

        if update_type == "message_created":
            msg = update.get("message", {})
            sender = msg.get("sender", {})
            recipient = msg.get("recipient", {})
            body = msg.get("body", {})
            text = body.get("text", "")

            sender_id = sender.get("id") if isinstance(sender, dict) else sender
            chat_id = recipient.get("chat_id") if isinstance(recipient, dict) else None

            if sender.get("is_bot"):
                return

            if self._on_message:
                self._on_message({
                    "platform": "max",
                    "type": "message",
                    "chat_id": chat_id,
                    "sender_id": sender_id,
                    "user": sender,
                    "text": text,
                    "message": msg,
                })
