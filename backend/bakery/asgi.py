import os
from dotenv import load_dotenv
load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bakery.settings")
import django
django.setup()
from django.core.asgi import get_asgi_application
app = get_asgi_application()
application = app
