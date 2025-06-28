from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL:str="sqlite+aiosqlite:///./database.db"
    PROJECT_NAME:str="Stocky"
    ACCESS_TOKEN_EXPIRE_MINUTES:int=30
    ALGORITHM:str="HS256"
    SECRET_KEY:str="tu_super_clave_secreta_y_segura"

    model_config=SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

    