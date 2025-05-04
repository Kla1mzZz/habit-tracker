from typing import List
from pathlib import Path
from pydantic import BaseModel, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


load_dotenv()


class DatabaseConfig(BaseModel):
    driver: str = 'asyncpg'
    user: str = 'postgres'
    password: str = '123'
    host: str = 'localhost'
    port: int = 5432
    name: str = 'habit_tracker'

    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 5
    max_overflow: int = 10

    @computed_field
    def url(self) -> str:
        return f'postgresql+{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'


class Prefix(BaseModel):
    v1: str = '/api/v1'


class MLConfig(BaseModel):
    base_path: Path = Path(__file__).resolve(strict=True).parent.parent / 'ml'
    path_to_model_weights: Path = (
        base_path / 'models' / 'trained' / 'predict_model_weights.pth'
    )
    path_to_train_data: Path = base_path / 'data' / 'habits_data.csv'


class AppConfig(BaseModel):
    debug: bool = False
    docs_url: str = '/docs'
    openapi_prefix: str = ''
    openapi_url: str = '/openapi.json'
    redoc_url: str = '/redoc'
    title: str = 'Habit Tracker'
    version: str = '0.0.0'

    allowed_hosts: List[str] = ['*']

    prefix: Prefix = Prefix()

    secret_key: str = ''
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 30


class Settings(BaseSettings):
    database: DatabaseConfig = DatabaseConfig()
    app: AppConfig = AppConfig()
    ml: MLConfig = MLConfig()

    model_config = SettingsConfigDict(env_nested_delimiter='__')


settings = Settings()
