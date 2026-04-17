"""
Authentication Module — API Key + JWT hỗ trợ.

Cung cấp 2 phương thức xác thực:
1. API Key qua header X-API-Key
2. JWT Token qua header Authorization: Bearer <token>
"""
import jwt
import time
from datetime import datetime, timedelta, timezone
from fastapi import Header, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .config import settings

security = HTTPBearer()


def create_jwt_token(username: str) -> str:
    """Tạo JWT token có hiệu lực trong 60 phút."""
    payload = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=60),
        "iat": datetime.now(timezone.utc)
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def verify_api_key(x_api_key: str) -> str:
    """Kiểm tra API Key từ header."""
    if not x_api_key or x_api_key != settings.agent_api_key:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return "api_user"


def verify_jwt_token(token: str) -> str:
    """Kiểm tra JWT Token hợp lệ. Nhận token string trực tiếp."""
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid Token")
