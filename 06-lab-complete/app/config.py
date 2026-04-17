"""
Production config — 12-Factor: tất cả từ environment variables.

Sử dụng pydantic-settings để tự động parse env vars.
"""
import os
import logging
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    environment: str = "development"
    debug: bool = False

    # App
    app_name: str = "Production AI Agent"
    app_version: str = "1.0.0"

    # LLM
    openai_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    llm_model: str = "gemini-1.5-flash"

    # LLM Pricing
    price_per_1k_input: float = 0.00015
    price_per_1k_output: float = 0.0006

    # Storage
    redis_url: str = "redis://localhost:6379/0"

    # Security
    agent_api_key: str = "dev-key-change-me"
    jwt_secret: str = "dev-jwt-secret-change-me"
    jwt_algorithm: str = "HS256"
    allowed_origins: str = "*"

    # Demo Credentials
    demo_username: str = "student"
    demo_password: str = "demo123"

    # Limits
    rate_limit_per_minute: int = 10
    daily_budget_usd: float = 1.0

    class Config:
        env_file = ".env"
        extra = "ignore"  # Cho phép thừa biến trong .env mà không lỗi

    def validate_production(self):
        """Validate critical settings in production."""
        logger = logging.getLogger(__name__)
        if self.environment == "production":
            if self.agent_api_key == "dev-key-change-me":
                raise ValueError("AGENT_API_KEY must be changed in production!")
            if self.jwt_secret == "dev-jwt-secret-change-me":
                raise ValueError("JWT_SECRET must be changed in production!")
        if not self.openai_api_key and not self.google_api_key:
            logger.warning("No LLM API key set — using mock LLM")
        return self


settings = Settings()
settings.validate_production()
