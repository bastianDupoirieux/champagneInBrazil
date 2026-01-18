from utils.get_env import get_ollama_model_env
from constants.llm import DEFAULT_OLLAMA_MODEL

def get_model():
    ollama_model = get_ollama_model_env()
    if ollama_model is None:
        return DEFAULT_OLLAMA_MODEL
    return ollama_model
