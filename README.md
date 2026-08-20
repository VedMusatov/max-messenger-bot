# Hermes Bridge Bot

AI-бот-мост между Telegram и MAX мессенджером. Сообщения из обеих платформ обрабатываются AI-агентом (Hermes) и синхронизируются.

## Быстрый старт

```bash
cp .env.example .env
# Заполните .env своими токенами
pip install -r requirements.txt
python main.py
```

## Docker

```bash
docker-compose up --build
```

## Конфигурация (.env)

| Переменная | Описание |
|-----------|----------|
| `TELEGRAM_BOT_TOKEN` | Токен Telegram-бота (от @BotFather) |
| `MAX_BOT_TOKEN` | Токен MAX-бота (с business.max.ru) |
| `HERMES_PROVIDER` | AI провайдер: `openrouter`, `openai`, `claude`, `local` |
| `HERMES_API_KEY` | API ключ провайдера |
| `HERMES_MODEL` | Модель AI |

## Провайдеры AI

- **openrouter** — агрегатор моделей (OpenAI-совместимый)
- **openai** — напрямую OpenAI API
- **claude** — Anthropic Claude API
- **local** — локальный сервер (Ollama, LM Studio, etc.)

## Архитектура

```
Telegram → Bot → Hermes AI → ответ → Telegram + MAX
MAX → Bot → Hermes AI → ответ → MAX + Telegram
```

## Структура

```
├── main.py            # Точка входа
├── src/
│   ├── config.py      # Конфигурация
│   ├── max_api.py     # MAX API клиент
│   ├── telegram_bot.py # Telegram бот
│   ├── hermes_agent.py # AI-агент
│   └── sync.py        # Синхронизация
├── .env.example       # Шаблон
├── Dockerfile
└── docker-compose.yml
```
