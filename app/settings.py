from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


env_path = Path(__file__).resolve().parent.parent / '.env' 


class Settings(BaseSettings):
    db_url: str
    
    model_config = SettingsConfigDict(env_file=env_path)


settings = Settings()
