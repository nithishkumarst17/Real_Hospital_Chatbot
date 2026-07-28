from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "Hospital AI Assistant"
    ENV: str = "development"
    DEBUG: bool = True

    SARVAM_API_KEY: str = "your-sarvam-api-key"
    SARVAM_BASE_URL: str = "https://api.sarvam.ai"
    SARVAM_CHAT_MODEL: str = "sarvam-m"          # Sarvam's chat/completion model
    SARVAM_TRANSLATE_ENDPOINT: str = "/translate"
    SARVAM_CHAT_ENDPOINT: str = "/v1/chat/completions"

    DB_ENGINE: str = "sqlite"
    SQLITE_PATH: str = "./hospital.db"

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "hospital_db"
    POSTGRES_USER: str = "hospital_user"
    POSTGRES_PASSWORD: str = "change_me"

    @property
    def DATABASE_URL(self) -> str:
        if self.DB_ENGINE == "sqlite":
            return f"sqlite:///{self.SQLITE_PATH}"
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    CHROMA_PERSIST_DIR: str = "./chroma_store"
    CHROMA_COLLECTION_NAME: str = "hospital_policies"

    JWT_SECRET_KEY: str = "CHANGE_THIS_TO_A_RANDOM_LONG_SECRET"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "your-email@gmail.com"
    SMTP_PASSWORD: str = "your-app-password"
    SMTP_FROM_NAME: str = "City Hospital"
    SMTP_USE_TLS: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
