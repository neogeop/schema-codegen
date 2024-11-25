from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/db"  # default for development
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
