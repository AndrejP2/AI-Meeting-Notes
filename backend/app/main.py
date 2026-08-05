from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.database import create_db_and_tables
from app.models import Meeting


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()

    yield


app = FastAPI(
    title="AI Meeting Notes API",
    description="API for analyzing and storing meeting transcripts",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)