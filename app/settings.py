from pydantic import BaseSettings


class Settings(BaseSettings):
    app_user: str
    app_password: str
    secret_key: str
    secret_key_size: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
