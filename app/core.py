from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    RESEND_API_KEY: str
    EMAIL_RECEIVER: str

    class Config:
        env_file = ".env"


settings = Settings()
