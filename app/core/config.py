from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    CACHE_TTL: int = 3600  # 1 hour cache by default
    
    class Config:
        env_file = ".env"

settings = Settings() 