from models.llm_message import LLMUserMessage, LLMAssistantMessage, LLMSystemMessage

def get_system_prompt():
    return LLMSystemMessage(content="You are a wine professional tasked with helping answer questions about certain wine regions.")

def get_user_promt(input:str):
    return LLMUserMessage(content=input)
