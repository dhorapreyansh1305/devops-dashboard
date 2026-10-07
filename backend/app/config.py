from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://devops:devops@localhost:5432/devops"
    jwt_secret: str = "change-me-in-production"
    cors_origins: str = "http://localhost"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
