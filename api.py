import os
from typing import Optional
from groq import Groq


class MeowMeowAPI:
    def __init__(self) -> None:
        self.api_key_file: str = "api_key.txt"
        self.api_key: Optional[str] = self.load_api_key()
        self.client: Groq = Groq(api_key=self.api_key)

    def load_api_key(self) -> Optional[str]:
        if os.path.exists(self.api_key_file):
            with open(self.api_key_file, "r") as f:
                return f.read().strip()
        return None

    def save_api_key(self, api_key: str) -> None:
        with open(self.api_key_file, "w") as f:
            f.write(api_key)
        self.api_key = api_key
        self.client = Groq(api_key=self.api_key)

    def send_message(self, prompt: str) -> str:
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content
