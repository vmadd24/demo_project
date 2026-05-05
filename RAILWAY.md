# Maison Levain — Railway Deployment Guide

This monorepo contains two Railway services:
- `backend/` — Django + DRF + Postgres (uvicorn ASGI)
- `frontend/` — React (CRA), served as a static site via `serve`

Both directories contain `Procfile` + `railway.json` for one-click deploys.

---

## 1. Push to GitHub
Use Emergent's **"Save to GitHub"** button in the chat input to publish the repo.

## 2. Create a Railway project
1. railway.com → **New Project → Deploy from GitHub Repo** → pick this repo.
2. Add a **PostgreSQL plugin**: New → Database → Postgres. Railway auto-injects `DATABASE_URL` into linked services.

## 3. Backend service
- **Settings → Service → Source → Root Directory:** `backend`
- Railway auto-detects `railway.json` / `Procfile` and runs:
  ```
  python manage.py migrate --noinput
  python manage.py collectstatic --noinput
  uvicorn server:app --host 0.0.0.0 --port $PORT
  ```
- **Variables** (Settings → Variables):
  | Key | Value |
  | --- | --- |
  | `DATABASE_URL` | (auto from Postgres plugin) |
  | `DB_SSL` | `true` |
  | `DJANGO_SECRET_KEY` | run `python -c "import secrets;print(secrets.token_urlsafe(64))"` |
  | `DJANGO_DEBUG` | `false` |
  | `JWT_SECRET` | a long random hex string |
  | `ADMIN_EMAIL` | `admin@yourbakery.com` |
  | `ADMIN_PASSWORD` | a strong password |
  | `FRONTEND_URL` | `https://<your-frontend>.up.railway.app` |
  | `CORS_ALLOWED_ORIGINS` | `https://<your-frontend>.up.railway.app` |
  | `CSRF_TRUSTED_ORIGINS` | `https://<your-frontend>.up.railway.app,https://<your-backend>.up.railway.app` |
  | `ALLOWED_HOSTS` | `<your-backend>.up.railway.app` |

- Click **Generate Domain** in Settings → Networking. Copy it.

## 4. Frontend service
1. Project → **+ New → GitHub Repo** (same repo).
2. **Settings → Source → Root Directory:** `frontend`
3. **Variables:**
   | Key | Value |
   | --- | --- |
   | `REACT_APP_BACKEND_URL` | `https://<your-backend>.up.railway.app` |
4. **Generate Domain** → copy it.
5. Go back to the **backend** service and update `FRONTEND_URL`, `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS` with this URL, then redeploy.

## 5. First login
Visit `https://<your-frontend>.up.railway.app/admin/login` and sign in with the `ADMIN_EMAIL` / `ADMIN_PASSWORD` you set. Migrations + admin + 9 sample products auto-seed on first boot.

---

## How it all fits together
- `dj-database-url` in `bakery/settings.py` reads `DATABASE_URL` and configures Postgres automatically (falls back to SQLite locally).
- `whitenoise` serves static files (Django collectstatic output) on the same uvicorn process — no separate CDN needed.
- `samesite=None; secure=true` cookies require HTTPS, which Railway provides by default.
- The backend's `CORS_ALLOWED_ORIGINS` and `CSRF_TRUSTED_ORIGINS` MUST exactly match the frontend origin (scheme + host, no trailing slash).

## Local development (still works)
```bash
cd backend && pip install -r requirements.txt && python manage.py migrate && uvicorn server:app --reload --port 8001
cd frontend && yarn && yarn start
```
Local dev uses SQLite at `backend/db.sqlite3`. Delete that file to reset.
