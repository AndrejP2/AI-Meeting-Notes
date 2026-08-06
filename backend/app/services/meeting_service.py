from sqlmodel import Session, select

from app.models import Meeting
from app.schemas.analysis import TextAnalysisModel


def save_meeting(
    session: Session,
    original_text: str,
    analysis: TextAnalysisModel,
) -> Meeting:
    meeting = Meeting(
        original_text=original_text,
        summary=analysis.summary,
        keywords=analysis.keywords,
        main_points=analysis.main_points,
        action_items=analysis.action_items,
    )

    try:
        session.add(meeting)
        session.commit()
        session.refresh(meeting)

        return meeting

    except Exception:
        session.rollback()
        raise


def get_all_meetings(
    session: Session,
    offset: int = 0,
    limit: int = 100,
) -> list[Meeting]:
    statement = (
        select(Meeting)        # SELECT * FROM meetings
        .offset(offset)
        .limit(limit)          # offset -> preskoci prvih n, liimit -> uzmi samo n redova
    )

    meetings = session.exec(statement).all()

    return list(meetings)


def get_meeting_by_id(
    session: Session,
    meeting_id: int,
) -> Meeting | None:
    meeting = session.get(Meeting, meeting_id)     # SELECT * FROM meetings WHERE id = meeting_id

    return meeting


def delete_meeting(
    session: Session,
    meeting: Meeting,
) -> None:
    try:
        session.delete(meeting)
        session.commit()

    except Exception:
        session.rollback()
        raise