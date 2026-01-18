from pydantic import BaseModel

class LLMessage(BaseModel):
    role: str
    content: str
