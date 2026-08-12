from app.schemas.analysis import TextAnalysisModel 
from ollama import Client, ResponseError
from app.config import settings
from pydantic import ValidationError



client = Client(host=settings.ollama_host)

class OllamaUnavailableError(Exception):
    pass


class OllamaModelNotFoundError(Exception):
    pass 


class InvalidAIResponseError(Exception):
    pass

def analyze_meeting_text(text: str) -> TextAnalysisModel:

    try:
        response = client.chat(
            model= settings.ollama_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You analyze meeting transcripts. "
                        "Return a concise summary, important keywords, "
                        "main discussion points and concrete action items. "
                        "Do not invent information that is not present in the text. "
                        "Write the result in the same language as the meeting text."
                    ),
                },
                {
                    "role": "user",
                    "content": text,
                },
            ],
            format=TextAnalysisModel.model_json_schema(),
            options={
                "temperature": 0,     # niza temp. -> manje kreativnosti, buduci da je ovo analiza 
            },
        )

    except ResponseError as error:
        if error.status_code == 404:
            raise OllamaModelNotFoundError(
                f"Model '{settings.ollama_model}' nije pronađen."
            ) from error

        raise OllamaUnavailableError(
            f"Ollama je vratila grešku: {error}"
        ) from error

    except ConnectionError as error:
        raise OllamaUnavailableError(
            "Nije moguće povezati se s Ollamom."
        ) from error

    try:
        return TextAnalysisModel.model_validate_json(
            response.message.content
        )

    except ValidationError as error:
        raise InvalidAIResponseError(
            "AI model nije vratio očekivanu strukturu podataka."
        ) from error

    

def check_ollama_status() -> dict:
    try:
        response = client.list()

    except ConnectionError as error:
        raise OllamaUnavailableError(
            "Nije moguće povezati se s Ollamom."
        ) from error

    except Exception as error:
        raise OllamaUnavailableError(
            f"Provjera Ollame nije uspjela: {error}"
        ) from error

    installed_models = []

    for model in response.models:
        model_name = getattr(model, "model", None)

        if model_name is None:
            model_name = getattr(model, "name", None)

        if model_name is not None:
            installed_models.append(model_name)

    model_installed = settings.ollama_model in installed_models

    return {
        "ollama": "available",
        "selected_model": settings.ollama_model,
        "model_installed": model_installed,
        "installed_models": installed_models,
    }