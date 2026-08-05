from app.schemas.analysis import TextAnalysisModel 
from ollama import chat


def analyze_meeting_text(text: str) -> dict:

    response = chat(
        model="llama3.2:3b",
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
            "temperature": 0,
        },
    )

    analysis = TextAnalysisModel.model_validate_json(
        response.message.content
    )
 

    return analysis
