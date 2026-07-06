from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # Use absolute path to avoid issues
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/data/app.db"
    
    SECRET_KEY: str = "your-super-secret-key-change-in-production-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    class Config:
        env_file = ".env"

settings = Settings()