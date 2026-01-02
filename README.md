# Django React Clear Project

Каркас full-stack приложения: backend на Django 5.2.7 + DRF 3.16.1 и frontend на React 19.2/Vite 7.3.
В backend уже подключены robots.txt, sitemap.xml и SEO-модуль с базовыми шаблонами.

## Стек
- Backend: Django 5.2.7, Django REST Framework 3.16.1, django-robots, python-dotenv, gunicorn, django-cors-headers (подключён в настройках).
- Frontend: React 19.2.3, React Router 7.11.0, Vite 7.3.0, Sass (sass-embedded), ESLint, axios, @twa-dev/sdk.
- Инфраструктура: Docker (dev/prod), PostgreSQL 17.

## Структура
- `backend/` — Django-проект (`core`, `src/main`, `src/seo`, `src/api`), шаблоны, статика, Dockerfile/Compose, Nginx-сниппет.
- `frontend/` — React/Vite-приложение со страницами, компонентами, сервисами API и SCSS.
- `README.md` — инструкции по запуску и деплою.

---

## Backend (Django)

**Настройки и окружение**
- `backend/core/settings/base.py`, `dev.py`, `prod.py`.
- Выбор окружения через `DJANGO_ENV=dev|prod` (по умолчанию `dev`) или `DJANGO_SETTINGS_MODULE`.
- Примеры переменных окружения: `backend/core/settings/.env.exemple`, `.env.dev.exemple`, `.env.prod.exemple`.
- Для локального запуска используйте `backend/core/settings/.env` (можно создать из `.env.exemple`).
- Для Docker создайте `backend/core/settings/.env.dev` и `backend/core/settings/.env.prod` на основе примеров.

**База данных**
- SQLite используется по умолчанию в `backend/core/settings/base.py`.
- Для PostgreSQL закомментируйте блок SQLite и раскомментируйте блок PostgreSQL в `backend/core/settings/base.py`.

**API и интеграция**
- DRF подключен в `backend/src/api`.
- Пример эндпоинта: `GET /api/home/` → `{"message": "Главная страница"}`.
- В `backend/core/settings/dev.py` уже разрешён CORS для `http://localhost:5173` (Vite).

**Локальный запуск (SQLite)**
```bash
python -m venv .venv
. .venv/Scripts/activate        # Windows PowerShell: .\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
cd backend
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Проект доступен на `http://localhost:8000/`, админка — `http://localhost:8000/auth/admin/`.

**Статика и медиа**
```bash
python manage.py collectstatic --noinput
```
Статика по умолчанию в `backend/static/`, собранные файлы — в `backend/staticfiles/`, медиа — в `backend/media/`.

**Docker (dev)**
```bash
cd backend
cp core/settings/.env.dev.exemple core/settings/.env.dev
docker compose -f docker-compose.dev.yml up --build
```
Django будет слушать `http://localhost:8000/`, PostgreSQL — на порту `5439`.

**Docker (prod)**
```bash
cd backend
cp core/settings/.env.prod.exemple core/settings/.env.prod
docker compose -f docker-compose.prod.yml up -d
```
Перед запуском обновите образ, порты и volume-монты в `backend/docker-compose.prod.yml` под вашу инфраструктуру.
В compose есть healthcheck на `http://127.0.0.1:8000/health` — добавьте эндпоинт или поправьте проверку под себя.

**SEO и вспомогательные модули**
- `robots.txt` и `sitemap.xml` уже подключены в `backend/core/urls.py`.
- Инструкции по SEO-модулю — в `backend/src/seo/README.md`.

---

## Frontend (React + Vite)

**Быстрый старт**
```bash
cd frontend
npm install
npm run dev
```
После запуска приложение доступно на `http://localhost:5173/` с HMR.

**Маршруты**
- `/home`, `/login`, `/account`, `/taplink`, `/help`.
- `*` — страница `NotFound`.

**Интеграция с backend**
- Запросы к API вынесены в `frontend/src/services/home.js` и используют `axios`.
- Базовый URL сейчас захардкожен на `http://localhost:8000/api/home/` — при другом адресе backend обновите сервис.

**Скрипты npm**
- `npm run dev` — режим разработки.
- `npm run build` — сборка в `frontend/dist`.
- `npm run preview` — локальный предпросмотр собранной версии.
- `npm run lint` — проверка ESLint.

**Структура**
- `frontend/src/main.jsx` — точка входа.
- `frontend/src/App.jsx` — маршрутизация.
- `frontend/src/components/` — переиспользуемые компоненты.
- `frontend/src/pages/` — страницы.
- `frontend/src/services/` — запросы к API.
- `frontend/src/scss/` — стили.

Для обновления зависимостей есть скрипты `frontend/update-deps.sh` и `frontend/update-deps.cmd`.

---

## Деплой и полезные файлы
- `backend/deploy_my.sh` — пример скрипта деплоя (внутри есть `git reset --hard`, используйте аккуратно).
- `backend/nginx/nginx-fastpanel-snippet.conf` — пример конфигурации внешнего Nginx (FastPanel).
- `backend/github_ci-cd.zip` — примеры GitHub Actions (`ci.yml`, `deploy.yml`).
