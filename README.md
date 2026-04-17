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

Если локально не установлены Python/Node зависимости, запускай проверки в контейнерах:

```bash
# API tests (из корня репо)
docker run --rm -v "$PWD/apps/api:/app" -w /app python:3.11-slim sh -lc "pip install -e . && pytest -q"

# Web build (из корня репо)
docker run --rm -v "$PWD/apps/web:/app" -w /app node:20-alpine sh -lc "npm install && npm run build"
```

Или одной командой через скрипт:

```bash
# можно запускать из любого подпути репозитория
./scripts/check-in-docker.sh all   # api + web
./scripts/check-in-docker.sh api   # только api
./scripts/check-in-docker.sh web   # только web
./scripts/check-in-docker.sh --help
```

Или через `make`:

```bash
make check      # api + web
make check MODE=api
make check MODE=web
make check-api  # только api
make check-web  # только web
make help       # показать все цели
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


## CI

GitHub Actions workflow: `.github/workflows/ci.yml`

Runs on push/PR:
- API install + tests (`pytest -q`)
- Web install + build (`npm run build`)
