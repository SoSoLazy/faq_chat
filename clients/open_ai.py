import os
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


class OpenAiCLient:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def chat_completions(self, message):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "너는 도와주는 사람이야."},
                {"role": "user", "content": message}
            ]
        )

        return response

open_ai_client = OpenAiCLient(OPENAI_API_KEY)