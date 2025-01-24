from openai import OpenAI

OPENAI_API_KEY = """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"""


class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def chat_completions(self, message):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "너는 도와주는 사람이야."},
                {"role": "user", "content": message}
            ]
        )

        return response
