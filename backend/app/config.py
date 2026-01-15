from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Sales Management IMS"
    app_env: str = "development"
    app_port: int = 8000

    mysql_user: str = "your_user"
    mysql_password: str = "your_password"
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_db: str = "sales_db"
    database_url: str = "mysql+pymysql://your_user:your_password@localhost:3306/sales_db"

    jwt_secret: str = "change_me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    cors_allow_origins: str = "*"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
