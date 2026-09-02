from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Env(BaseSettings):
    NODE_ENV: Literal["development", "test", "production"] = "development"
    HOST: str = "0.0.0.0"
    PORT: int = 3000
    LOG_LEVEL: Literal["fatal", "error", "warn", "info", "debug", "trace", "silent"] = "info"
    SHUTDOWN_TIMEOUT_MS: int = 10000
    
    # Optimization Thresholds
    MIN_TOKENS_FOR_OPTIMIZATION: int = 50
    MAX_TOKENS_FOR_OPTIMIZATION: int = 128000
    
    # AI Optimization configuration
    AI_OPTIMIZE_THRESHOLD: int = 500
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    
    # Redis configuration
    REDIS_URL: Optional[str] = None
    CACHE_TTL_SECONDS: int = 3600
    
    # Authentication
    LITES_API_KEY: Optional[str] = None
    
    # Security / CORS
    FRONTEND_URL: str = "http://localhost:5173"
    
    # Semantic Cache configuration
    SEMANTIC_CACHE_THRESHOLD: float = 0.95

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

env = Env()
