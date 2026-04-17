# CalcSteam Web

Stage 4 admin panel scaffold on Next.js (App Router) with:

- React Query provider (`@tanstack/react-query`)
- Zustand app store (token + role)
- Role switch in top navigation
- Login flow calling `/api/v1/auth/login`
- Dashboard summary from `/api/v1/dashboard/summary`
- Orders page:
  - fetch list from `/api/v1/orders`
  - create order (`POST /api/v1/orders`)
  - actions: reserve (`/orders/{id}/reserve`), fulfill, mark problem
- Pricing page data fetch from `/api/v1/pricing/recommendations` (fallback to mock)
- Inventory page:
  - list from `/api/v1/inventory/codes`
  - create code (`POST /api/v1/inventory/codes`)
  - reveal action `/inventory/codes/{id}/reveal`
- Reports page data from `/api/v1/reports/*`
- Settings save via `PATCH /api/v1/settings` (admin only)

Pages:
- `/login`
- `/dashboard`
- `/pricing`
- `/inventory`
- `/orders`
- `/settings`
- `/reports`

## Run

```bash
cd apps/web
npm install
npm run dev
```
