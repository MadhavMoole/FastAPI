# app/core/security.py
from datetime import datetime, timedelta, timezone
from jose import jwt
import uuid
from app.core.config import settings

def create_access_token(data: dict):
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        **data,
        "expiry": exp,
        "iat": now,
        "nbf": now,
        "type": "access",
        "jti": str(uuid.uuid4())
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict):
    now = datetime.now(timezone.utc)
    exp = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    payload = {
        **data,
        "expiry": exp,
        "iat": now,
        "nbf": now,
        "type": "refresh",
        "jti": str(uuid.uuid4())
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_user_dict(user):
    return {
        "name": str(user["first_name"]) + " " + str(user["last_name"]),
        "email": user["email"],
    }