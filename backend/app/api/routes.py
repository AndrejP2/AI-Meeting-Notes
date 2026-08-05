from fastapi import APIRouter, HTTPException
from httpx import request
from app.schemas.analysis import TextAnalysisModel, TextRequest
from app.services.ai_service import (
    analyze_meeting_text,
    OllamaModelNotFoundError,
    OllamaUnavailableError,
    InvalidAIResponseError,
    check_ollama_status
)


router = APIRouter()


@router.get("/")
def root():
    return {"message": "AI Meeting Notes API"}

@router.get("/status")
def health():
    try:
        return check_ollama_status()

    except OllamaUnavailableError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        )

@router.post("/analyze-text", response_model=TextAnalysisModel)
def analyze_text(request: TextRequest):

    try:
        return analyze_meeting_text(request.text)

    except OllamaModelNotFoundError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        )

    except OllamaUnavailableError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        )

    except InvalidAIResponseError as error:
        raise HTTPException(
            status_code=502,
            detail=str(error),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Dogodila se neočekivana greška.",
        )
