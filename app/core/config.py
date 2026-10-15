from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "FastAPI App"
    DEBUG: bool = False
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    SUPER_ADMIN_BOOTSTRAP_EMAIL: str | None = None
    SUPER_ADMIN_BOOTSTRAP_PASSWORD: str | None = None
    model_config = SettingsConfigDict(env_file=".env")



settings = Settings()