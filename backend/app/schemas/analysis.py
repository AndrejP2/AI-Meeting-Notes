from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class TextRequest(BaseModel):
    text: str = Field(min_length=1)

class TextAnalysisModel(BaseModel):
    summary: str
    keywords: list[str]
    main_points: list[str]
    action_items: list[str]

class MeetingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    original_text: str
    summary: str
    keywords: list[str]
    main_points: list[str]
    action_items: list[str]
    created_at: datetime
