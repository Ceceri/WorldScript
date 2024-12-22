from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str 
    OPENAI_API_KEY: str

    class Config:
        env_file = "../.env"  # 设置为相对于 `backend` 目录的路径

settings = Settings()
print(f"Loaded OPENAI_API_KEY: {settings.OPENAI_API_KEY}")
