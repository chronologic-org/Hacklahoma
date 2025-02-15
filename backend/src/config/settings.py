from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "hacklahoma"
    MAX_ITERATIONS: int = 3
    MODEL_TEMPERATURE: float = 0.2
    
    class Config:
        env_file = ".env"

settings = Settings() 