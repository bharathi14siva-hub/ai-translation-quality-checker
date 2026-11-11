import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

MODEL_NAME = "gemini-3.5-flash-lite"


class Translator:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing. Check your .env file.")

        self.client = genai.Client(api_key=api_key)

    def _generate_response(self, prompt: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
            )

            if not response.text:
                raise RuntimeError("Gemini returned an empty response.")

            return response.text.strip()

        except Exception as error:
            raise RuntimeError(f"Translation request failed: {error}") from error

    def translate_text(
        self,
        text: str,
        source_language: str,
        target_language: str,
    ) -> str:

        prompt = f"""
        Translate the following text from {source_language}
        to {target_language}.

        Preserve the original meaning, tone, context, and intent.
        Do not add explanations or extra information.
        Return only the translated text.

        Text:
        {text}
        """

        return self._generate_response(prompt)

    def back_translate_text(
        self,
        translated_text: str,
        target_language: str,
        source_language: str,
    ) -> str:

        prompt = f"""
        Translate the following text from {target_language}
        back into {source_language}.

        Preserve the meaning as accurately as possible.
        Do not refer to the original text.
        Do not add explanations.
        Return only the translated text.

        Text:
        {translated_text}
        """

        return self._generate_response(prompt)
