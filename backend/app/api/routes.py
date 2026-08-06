from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.database import get_session
from app.schemas.analysis import (
    MeetingResponse,
    TextRequest,
    DeleteMeetingResponse,
)
from app.services.ai_service import (
    InvalidAIResponseError,
    OllamaModelNotFoundError,
    OllamaUnavailableError,
    analyze_meeting_text,
    check_ollama_status,
)
from app.services.meeting_service import (
    delete_meeting,
    get_all_meetings,
    get_meeting_by_id,
    save_meeting,
)

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


@router.get(
    "/meetings",
    response_model=list[MeetingResponse],
)
def read_meetings(
    offset: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
):
    meetings = get_all_meetings(
        session=session,
        offset=offset,
        limit=limit,
    )

    return meetings


@router.get(
    "/meetings/{meeting_id}",
    response_model=MeetingResponse,
)
def read_meeting(
    meeting_id: int,
    session: Session = Depends(get_session),
):
    meeting = get_meeting_by_id(
        session=session,
        meeting_id=meeting_id,
    )

    if meeting is None:
        raise HTTPException(
            status_code=404,
            detail="Sastanak nije pronađen.",
        )

    return meeting


@router.delete(
    "/meetings/{meeting_id}",
    response_model=DeleteMeetingResponse,
)
def remove_meeting(
    meeting_id: int,
    session: Session = Depends(get_session),
):
    meeting = get_meeting_by_id(
        session=session,
        meeting_id=meeting_id,
    )

    if meeting is None:
        raise HTTPException(
            status_code=404,
            detail="Sastanak nije pronađen.",
        )

    delete_meeting(
        session=session,
        meeting=meeting,
    )

    return {
        "message": "Sastanak je uspješno obrisan.",
        "deleted_id": meeting_id,
    }

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