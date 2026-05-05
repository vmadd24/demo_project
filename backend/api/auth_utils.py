import bcrypt
import jwt
from datetime import datetime, timezone, timedelta
from django.conf import settings
from functools import wraps
from rest_framework.response import Response

from .db import users


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def create_access_token(user_id: str, email: str) -> str:
    payload = {
        "sub": user_id,
        "email": email,
        "exp": datetime.now(timezone.utc) + timedelta(hours=12),
        "type": "access",
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def _extract_token(request) -> str | None:
    token = request.COOKIES.get("access_token")
    if token:
        return token
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return auth[7:]
    return None


def get_current_admin(request):
    """Returns user dict on success, Response on error (to be returned by view)."""
    token = _extract_token(request)
    if not token:
        return None, Response({"detail": "Not authenticated"}, status=401)
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None, Response({"detail": "Token expired"}, status=401)
    except jwt.InvalidTokenError:
        return None, Response({"detail": "Invalid token"}, status=401)

    user = users.find_one({"id": payload["sub"]}, {"_id": 0, "password_hash": 0})
    if not user or user.get("role") != "admin":
        return None, Response({"detail": "Admin not found"}, status=401)
    return user, None


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        user, err = get_current_admin(request)
        if err is not None:
            return err
        request.admin_user = user
        return view_func(self, request, *args, **kwargs)

    return wrapper
