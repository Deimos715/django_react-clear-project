## Django React Clear Project

Подготовленный каркас для full-stack приложения: backend на Django 5 и frontend на React 19 с Vite 7. Репозиторий подходит для быстрого развёртывания, экспериментов и последующей интеграции в production.

## Структура
- `backend/` — Django-проект (`core`, `main`, `seo`), шаблоны, статические файлы и скрипт деплоя.
- `frontend/` — React/Vite-приложение со страницами, компонентами и SCSS.
- `.gitignore`, `frontend/.gitignore` — базовые правила игнорирования артефактов и секретов.

---

## Backend (Django)

**Зависимости и конфигурация**
- Список пакетов в `backend/requirements.txt` (Django 5.2.7, asgiref, django-robots, python-dotenv и др.).
- Точка входа — `backend/manage.py`.
- Настройки разбиты на модули: `core/settings/base.py`, `core/settings/dev.py`, `core/settings/prod.py`. Файл-пример подключения настроек — `backend/settings.exemple.py`.
- Для переменных окружения используйте шаблон `backend/core/settings/.env.exemple`.

**Быстрый старт**
```bash
python -m venv .venv
. .venv/Scripts/activate        # Windows PowerShell: .\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
cd backend
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**Статика и медиа**
```bash
python manage.py collectstatic --noinput
```
Статические ресурсы по умолчанию лежат в `backend/static/`, шаблоны — в `backend/templates/`.

**Переменные окружения**
- Для разработки достаточно `core.settings.dev`.
- Для production установите `DJANGO_SETTINGS_MODULE=core.settings.prod` и заполните `.env` (SECRET_KEY, настройки БД, DEBUG=False, email, Sentry и т.д.).

---

## Frontend (React + Vite)

**Что внутри**
- Vite 7, React 19, React Router v7, SCSS, ESLint (см. `frontend/package.json`).
- Точка входа — `frontend/src/main.jsx`, маршруты описаны в `frontend/src/App.jsx`.
- Компоненты (`frontend/src/components/`), страницы (`frontend/src/pages/`), стили (`frontend/src/scss/`).
- Для обновления зависимостей есть `frontend/update-deps.cmd` и `frontend/update-deps.sh`.

**Быстрый старт**
```bash
cd frontend
npm install
npm run dev
```
После запуска приложение доступно на `http://localhost:5173/` с поддержкой HMR.

**Скрипты npm**
- `npm run dev` — режим разработки.
- `npm run build` — сборка в `frontend/dist`.
- `npm run preview` — локальный предпросмотр собранной версии.
- `npm run lint` — проверка ESLint.

---

## Деплой и рекомендации
- Проверьте `backend/deploy_my.sh` — можно адаптировать под вашу инфраструктуру.
- Для production:
  - переключитесь на `core.settings.prod`;
  - настройте переменные окружения (SECRET_KEY, DEBUG=False, внешняя БД, провайдер почты);
  - используйте внешнюю СУБД (PostgreSQL/MySQL) вместо SQLite;
  - соберите фронтенд (`npm run build`) и выполните `collectstatic`, чтобы все assets попали в `STATIC_ROOT`;
  - настройте сервер приложений (gunicorn/uvicorn + nginx, systemd/supervisor).

---

## Быстрые команды
```bash
# Backend
python -m venv .venv
. .venv/Scripts/activate        # или source .venv/bin/activate на Linux/Mac
pip install -r backend/requirements.txt
cd backend
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
python manage.py collectstatic --noinput

# Frontend
cd frontend
npm install
npm run dev
npm run build
npm run preview
npm run lint
```
