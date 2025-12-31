# Django React Clear Project

Каркас full-stack приложения: backend на Django 5.2 + DRF и frontend на React 19/Vite 7. В backend уже подключены robots.txt, sitemap.xml и SEO-модуль с базовыми шаблонами.

## Стек
- Backend: Django 5.2, Django REST Framework, django-robots, python-dotenv, gunicorn.
- Frontend: React 19, React Router 7, Vite 7, Sass, ESLint.
- Инфраструктура: Docker (dev/prod), PostgreSQL 17.

## Структура
- `backend/` — Django-проект (`core`, `src/main`, `src/seo`, `src/api`), шаблоны, статика, Dockerfile/Compose, Nginx-сниппет.
- `frontend/` — React/Vite-приложение со страницами, компонентами и SCSS.
- `README.md` — инструкции по запуску и деплою.

---

## Backend (Django)

**Настройки**
- `backend/core/settings/base.py`, `dev.py`, `prod.py`.
- Выбор окружения через `DJANGO_ENV=dev|prod` (по умолчанию `dev`) или `DJANGO_SETTINGS_MODULE`.
- Примеры переменных окружения лежат в `backend/core/settings/.env.exemple`, `.env.dev.exemple`, `.env.prod.exemple`.
- Для Docker создайте файлы `backend/core/settings/.env.dev` и `backend/core/settings/.env.prod` на основе примеров.

**База данных**
- SQLite используется по умолчанию в `backend/core/settings/base.py`.
- Для PostgreSQL закомментируйте блок SQLite и раскомментируйте блок PostgreSQL в `backend/core/settings/base.py`.

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
- `frontend/src/scss/` — стили.

Для обновления зависимостей есть скрипты `frontend/update-deps.sh` и `frontend/update-deps.cmd`.

---

## Деплой и полезные файлы
- `backend/deploy_my.sh` — пример скрипта деплоя (внутри есть `git reset --hard`, используйте аккуратно).
- `backend/nginx/nginx-fastpanel-snippet.conf` — пример конфигурации внешнего Nginx (FastPanel).
