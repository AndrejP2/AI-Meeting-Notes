from datetime import datetime, timezone
from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class Meeting(SQLModel, table=True):     # True označava da je ovo db model, a ne običan i da treba napraviti tablicu s njim
    __tablename__ = "meetings"

    id: int | None = Field(     # vrijednost je int ili None, jer će se automatski generirati prilikom umetanja u bazu
        default=None,           # None znači da će se vrijednost automatski generirati prilikom umetanja u bazu
        primary_key=True,
    )

    original_text: str

    summary: str

    keywords: list[str] = Field(
        sa_column=Column(JSON),
    )

    main_points: list[str] = Field(
        sa_column=Column(JSON),
    )

    action_items: list[str] = Field(
        sa_column=Column(JSON),
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )