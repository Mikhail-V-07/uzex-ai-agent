from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

models = [
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash",
    "gemini-3.6-flash",
    "gemini-3.7-flash",
    "gemini-flash-lite-latest",
]

for model in models:
    print(f"\nПроверяем {model}...")

    try:
        response = client.models.generate_content(
            model=model,
            contents="Ответь одним словом: Привет"
        )

        print("УСПЕХ:", response.text)

    except Exception as error:
        print("ОШИБКА:", str(error)[:250])