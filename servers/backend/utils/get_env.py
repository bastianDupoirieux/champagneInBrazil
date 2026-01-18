import os
from dotenv import load_dotenv

load_dotenv()

def get_app_data_directory_env():
    return os.getenv("APP_DATA_DIRECTORY")

def get_database_url_env():
    return os.getenv("DATABASE_URL")

def get_ollama_model_env():
    return os.getenv("OLLAMA_MODEL")
