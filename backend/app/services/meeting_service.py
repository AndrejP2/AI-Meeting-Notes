from sqlmodel import Session

from app.models import Meeting
from app.schemas.analysis import TextAnalysisModel


def save_meeting( session: Session, original_text: str, analysis: TextAnalysisModel) -> Meeting:
    meeting = Meeting(
        original_text=original_text,
        summary=analysis.summary,
        keywords=analysis.keywords,
        main_points=analysis.main_points,
        action_items=analysis.action_items,
    )

    session.add(meeting)          # kazemo sesiji da ovaj objekt zelimo spremiti u bazu, no tek se dodaje u sesiju ovdje
    session.commit()              # stvarno sprema u bazu, tj. izvršava SQL upit
    session.refresh(meeting)            # ponovo učitava objekt iz baze

    return meeting