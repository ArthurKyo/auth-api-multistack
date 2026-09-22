from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Auth API Multistack"
    environment: str = "development"
    database_url: str = "postgresql+psycopg://postgres:postgres@db:5432/auth_api"
    jwt_secret: str = "change-this-secret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7
    login_rate_limit: int = 5
    register_rate_limit: int = 3
    rate_limit_window_seconds: int = 60

    model_config = SettingsConfigDict(
        env_file="../../.env",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
