from collections.abc import Generator
from sqlmodel import Session, SQLModel, create_engine
from app.config import settings


connect_args = {
    "check_same_thread": False,      # FastAPI može tijekom jednog zahtjeva koristiti različite dretve, pa za SQLite postavljamo False
}

engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
)    # glavni objekt preko kojeg aplikacija komunicira s bazom


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session