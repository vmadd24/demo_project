import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-insecure-bakery-dev-key-change-me")
DEBUG = os.environ.get("DJANGO_DEBUG", "true").lower() == "true"

# Railway sets RAILWAY_PUBLIC_DOMAIN automatically; allow it + whatever the user configures.
ALLOWED_HOSTS = ["*"] if DEBUG else [
    h.strip() for h in os.environ.get("ALLOWED_HOSTS", "").split(",") if h.strip()
] or ["*"]

# Railway uses HTTPS terminating proxy; trust it for CSRF and secure cookies.
CSRF_TRUSTED_ORIGINS = [
    o.strip()
    for o in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")
    if o.strip()
]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "corsheaders",
    "rest_framework",
    "api.apps.ApiConfig",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "bakery.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": []},
    },
]

ASGI_APPLICATION = "bakery.asgi.application"
WSGI_APPLICATION = "bakery.wsgi.application"

# ---------------- Database ----------------
# Local dev: SQLite (no extra setup). Railway: set DATABASE_URL → Postgres.
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=os.environ.get("DB_SSL", "false").lower() == "true",
    )
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
USE_TZ = True
TIME_ZONE = "UTC"

# ---------------- Static (for whitenoise / future django admin) ----------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ---------------- CORS ----------------
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:3000")
extra_origins = [
    o.strip() for o in os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",") if o.strip()
]
CORS_ALLOWED_ORIGINS = list({FRONTEND_URL, "http://localhost:3000", *extra_origins})
CORS_ALLOW_CREDENTIALS = True

# ---------------- DRF ----------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [],
    "UNAUTHENTICATED_USER": None,
    "UNAUTHENTICATED_TOKEN": None,
}

# ---------------- Bakery custom config ----------------
JWT_SECRET = os.environ.get("JWT_SECRET", "dev-jwt-secret-change-me")
JWT_ALGORITHM = "HS256"
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@bakery.com")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")
