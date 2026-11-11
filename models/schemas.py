from typing import Literal

from pydantic import BaseModel, Field, field_validator


class TranslationResult(BaseModel):
    original_text: str
    source_language: str
    target_language: str
    translated_text: str
    back_translated_text: str

    quality_score: float = Field(ge=0, le=100)

    confidence_level: Literal["High", "Medium", "Low"]

    meaning_preserved: bool

    warnings: list[str] = Field(default_factory=list)

    feedback: str

    @field_validator("quality_score")
    @classmethod
    def validate_quality_score(cls, value):
        return round(value, 2)
