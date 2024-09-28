import os
import getpass
import keyring
from groq import Groq
from typing import Optional

SERVER_NAME = "MeowMeow-Key"
USERNAME = getpass.getuser()

class MeowMeowAPI:
    def __init__(self) -> None:
        self.api_key: Optional[str] = self.load_api_key()
        self.client: Optional[Groq] = None
        if self.api_key:
            self.client = Groq(api_key=self.api_key)

    def load_api_key(self) -> Optional[str]:
        api_key = keyring.get_password(SERVER_NAME, USERNAME)
        if api_key:
            return api_key
        return None

    def save_api_key(self, api_key: str) -> None:
        keyring.set_password(SERVER_NAME, USERNAME, api_key)
        self.api_key = api_key
        self.client = Groq(api_key=self.api_key)

    def send_message(self, prompt: str) -> Optional[str]:
        if not self.client:
            return "API key is missing or invalid. Please set a valid API key."
        try:
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
        except Exception as e:
            return f"Error sending message: {str(e)}"
