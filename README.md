# UNIQUE VOICE BOT v2.2

🇷🇺 Русскоязычный голосовой бот для Telegram + Max Messenger

## 🚀 Быстрый старт

1. **Настройка окружения**:
```bash
cp .env.example .env
# Редактируйте .env с вашими данными
```

2. **Установка зависимостей**:
```bash
pip install -r requirements.txt
```

3. **Запуск**:
```bash
python unique_voice_bot_v2_2.py
```

## 🔒 Безопасность

- **Все персональные данные** работают исключительно через переменные окружения
- **Никаких токенов/паролей в коде**
- **.gitignore** блокирует все конфиденциальные файлы
- **Логирование** в отдельный файл

## 🎯 Функционал

- 🎤 Голосовые ↔ Текст (русский язык)
- 🔄 Интеграция Telegram + Max Messenger
- 📱 Дублирование сообщений между платформами
- 🇷🇺 Полная русификация
- 🔐 Безопасная конфигурация

## 📁 Структура

- `unique_voice_bot_v2_2.py` - Основной бот
- `test_max_connection.py` - Тест подключения
- `.env.example` - Шаблон конфигурации
- `.gitignore` - Защита данных
- `requirements.txt` - Зависимости

## ⚙️ Настройка

### Max Messenger
- `MAX_MESSENGER_API_URL` - API URL
- `MAX_MESSENGER_BOT_URL` - Бот URL
- `MAX_MESSENGER_TOKEN` - API токен
- `MAX_MESSENGER_TARGETS` - Целевые пользователи (через запятую)

### Telegram
- `TELEGRAM_BOT_TOKEN` - Токен бота
- `TELEGRAM_CHAT_ID` - ID чата

## 🛡️ Важно

- **Никогда** не коммитьте `.env` файл
- **Всегда** используйте `.env.example` для примеров
- **Переменные** чувствительны к регистру

## 📞 Поддержка

GitHub: https://github.com/VedMusatov/max-messenger-bot