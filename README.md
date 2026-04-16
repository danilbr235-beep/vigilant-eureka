# CalcSteam

Production-oriented MVP внутренней системы продавца Steam-пополнений (не клиентская витрина).

## Stage 1 (сделано)

- Собран monorepo scaffold: `apps/web`, `apps/api`, `packages/shared`, `infra`, `docs`.
- Поднят backend foundation на FastAPI.
- Реализованы SQLAlchemy-модели всех 12 сущностей из ТЗ.
- Добавлена initial Alembic migration с нужными индексами.
- Реализованы auth endpoints (`/api/v1/auth/login`, `/api/v1/auth/me`) и RBAC dependency layer.

## Структура

- `apps/api` — FastAPI, SQLAlchemy, Alembic.
- `apps/web` — будущая админ-панель (Stage 4).
- `packages/shared` — общие контракты/типы.
- `infra` — nginx конфиг.
- `docs` — этапная документация.

## Быстрый запуск (локально)

```bash
docker compose up --build
```

API health check:

```bash
curl http://localhost:8000/health
```

## Миграции

```bash
cd apps/api
alembic upgrade head
```

## Переменные окружения

См. `.env.example`.
