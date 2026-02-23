# Django + React Starter (DRF + Vite)

Full-stack шаблон: backend на Django + DRF, frontend на React + Vite, запуск через Docker (dev/prod).

## Стек
- Backend: Python 3.12, Django 6.0.2, DRF 3.16.1, SimpleJWT, Gunicorn.
- Frontend: React 19, React Router 7, Vite 7, Sass.
- Инфраструктура: Docker Compose, PostgreSQL 17, Nginx (для frontend prod-образа).

## Актуальная структура
- `docker-compose.dev.yml` — локальная разработка (backend + frontend + postgres).
- `docker-compose.prod.yml` — production-схема (backend image + frontend image + postgres).
- `backend/` — Django-проект и Dockerfile’ы backend.
- `frontend/` — React-проект и Dockerfile’ы frontend.
- `backend/core/settings/.env.dev` и `backend/core/settings/.env.prod` — env для Docker.

## Важно про настройки
- Проект сейчас настроен на PostgreSQL в `backend/core/settings/base.py`.
- Для Docker используются:
  - `backend/core/settings/.env.dev`
  - `backend/core/settings/.env.prod`
- Для ссылок активации/редиректов обязательно задайте:
  - `FRONTEND_URL=http://localhost:5173` (dev)
  - `FRONTEND_URL=https://ваш-домен` (prod)

## Запуск в Docker (dev)

1. Создайте env-файл:
```bash
cp backend/core/settings/.env.dev.exemple backend/core/settings/.env.dev
```

2. Заполните переменные в `backend/core/settings/.env.dev`:
- `SECRET_KEY`
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST=db_dev`, `DB_PORT=5432`
- `FRONTEND_URL=http://localhost:5173`
- SMTP-переменные (`EMAIL_*`, `DEFAULT_FROM_EMAIL`)

3. Поднимите сервисы:
```bash
docker compose -f docker-compose.dev.yml up --build
```

4. Доступные адреса:
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000/api/home/`
- Django admin: `http://localhost:8000/auth/admin/`
- PostgreSQL: `localhost:5439`

## Запуск в Docker (prod)

1. Создайте env-файл:
```bash
cp backend/core/settings/.env.prod.exemple backend/core/settings/.env.prod
```

2. Заполните `backend/core/settings/.env.prod` (аналогично dev, но с prod-значениями):
- `FRONTEND_URL=https://ваш-домен`
- `DB_HOST=db_prod`
- `DB_PORT=5432`

3. В `docker-compose.prod.yml` укажите свои образы:
- `backend_prod.image`
- `frontend_prod.image`

4. Запуск:
```bash
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d
```

5. Порты в текущем `docker-compose.prod.yml`:
- Backend (gunicorn): `127.0.0.1:8001 -> 8000`
- Frontend (nginx): `127.0.0.1:3000 -> 80`
- PostgreSQL: `127.0.0.1:5440 -> 5432`

## Сборка production-образов вручную (опционально)

Если CI/CD не собирает образы автоматически:

```bash
docker build -f backend/Dockerfile.prod -t ghcr.io/<owner>/<repo>-backend:latest ./backend
docker build -f frontend/Dockerfile.prod -t ghcr.io/<owner>/<repo>-frontend:latest ./frontend
```

После этого обновите теги в `docker-compose.prod.yml`.

## Полезные команды

Логи dev:
```bash
docker compose -f docker-compose.dev.yml logs -f
```

Остановка dev:
```bash
docker compose -f docker-compose.dev.yml down
```

Остановка prod:
```bash
docker compose -f docker-compose.prod.yml down
```

Пересоздать только backend в dev:
```bash
docker compose -f docker-compose.dev.yml up -d --build --force-recreate backend
```

## Известные моменты
- Во frontend сейчас `baseURL` зашит как `http://localhost:8000/api` (`frontend/src/services/api.js`). Для реального production лучше вынести URL в env фронта.
- Backend в dev/prod стартует с `migrate` (и в prod дополнительно `collectstatic`) через команду в compose.
- В `docker-compose` используется поле `version`; современные версии Docker Compose его игнорируют (warning), это не ломает запуск.

