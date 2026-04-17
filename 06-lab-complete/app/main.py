"""
Production AI Agent — Part 6: Final Project
Kết hợp TẤT CẢ Day 12 concepts.

Checklist:
  ✅ Config từ environment (12-factor)
  ✅ Structured JSON logging
  ✅ API Key + JWT authentication
  ✅ Rate limiting (Redis sliding window)
  ✅ Cost guard (daily budget)
  ✅ Input validation (Pydantic)
  ✅ Health check + Readiness probe
  ✅ Graceful shutdown (SIGTERM)
  ✅ Security headers
  ✅ CORS
  ✅ Error handling
  ✅ Metrics endpoint
  ✅ Stateless design (state in Redis)
  ✅ Real LLM (Google Gemini) support
"""

import os
import time
import json
import logging
import signal
import requests
from datetime import datetime, timezone
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, Request, Response
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn
import redis

from app.config import settings
from app.auth import verify_api_key, verify_jwt_token, create_jwt_token
from app.rate_limiter import check_rate_limit, r as redis_client
from app.cost_guard import check_budget, record_usage
from utils.mock_llm import ask as llm_ask

# ─────────────────────────────────────────────────────────
# Logging — JSON structured
# ─────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format='{"ts":"%(asctime)s","lvl":"%(levelname)s","msg":"%(message)s"}',
)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────
# Global state (non-persistent — for metrics only)
# ─────────────────────────────────────────────────────────
START_TIME = time.time()
_is_ready = False
_request_count = 0
_error_count = 0


# ─────────────────────────────────────────────────────────
# Pydantic Models
# ─────────────────────────────────────────────────────────
class AskRequest(BaseModel):
    question: str = Field(
        ..., min_length=1, max_length=2000, description="Your question for the agent"
    )


class AskResponse(BaseModel):
    question: str
    answer: str
    user_id: str
    model: str
    timestamp: str
    status: str = "success"


class LoginRequest(BaseModel):
    username: str
    password: str


# ─────────────────────────────────────────────────────────
# Authentication helper
# ─────────────────────────────────────────────────────────
def get_current_user(request: Request) -> str:
    """Xác thực qua API Key hoặc JWT."""
    api_key = request.headers.get("X-API-Key")
    if api_key:
        return verify_api_key(api_key)

    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        return verify_jwt_token(token)

    raise HTTPException(
        status_code=401,
        detail="Authentication required. Include header: X-API-Key or Authorization: Bearer <jwt>",
    )


# ─────────────────────────────────────────────────────────
# LLM Caller — supports real Google Gemini or mock
# ─────────────────────────────────────────────────────────
def call_real_llm(prompt: str) -> str:
    """Gọi LLM thật (Google Gemini) hoặc fallback về mock."""
    if not settings.google_api_key:
        return llm_ask(prompt)

    try:
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{settings.llm_model}:generateContent?key={settings.google_api_key}"
        )
        headers = {"Content-Type": "application/json"}
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        logger.error(
            json.dumps(
                {
                    "event": "llm_error",
                    "error": str(e),
                    "model": settings.llm_model,
                }
            )
        )
        # Fallback to mock on error
        return llm_ask(prompt)


# ─────────────────────────────────────────────────────────
# Lifespan — startup / shutdown
# ─────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    global _is_ready
    logger.info(
        json.dumps(
            {
                "event": "startup",
                "app": settings.app_name,
                "version": settings.app_version,
                "environment": settings.environment,
            }
        )
    )
    # Verify Redis connection on startup
    try:
        redis_client.ping()
        logger.info(json.dumps({"event": "redis_connected"}))
    except Exception as e:
        logger.warning(
            json.dumps({"event": "redis_connection_failed", "error": str(e)})
        )

    _is_ready = True
    logger.info(json.dumps({"event": "ready"}))

    yield

    _is_ready = False
    logger.info(
        json.dumps({"event": "shutdown", "msg": "Agent shutting down gracefully..."})
    )


# ─────────────────────────────────────────────────────────
# App
# ─────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs" if settings.environment != "production" else None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=(
        settings.allowed_origins.split(",") if settings.allowed_origins else ["*"]
    ),
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type", "X-API-Key"],
)


# ─────────────────────────────────────────────────────────
# Middleware — Security headers + request logging
# ─────────────────────────────────────────────────────────
@app.middleware("http")
async def request_middleware(request: Request, call_next):
    global _request_count, _error_count
    start = time.time()
    _request_count += 1
    try:
        response: Response = await call_next(request)
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        if "server" in response.headers:
            del response.headers["server"]

        duration = round((time.time() - start) * 1000, 1)
        logger.info(
            json.dumps(
                {
                    "event": "request",
                    "method": request.method,
                    "path": request.url.path,
                    "status": response.status_code,
                    "ms": duration,
                }
            )
        )
        return response
    except Exception as e:
        _error_count += 1
        raise


# ─────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────


@app.get("/", tags=["Info"])
def root():
    """Root endpoint — hiển thị thông tin app."""
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "endpoints": {
            "ask": "POST /ask (requires X-API-Key or Bearer JWT)",
            "login": "POST /login (for JWT)",
            "health": "GET /health",
            "ready": "GET /ready",
            "metrics": "GET /metrics (requires auth)",
        },
    }


@app.get("/health", tags=["Operations"])
def health():
    """Liveness probe. Platform restarts container if this fails."""
    return {
        "status": "ok",
        "version": settings.app_version,
        "environment": settings.environment,
        "uptime_seconds": round(time.time() - START_TIME, 1),
        "total_requests": _request_count,
        "llm": "gemini" if settings.google_api_key else "mock",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/ready", tags=["Operations"])
def ready():
    """Readiness probe. Load balancer stops routing here if not ready."""
    if not _is_ready:
        raise HTTPException(status_code=503, detail="App not ready")
    try:
        redis_client.ping()
        return {"status": "ready", "redis": "connected"}
    except Exception:
        raise HTTPException(status_code=503, detail="Redis connection failed")


@app.post("/login", tags=["Auth"])
def login(body: LoginRequest):
    """Đăng nhập lấy JWT token."""
    if (
        body.username == settings.demo_username
        and body.password == settings.demo_password
    ):
        token = create_jwt_token(body.username)
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/ask", response_model=AskResponse, tags=["Agent"])
async def ask(
    body: AskRequest,
    request: Request,
    user_id: str = Depends(get_current_user),
):
    """
    Send a question to the AI agent.

    **Authentication:** Include header `X-API-Key: <key>` or `Authorization: Bearer <jwt>`
    """
    # Rate limit check
    check_rate_limit(user_id)

    # Budget check
    check_budget(user_id)

    # Calculate input tokens (rough estimate)
    input_tokens = len(body.question.split()) * 2

    # Log the request
    logger.info(
        json.dumps(
            {
                "event": "agent_call",
                "q_len": len(body.question),
                "user_id": user_id,
                "client": str(request.client.host) if request.client else "unknown",
            }
        )
    )

    # Call LLM
    answer = call_real_llm(body.question)
    output_tokens = len(answer.split()) * 2

    # Save conversation history to Redis (stateless design)
    history_key = f"history:{user_id}"
    redis_client.rpush(history_key, json.dumps({"q": body.question, "a": answer}))
    redis_client.ltrim(history_key, -10, -1)  # Keep last 10 conversations

    # Record usage for cost guard
    record_usage(user_id, input_tokens, output_tokens)

    return AskResponse(
        question=body.question,
        answer=answer,
        user_id=user_id,
        model=settings.llm_model if settings.google_api_key else "mock-llm",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.get("/metrics", tags=["Operations"])
def metrics(user_id: str = Depends(get_current_user)):
    """Basic metrics (protected). Requires authentication."""
    return {
        "uptime_seconds": round(time.time() - START_TIME, 1),
        "total_requests": _request_count,
        "error_count": _error_count,
        "daily_budget_usd": settings.daily_budget_usd,
        "rate_limit_per_minute": settings.rate_limit_per_minute,
        "environment": settings.environment,
    }


# ─────────────────────────────────────────────────────────
# Graceful Shutdown
# ─────────────────────────────────────────────────────────
def _handle_signal(signum, _frame):
    logger.info(
        json.dumps({"event": "signal", "signum": signum, "msg": "Received SIGTERM"})
    )


signal.signal(signal.SIGTERM, _handle_signal)


# ─────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    logger.info(f"Starting {settings.app_name} on {settings.host}:{settings.port}")
    logger.info(f"API Key: {settings.agent_api_key[:4]}****")
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        timeout_graceful_shutdown=30,
    )
