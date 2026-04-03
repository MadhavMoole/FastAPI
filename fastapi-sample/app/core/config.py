from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    MONGO_URL: str
    DB_NAME: str
    REDIS_URL: str

    SECRET_KEY: str
    ALGORITHM: str
    
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "https://yourfrontend.com"
    ]

    class Config:
        env_file = ".env"

settings = Settings()