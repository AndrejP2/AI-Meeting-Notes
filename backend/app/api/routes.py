from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.database import get_session
from app.schemas.analysis import (
    MeetingResponse,
    TextRequest,
)
from app.services.ai_service import (
    InvalidAIResponseError,
    OllamaModelNotFoundError,
    OllamaUnavailableError,
    analyze_meeting_text,
    check_ollama_status,
)
from app.services.meeting_service import save_meeting


router = APIRouter()


@router.get("/")
def home():
    return {
        "message": "AI Meeting Notes API is running"
    }


@router.get("/status")
def health():
    try:
        return check_ollama_status()

    except OllamaUnavailableError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        )


@router.post( "/analyze-text", response_model=MeetingResponse)
def analyze_text( request: TextRequest, session: Session = Depends(get_session) ):
    try:
        analysis = analyze_meeting_text(request.text)

        meeting = save_meeting(
            session=session,
            original_text=request.text,
            analysis=analysis,
        )

        return meeting

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