# CalcSteam

## Что готово сейчас

- Инициализирован репозиторий проекта.
- Подготовлен стартовый каркас для дальнейшей поэтапной разработки MVP.

## Что предстоит сделать

### Этап 1
- Scaffold monorepo: `apps/web`, `apps/api`, `packages/shared`, `infra`, `docs`.
- Backend foundation (FastAPI, SQLAlchemy, Alembic).
- Auth + RBAC (`admin`, `operator`, `viewer`).
- Базовые модели БД и initial migration.

### Этап 2
- Pricing engine по формулам ТЗ.
- Rates module и price snapshots.
- Settings module (конфиги pricing/promotion).

### Этап 3
- Inventory + Orders flow (reserve/fulfill/problem/complete).
- Redis locks (TTL reserve, anti-double-click, distributed scheduler locks).
- Шифрование кодов и audit log критических операций.

### Этап 4
- Frontend admin panel (login/dashboard/pricing/inventory/orders/settings/reports).
- Role-based UI ограничения и статусы рисков.

### Этап 5
- Unit/integration/E2E тесты.
- Seed-данные.
- Docker Compose (web/api/db/redis/nginx) + healthchecks.
- Финальный README и runbook запуска/эксплуатации.

## Следующий шаг

Начать с Этапа 1 и последовательно реализовать production-ready MVP по ТЗ.
