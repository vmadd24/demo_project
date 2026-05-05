"""
ASGI entrypoint for the Django bakery backend.
Exposed as `app` so the existing supervisor command
`uvicorn server:app --host 0.0.0.0 --port 8001 --reload` continues to work.
"""
import os
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bakery.settings")
# Permit synchronous DB calls during ASGI startup (used by api.apps.ready() seed hook).
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

import django  # noqa: E402

django.setup()

from django.core.asgi import get_asgi_application  # noqa: E402

app = get_asgi_application()
