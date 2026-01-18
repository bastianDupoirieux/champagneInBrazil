import ollama

def get_available_model_names():
    available_models = ollama.list().models
    return [mod.model for mod in available_models]
