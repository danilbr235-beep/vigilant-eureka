# Stage 5 (partial): dashboard and reports API backed by DB

Implemented DB-backed dashboard/reports service and wired routers:

- `GET /api/v1/dashboard/summary`
- `GET /api/v1/dashboard/charts`
- `GET /api/v1/reports/profit`
- `GET /api/v1/reports/orders`
- `GET /api/v1/reports/problems`
- `GET /api/v1/reports/audit`

Includes unit coverage for summary/profit metrics in `test_reports_service.py`.
