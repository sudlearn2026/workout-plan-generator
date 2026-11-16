
import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv(Path(__file__).resolve().parent / ".env")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("API key not found")
else:
    try:
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": "Say hello in one sentence."
                }
            ],
            max_completion_tokens=150
        )

        print("Groq API connection successful!")
        print(response.choices[0].message.content)

    except Exception as error:
        print("Groq API test failed!")
        print(type(error).__name__)
        print(str(error))
