from pydantic import BaseModel, Field

class TextRequest(BaseModel):
    text: str = Field(min_length=1)

class TextAnalysisModel(BaseModel):
    summary: str
    keywords: list[str]
    main_points: list[str]
    action_items: list[str]

