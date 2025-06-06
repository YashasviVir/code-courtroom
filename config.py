from pydantic_settings import BaseSettings

class Config(BaseSettings):
    model_name: str = "gemini-2.5-pro-preview-05-06"

config = Config()