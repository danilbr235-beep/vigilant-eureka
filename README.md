# CalcSteam

Production-oriented MVP внутренней системы продавца Steam-пополнений (не клиентская витрина).

## Реализовано сейчас

### Stage 1
- Monorepo scaffold: `apps/web`, `apps/api`, `packages/shared`, `infra`, `docs`.
- Backend foundation на FastAPI.
- SQLAlchemy-модели всех 12 сущностей.
- Alembic initial migration.
- Auth + RBAC foundation.

### Stage 2 (foundation)
- Pricing service с формулами из ТЗ и проверкой tolerance.
- API route groups для `dashboard`, `pricing`, `inventory`, `orders`, `rates`, `settings`, `reports`.
- Rates/settings базовые сервисы.
- Unit tests для pricing formulas.

### Stage 3 (implemented core flow)
- Inventory: code create/list/reveal with encryption-at-rest + masked storage.
- Orders: create/reserve/fulfill with real status transitions and TTL reservation timestamps.
- Audit log writes for critical inventory/order actions.
- Alembic migration for reservation link `code_items.current_order_id`.

### Stage 4 (web scaffold)
- Next.js admin panel scaffold with pages: login, dashboard, pricing, inventory, orders, settings, reports.
- Status badges for risk states and basic operator action UI in orders page.

## Быстрый запуск

```bash
docker compose up --build
```

API health check:

```bash
curl http://localhost:8000/health
```

## Локальный запуск API

```bash
cd apps/api
pip install -e .
uvicorn app.main:app --reload
```

## Тесты

```bash
cd apps/api
pytest -q
```

## Миграции

```bash
cd apps/api
alembic upgrade head
```

## Переменные окружения

См. `.env.example`.


## Seed

```bash
cd apps/api
python -m app.seed
```

Demo users created by seed:
- admin@calcsteam.local / admin123
- operator@calcsteam.local / operator123
- viewer@calcsteam.local / viewer123
