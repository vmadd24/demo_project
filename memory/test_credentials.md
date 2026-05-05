# Test Credentials — Maison Levain Bakery

## Admin Account (seeded on startup)
- **Email:** `admin@bakery.com`
- **Password:** `admin123`
- **Role:** admin
- **Login URL:** `/admin/login`
- **Dashboard URL:** `/admin`

## Auth Endpoints
- POST `/api/auth/login` — body `{ email, password }`, returns `{ token, ... }` and sets `access_token` httpOnly cookie.
- POST `/api/auth/logout`
- GET  `/api/auth/me` — requires Bearer token or cookie

## Public Endpoints (no auth)
- GET  `/api/products` — query `?category=Bread|Cake|Pastry|All`
- GET  `/api/products/{id}`
- POST `/api/orders` — body `{ customer_name, phone, address, notes, items: [{ product_id, product_name, quantity, price }] }`

## Admin-only Endpoints (Bearer token required)
- POST   `/api/products`
- PUT    `/api/products/{id}`
- DELETE `/api/products/{id}`
- GET    `/api/orders`
- PATCH  `/api/orders/{id}/status` — body `{ "status": "pending|confirmed|completed|cancelled" }`
