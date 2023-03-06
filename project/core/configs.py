from typing import List
from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote_plus
import secrets

class Settings(BaseSettings):
    
    API_V1_STR: str = '/api/v1'
    DB_URL: str = f"postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi1"
    JWT_SECRET:str = 'dw-iQyGLZUgH7wXd8d3DWKh2VaRt5Yf7oiS9fYNB0v4'
    ALGORITHM:str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES:int = 10


    DBBaseModel = declarative_base()

    class Config():
        case_sensitive = True

settings:Settings = Settings()
