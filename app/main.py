import uvicorn
from app.config.env import env
from app.core.app import app

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=env.HOST,
        port=env.PORT,
        reload=(env.NODE_ENV == "development")
    )
