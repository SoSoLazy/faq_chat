import os
import logging

from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


class OpenAiCLient:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def chat_completions(self, message: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "너는 도와주는 사람이야."},
                {"role": "user", "content": message}
            ]
        )
        logging.info(response)

        return response.choices[0].message.content
    
    def embedding(self, message:str) -> str:
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=message
        )
        logging.info(message, response)

        return response.data[0].embedding

open_ai_client = OpenAiCLient(OPENAI_API_KEY)