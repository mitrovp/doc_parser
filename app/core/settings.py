from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    HOST: str
    PORT: int
    RELOAD: bool
    DEBUG: bool

    OPENAI_API_KEY: str
    WHISPERER_API_KEY: str

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
