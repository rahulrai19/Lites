import logging
from fastapi import FastAPI
from app.config.env import env
from app.core.health import router as health_router

def build_app() -> FastAPI:
    app = FastAPI(title="Lites")

    # Set up basic logging
    log_level_name = env.LOG_LEVEL.upper()
    if log_level_name == "TRACE":
        log_level_name = "DEBUG"
    elif log_level_name == "SILENT":
        log_level_name = "CRITICAL"
    
    log_level = logging.getLevelName(log_level_name)
    logging.basicConfig(level=log_level)

    app.include_router(health_router)

    return app

app = build_app()
