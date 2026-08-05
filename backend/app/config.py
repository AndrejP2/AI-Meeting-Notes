import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    ollama_host: str = os.getenv(
        "OLLAMA_HOST",
        "http://localhost:11434",
    )

    ollama_model: str = os.getenv(
        "OLLAMA_MODEL",
        "llama3.2:3b",
    )


    database_url: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./meeting_notes.db",
    )


settings = Settings()
