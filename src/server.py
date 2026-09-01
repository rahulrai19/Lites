import uvicorn
from src.config.env import env

if __name__ == "__main__":
    uvicorn.run(
        "src.core.app:app",
        host=env.HOST,
        port=env.PORT,
        reload=(env.NODE_ENV == "development")
    )
