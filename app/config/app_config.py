from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    app_env: str = "local"
    eureka_server_url: str
    app_name: str
    instance_host: str
    instance_port: int

    model_config = SettingsConfigDict(
        env_file=(".env.local", ".env.dev", ".env.prod"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

env = os.getenv("APP_ENV", "local")
settings = Settings(_env_file=f".env.{env}")

print(f"Loaded settings: {settings.dict()}")