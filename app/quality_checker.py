import json
from typing import Literal

from google import genai
from pydantic import BaseModel, Field

MODEL_NAME = "gemini-3.5-flash-lite"


class QualityAnalysis(BaseModel):
    quality_score: float = Field(ge=0, le=100)
    confidence_level: Literal["High", "Medium", "Low"]
    meaning_preserved: bool
    warnings: list[str] = Field(default_factory=list)
    feedback: str


class QualityChecker:
    def __init__(self, client: genai.Client):
        self.client = client

    def check_quality(
        self,
        original_text: str,
        back_translated_text: str,
    ) -> QualityAnalysis:

        prompt = f"""
        You are an expert translation quality evaluator.

        Compare the original and back-translated text.

        ORIGINAL TEXT:
        {original_text}

        BACK-TRANSLATED TEXT:
        {back_translated_text}

        Evaluate:
        1. Meaning preservation.
        2. Missing information.
        3. Changed facts or details.
        4. Tone and intent preservation.

        Assign a score from 0 to 100.

        Return valid JSON with:
        quality_score, confidence_level, meaning_preserved,
        warnings, feedback.

        Confidence guidelines:
        High: 85-100
        Medium: 60-84
        Low: Below 60

        Be strict when meaning changes.
        """

        try:
            response = self.client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config={"response_mime_type": "application/json"},
            )

            if not response.text:
                raise ValueError("Empty quality analysis response.")

            result = json.loads(response.text)

            analysis = QualityAnalysis.model_validate(result)

            # Determine confidence using the actual score.
            if analysis.quality_score >= 85:
                analysis.confidence_level = "High"
            elif analysis.quality_score >= 60:
                analysis.confidence_level = "Medium"
            else:
                analysis.confidence_level = "Low"

            # Automatically flag low-quality translations.
            if analysis.quality_score < 60:
                analysis.warnings.append(
                    "Low translation quality detected. " "Manual review is recommended."
                )

            if not analysis.meaning_preserved:
                analysis.warnings.append(
                    "The original meaning was not fully preserved."
                )

            if 60 <= analysis.quality_score < 85:
                analysis.warnings.append("Translation quality requires manual review.")

            return analysis

        except Exception as error:
            raise RuntimeError(f"Quality checking failed: {error}") from error
