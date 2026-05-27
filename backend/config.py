from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Sistema Alquileres"
    app_env: str = "dev"
    database_url: str = "sqlite:///./alquileres.db"
    jwt_secret_key: str = "super-secreto-cambiar"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 480

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
