from pydantic import BaseModel
from typing import Literal

class LLMMessage(BaseModel):
    pass

class LLMUserMessage(LLMMessage):
    role: Literal["user"]
    content: str

class LLMAssistantMessage(LLMMessage):
    role: Literal["assistant"]
    content: str

class LLMSystemMessage(LLMMessage):
    role: Literal["system"]
    content: str
