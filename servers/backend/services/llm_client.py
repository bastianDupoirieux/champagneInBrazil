import ollama
import asyncio
from typing import List, Optional, Dict, Any

from enums.llm_provider import LLMProvider
from models.llm_message import LLMMessage

class LLMClient:
    def __init__(self):
        self._client = self._get_client()

        self.llm_provider = "ollama"

    def _get_client(self):
        return ollama.AsyncClient()

    async def generate_content(
            self,
            model: str,
            messages = List[Dict[str, Any]],
    ) -> str | None:
        client: ollama.AsyncClient = self._client
        response = await client.chat(model = model, messages = messages)

        return response.message.content
