# CalcSteam Web

Stage 4 admin panel scaffold on Next.js (App Router) with:

- React Query provider (`@tanstack/react-query`)
- Zustand app store (token + role)
- Role switch in top navigation
- Login flow calling `/api/v1/auth/login`
- Orders page data fetch from `/api/v1/orders`

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
