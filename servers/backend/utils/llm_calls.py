from services.llm_client import LLMClient
from constants.prompts import get_system_prompt, get_user_promt
from utils.llm_providers import get_model

async def get_llm_response(input:str):
    client = LLMClient()
    model = get_model()
    try:
        response = await client.generate_content(model=model, messages=[get_system_prompt(), get_user_promt(input)])
        return response
    except Exception as e:
        raise e
