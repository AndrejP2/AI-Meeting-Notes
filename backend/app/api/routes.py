from fastapi import APIRouter, HTTPException
from httpx import request
from app.services.ai_service import analyze_meeting_text
from app.schemas.analysis import TextAnalysisModel, TextRequest

router = APIRouter()


@router.get("/")
def root():
    return {"message": "AI Meeting Notes API"}



@router.post("/analyze-text", response_model=TextAnalysisModel)
def analyze_text(request: TextRequest):


    try:
        analysis = analyze_meeting_text(request.text)

        return analysis

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Text analysis failed: {str(error)}",
        )

