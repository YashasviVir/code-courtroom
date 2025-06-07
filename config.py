from pydantic_settings import BaseSettings


class Config(BaseSettings):
    model_name: str = "gemini-2.5-flash-preview-05-20"


config = Config()
