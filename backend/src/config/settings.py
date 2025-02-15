from pydantic_settings import BaseSettings
from pydantic import validator

class Settings(BaseSettings):
    # Database settings
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "hacklahoma"
    
    # Groq settings
    GROQ_API_KEY: str
    MODEL_NAME: str = "mixtral-8x7b-32768"  # Groq's Mixtral model
    MODEL_TEMPERATURE: float = 0.2
    
    # Application settings
    MAX_ITERATIONS: int = 3
    LOG_LEVEL: str = "INFO"
    
    # Add validation
    @validator("MODEL_NAME")
    def validate_model_name(cls, v):
        allowed_models = ["mixtral-8x7b-32768", "llama2-70b-4096"]
        if v not in allowed_models:
            raise ValueError(f"Model must be one of {allowed_models}")
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings() 