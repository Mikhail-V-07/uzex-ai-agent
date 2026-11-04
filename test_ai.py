from dotenv import load_dotenv
from google import genai
import os
import time

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

for attempt in range(1, 4):
    try:
        print(f"Попытка {attempt}. Модель: {model}")

        response = client.models.generate_content(
            model=model,
            contents="Ответь на русском: что такое биржевая сделка?"
        )

        print("\nОтвет Gemini:")
        print(response.text)
        break

    except Exception as error:
        print(f"Ошибка: {error}")

        if "503" in str(error) and attempt < 3:
            wait = attempt * 5
            print(f"Повторим через {wait} секунд...")
            time.sleep(wait)
        else:
            break