# Stage 5 (partial): seed data

Implemented idempotent seed script `app.seed` that creates:

- 1 admin, 1 operator, 1 viewer
- sell nominals for USD/EUR/KZT/CNY per specification
- supplier code types for SGD/MYR
- default pricing config and promotion rule
- demo purchase batch and demo encrypted code items
- demo FX rates

Run:

```bash
cd apps/api
python -m app.seed
```
