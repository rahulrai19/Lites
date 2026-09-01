from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

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
    
    # Semantic Cache configuration
    SEMANTIC_CACHE_THRESHOLD: float = 0.95

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

env = Env()
