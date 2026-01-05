from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_VERSION: str
    DEBUG: bool
    APP_ENV: str
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
