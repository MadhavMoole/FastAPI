from datetime import datetime, timedelta, timezone
from jose import jwt
import uuid
from app.core.config import settings

def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire,          # Expiry
        "iat": now,             # Issued at
        "nbf": now,             # Not before
        "type": "access",       # Token type
        "jti": str(uuid.uuid4())  # Unique token ID (for revocation)
    })

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()

    now = datetime.now(timezone.utc)
    expire = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({
        "exp": expire,
        "iat": now,
        "nbf": now,
        "type": "refresh",
        "jti": str(uuid.uuid4())
    })

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )