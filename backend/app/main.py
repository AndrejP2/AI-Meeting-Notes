from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="AI Meeting Notes API", description="API for analyzing meeting notes using AI", version="1.0.0")

app.include_router(router)
