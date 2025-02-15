from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database settings
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "hacklahoma"
    
    # OpenAI settings
    OPENAI_API_KEY: str
    MODEL_NAME: str = "gpt-4-turbo-preview"  # or "gpt-3.5-turbo" for lower cost
    MODEL_TEMPERATURE: float = 0.2
    
    # Application settings
    MAX_ITERATIONS: int = 3
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings() 