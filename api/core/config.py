from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL:str="sqlite+aiosqlite:///./database.db"
    PROJECT_NAME:str="Stocky"
    ACCESS_TOKEN_SPIRES_MINUTES:int=30

    model_config=SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

    