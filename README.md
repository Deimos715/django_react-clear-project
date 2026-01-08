# Django + React Starter (DRF + Vite)

Каркас full-stack приложения: backend на Django + DRF и frontend на React + Vite. В проекте уже подключены CORS, `robots.txt` и `sitemap.xml`, есть демо-API и базовые страницы фронта.

## Стек
- Backend: Django 5.2.7, DRF 3.16.1, django-cors-headers, django-robots, python-dotenv, gunicorn.
- Frontend: React 19.2.3, React Router 7.11.0, Vite 7.3.0, Sass (sass-embedded), ESLint, axios, @twa-dev/sdk.
- Инфраструктура: Docker (dev/prod), PostgreSQL 17.

## Структура
- `backend/` — Django-проект: `core` (settings/urls), `src/api` (DRF), `templates/admin`, `static`, Dockerfiles/Compose.
- `frontend/` — Vite/React: `src/pages`, `src/components`, `src/services`, `src/scss`.
- `README.md` — инструкции по запуску и деплою.

## Быстрый старт (локально)

### Backend
```bash
python -m venv .venv
. .venv/bin/activate      # Windows: .\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
cd backend
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
API: `http://localhost:8000/api/home/`, админка — `http://localhost:8000/auth/admin/`.

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Vite: `http://localhost:5173/`.

## Настройки и окружение
- Выбор окружения: `DJANGO_ENV=dev|prod` (см. `backend/core/settings/__init__.py`) или `DJANGO_SETTINGS_MODULE`.
- `python-dotenv` загружает переменные из `.env`. Для локального запуска используйте `backend/core/settings/.env` (пример — `backend/core/settings/.env.exemple`).
- Для Docker создайте `.env.dev` и `.env.prod` из `backend/core/settings/.env.*.exemple`.

### База данных
- По умолчанию используется SQLite (`backend/core/settings/base.py`).
- Для PostgreSQL (Docker) переключите блоки SQLite/PostgreSQL в `backend/core/settings/base.py` и заполните `DB_*` в `.env.*`.

### CORS
- В `backend/core/settings/dev.py` разрешён `http://localhost:5173`. Для других адресов добавьте их в `CORS_ALLOWED_ORIGINS`.

## API и маршруты
- `GET /api/home/` — тестовый эндпоинт (см. `backend/src/api/views.py`).
- `robots.txt` и `sitemap.xml` подключены в `backend/core/urls.py`.
- Фронт-роуты: `/home`, `/login`, `/account`, `/taplink`, `/help`, `*` → NotFound.

## Docker

### dev
```bash
cd backend
cp core/settings/.env.dev.exemple core/settings/.env.dev
docker compose -f docker-compose.dev.yml up --build
```
API: `http://localhost:8000/api/home/`, админка — `http://localhost:8000/auth/admin/`, PostgreSQL — `5439`.

### prod
```bash
cd backend
cp core/settings/.env.prod.exemple core/settings/.env.prod
docker compose -f docker-compose.prod.yml up -d
```
Перед запуском обновите image, порты и volume-монты в `backend/docker-compose.prod.yml`.

## Статика и медиа
```bash
cd backend
python manage.py collectstatic --noinput
```
- Статика: `backend/static/`, сборка — `backend/staticfiles/`.
- Медиа: `backend/media/`.

## Что стоит проверить/донастроить
- `backend/core/sitemaps.py` содержит карту с именем маршрута `main:index` — обновите под реальные URL.
- В `backend/docker-compose.prod.yml` healthcheck обращается к `/health` — добавьте эндпоинт или измените проверку.
- `frontend/src/services/home.js` использует фиксированный URL `http://localhost:8000/api/home/` — замените для другого окружения.

## Полезные файлы
- `backend/nginx/nginx-fastpanel-snippet.conf` — пример Nginx-конфига.
- `backend/github_ci-cd.zip` — заготовки GitHub Actions.
- `backend/deploy_my.sh` — пример деплоя (есть `git reset --hard`, используйте осторожно).
- `frontend/update-deps.sh`, `frontend/update-deps.cmd` — обновление зависимостей.
