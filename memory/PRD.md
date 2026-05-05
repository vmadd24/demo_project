# Maison Levain — Artisan Bakery

## Problem Statement
Build a simple bakery application with React frontend and Python (FastAPI) backend.

## User Choices (captured)
- Features: Product catalog + Admin panel
- Payment: None — "Place Order" form only
- Auth: Admin only (JWT email/password)
- Design: Warm & rustic (earthy tones, artisan feel)
- Images: Stock bakery images from the web

## Architecture
- **Frontend:** React 18 + React Router + Tailwind + lucide-react. Warm rustic theme (`#F9F6F0` bg, `#C86B3C` primary, Playfair Display + Manrope).
- **Backend:** Django 5.1 + Django REST Framework + pymongo (sync). Served via uvicorn as ASGI (`server:app = get_asgi_application()`). UUID ids, all routes under `/api`.
- **DB:** MongoDB collections — `users`, `products`, `orders` (no Django ORM; pymongo direct).
- **Auth:** JWT (PyJWT + bcrypt) via httpOnly cookie + `Authorization: Bearer` header (localStorage fallback).

## User Personas
1. **Shopper** — browses catalogue, filters by category, places a single-product order with contact + address.
2. **Bakery admin** — logs in, manages products (CRUD), reviews & updates order status.

## Core Requirements (static)
- Public storefront with hero, filterable catalogue, story, visit sections.
- Order placement without payment (phone confirmation workflow).
- Admin login + dashboard for product CRUD and order management.

## Implemented (2026-01)
- **Iteration 1 — FastAPI MVP:** auth, products CRUD, orders, admin seed, 9 sample products. Storefront + admin UI. 100% tests.
- **Iteration 2 — Django rewrite (current):** Same API contract re-implemented on Django 5.1 + DRF + pymongo, served by uvicorn ASGI. Frontend unchanged. 100% backend pytest, end-to-end storefront order + admin login verified against Django.

## Prioritized Backlog
- **P1:** Add rate limiting on public `/api/orders`; add brute-force lockout on login (playbook recommendation).
- **P2:** Multi-item cart (currently single product per order).
- **P2:** Image upload to Cloudinary instead of URL input.
- **P2:** Email/SMS notification to customer on order confirmation.
- **P3:** Loyalty program, weekly subscription box, gift cards.

## Next Tasks
- Await user feedback / iteration requests.
