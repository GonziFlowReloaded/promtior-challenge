from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "Promtior Chatbot"
    PROJECT_VERSION: str = "1.0.0"
    DEBUG: bool = True
    PORT: int = 8000
    
    # MongoDB settings
    MONGO_URI: str = os.getenv("MONGO_URI", "")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "scraper_db")
    MONGO_COLLECTION_NAME: str = os.getenv("MONGO_COLLECTION_NAME", "pages")
    
    # Google API settings
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "models/embedding-001")
    CHAT_MODEL: str = os.getenv("CHAT_MODEL", "gemini-2.0-flash")
    
    # Vector store settings
    VECTOR_DB_PATH: str = os.getenv("VECTOR_DB_PATH", "chroma_db")
    
    class Config:
        env_file = ".env"

settings = Settings()