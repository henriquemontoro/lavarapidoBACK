from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = ""

    N8N_AVISAR_INICIO_WEBHOOK_URL: str = ""
    N8N_AVISAR_PRONTO_WEBHOOK_URL: str = ""

    # Segredo compartilhado com o workflow do n8n: ele manda esse valor no header
    # X-N8N-Secret ao chamar POST /agendamentos, e a API confere antes de gravar.
    N8N_INBOUND_SECRET: str = ""

    OPENAI_API_KEY: str = ""

    CORS_ALLOWED_ORIGINS: str = "http://localhost:5173"

    class Config:
        env_file = ".env"

    @property
    def cors_allowed_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ALLOWED_ORIGINS.split(",") if origin.strip()]


@lru_cache()
def get_settings() -> Settings:
    return Settings()
