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

Бот начнёт polling, API-сервер запустится на порту 8080, планировщик будет проверять просроченные напоминания каждые 60 секунд.

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

## Деплой на Railway

### 1. Подготовка

- Аккаунт на [Railway](https://railway.app)
- Репозиторий в GitHub/GitLab
- MongoDB Atlas (бесплатный кластер на [mongodb.com](https://www.mongodb.com/atlas))

### 2. Создание проекта

1. В дашборде Railway нажми **New Project → Deploy from GitHub Repo**
2. Выбери репозиторий с ботом
3. Railway автоматически подхватит `railway.json` — билд (Python + Node.js) и старт-команда настроены

### 3. Переменные окружения

В настройках сервиса (**Variables**) добавь:

| Переменная | Значение |
|---|---|
| `BOT_TOKEN` | Токен от [@BotFather](https://t.me/BotFather) |
| `WEBAPP_URL` | `https://<твой-сервис>.up.railway.app` |
| `MONGO_URI` | Connection string из MongoDB Atlas |
| `MONGO_DB` | `tg_reminder` (или своё имя базы) |

`PORT` назначается Railway автоматически — бэкенд его подхватывает.

### 4. Домен

1. Перейди в **Settings → Networking → Public Networking**
2. Нажми **Generate Domain** — получишь URL вида `https://xxx.up.railway.app`
3. Этот URL используй как `WEBAPP_URL`

### 5. Редеплой

При каждом пуше в основную ветку Railway автоматически пересобирает и деплоит сервис.

---

## Переменные окружения

| Переменная | Обязательная | По умолчанию | Описание |
|---|---|---|---|
| `BOT_TOKEN` | да | — | Токен Telegram-бота |
| `WEBAPP_URL` | да | `http://localhost:5173` | Публичный URL Mini App |
| `MONGO_URI` | нет | `mongodb://localhost:27017` | URI подключения к MongoDB |
| `MONGO_DB` | нет | `tg_reminder` | Имя базы данных |
| `API_PORT` | нет | `8080` | Порт API-сервера |
| `PORT` | нет | — | Порт от PaaS (Railway и др.), приоритетнее `API_PORT` |
| `PROXY_URL` | нет | — | HTTP-прокси для Telegram API |
| `CONNECT_TIMEOUT` | нет | `30` | Таймаут подключения (сек) |
| `READ_TIMEOUT` | нет | `30` | Таймаут чтения (сек) |
