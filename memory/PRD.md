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
- **Backend:** FastAPI + Motor (MongoDB async) + bcrypt + PyJWT. UUID ids, all routes under `/api`.
- **DB:** MongoDB collections — `users`, `products`, `orders`.
- **Auth:** JWT via httpOnly cookie + `Authorization: Bearer` header (localStorage fallback).

## User Personas
1. **Shopper** — browses catalogue, filters by category, places a single-product order with contact + address.
2. **Bakery admin** — logs in, manages products (CRUD), reviews & updates order status.

## Core Requirements (static)
- Public storefront with hero, filterable catalogue, story, visit sections.
- Order placement without payment (phone confirmation workflow).
- Admin login + dashboard for product CRUD and order management.

## Implemented (2026-01)
- Backend API: auth (login/logout/me), products CRUD, orders create/list/status-patch, admin seed, 9 sample products seeded.
- Frontend: Storefront (hero, catalogue w/ category filter, order modal w/ quantity stepper + success screen, story, visit, footer).
- Admin: login page, dashboard with Products tab (table, create/edit modal, delete) and Orders tab (cards, status dropdown).
- 100% test pass rate (backend pytest + frontend UI flows).

## Prioritized Backlog
- **P1:** Add rate limiting on public `/api/orders`; add brute-force lockout on login (playbook recommendation).
- **P2:** Multi-item cart (currently single product per order).
- **P2:** Image upload to Cloudinary instead of URL input.
- **P2:** Email/SMS notification to customer on order confirmation.
- **P3:** Loyalty program, weekly subscription box, gift cards.

## Next Tasks
- Await user feedback / iteration requests.
