from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.lifespan import app_lifespan
from api.routes.router import API_ROUTER

app = FastAPI(lifespan=app_lifespan)

app.include_router(API_ROUTER)

