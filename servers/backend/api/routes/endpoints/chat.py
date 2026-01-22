import json
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.list_available_models import list_available_models
from utils.llm_calls import get_llm_response


CHAT_ROUTER = APIRouter(prefix="/chat", tags=["chat"])

@CHAT_ROUTER.get("/models/available", response_model=list[str])
async def get_available_models():
    return await list_available_models()

@CHAT_ROUTER.get("/chat", response_model=str)
async def chat(query: str):
    return await get_llm_response(query)

@CHAT_ROUTER.post("/chat", response_model=str)
async def chat(query: str):
    return await get_llm_response(query)



