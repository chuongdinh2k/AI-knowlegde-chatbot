from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database Configuration
    database_url: str = "postgresql://username:password@localhost:5432/ai_chat_db"
    postgres_user: str = "username"
    postgres_password: str = "password"
    postgres_db: str = "ai_chat_db"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    
    # OpenAI Configuration
    openai_api_key: str = ""
    
    # Hugging Face Configuration
    huggingface_api_token: str = ""
    
    # Application Configuration
    secret_key: str = "your-secret-key-change-this"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Vector Database Configuration
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
