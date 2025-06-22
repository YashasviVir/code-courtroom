import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

envs = {
    "GOOGLE_CLOUD_PROJECT": os.getenv("GOOGLE_CLOUD_PROJECT"),
    "GOOGLE_CLOUD_LOCATION": os.getenv("GOOGLE_CLOUD_LOCATION"),
    "GOOGLE_CLOUD_STORAGE_BUCKET": os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET"),
    "DEFAULT_RESOURCE_ID": os.getenv("DEFAULT_RESOURCE_ID"),
}

for key, value in envs.items():
    if value is None:
        raise ValueError(f"Environment variable {key} is not set.")


class Config(BaseSettings):
    model_name: str = "gemini-2.5-flash-preview-05-20"
    google_cloud_project: str = envs["GOOGLE_CLOUD_PROJECT"]
    google_cloud_location: str = envs["GOOGLE_CLOUD_LOCATION"]
    google_cloud_storage_bucket: str = envs["GOOGLE_CLOUD_STORAGE_BUCKET"]
    default_resource_id: str = envs["DEFAULT_RESOURCE_ID"]


config = Config()
