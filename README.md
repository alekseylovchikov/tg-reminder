# TG Reminder Bot

Telegram-бот с Mini App для создания и получения напоминаний.

## Структура

```
backend/       — Python: бот, API, планировщик, БД
frontend/      — React Mini App (Vite + TypeScript)
tests/         — pytest-тесты
```

## Быстрый старт

### 1. Зависимости

```bash
pip3 install -r requirements.txt
cd frontend && npm install && npm run build && cd ..
```

### 2. Конфигурация

```bash
cp .env.example .env
```

Заполни `.env`:
- `BOT_TOKEN` — токен от [@BotFather](https://t.me/BotFather)
- `WEBAPP_URL` — публичный HTTPS-адрес, где доступен Mini App (например, через ngrok)

### 3. Запуск

```bash
python3 -m backend.main
```

Бот начнёт polling, API-сервер запустится на порту 8080, планировщик будет проверять напоминания каждые 30 секунд.

### Разработка фронтенда

```bash
cd frontend && npm run dev
```

Vite проксирует `/api` запросы на `localhost:8080`.

### Тесты

```bash
python3 -m pytest tests/ -v
```

## HTTPS для Mini App

Telegram требует HTTPS для Web App. Для разработки:

```bash
ngrok http 8080
```

Полученный URL (например `https://xxxx.ngrok.io`) укажи в `WEBAPP_URL` в `.env`.

## Переменные окружения

| Переменная | Обязательная | По умолчанию | Описание |
|---|---|---|---|
| `BOT_TOKEN` | да | — | Токен Telegram-бота |
| `WEBAPP_URL` | да | — | Публичный URL Mini App |
| `DB_PATH` | нет | `reminders.db` | Путь к SQLite файлу |
| `API_PORT` | нет | `8080` | Порт API-сервера |
| `SCHEDULER_INTERVAL` | нет | `30` | Интервал проверки напоминаний (сек) |
