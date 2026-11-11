import json
from unittest.mock import MagicMock

from app.quality_checker import QualityChecker


def test_quality_check_high_confidence():
    mock_client = MagicMock()

    mock_response = MagicMock()
    mock_response.text = json.dumps(
        {
            "quality_score": 95,
            "confidence_level": "High",
            "meaning_preserved": True,
            "warnings": [],
            "feedback": "The original meaning is preserved.",
        }
    )

    mock_client.models.generate_content.return_value = mock_response

    checker = QualityChecker(mock_client)

    result = checker.check_quality(
        original_text="I am happy today.", back_translated_text="I feel happy today."
    )

    assert result.quality_score == 95
    assert result.confidence_level == "High"
    assert result.meaning_preserved is True
    assert result.warnings == []


def test_quality_check_low_confidence():
    mock_client = MagicMock()

    mock_response = MagicMock()
    mock_response.text = json.dumps(
        {
            "quality_score": 35,
            "confidence_level": "Low",
            "meaning_preserved": False,
            "warnings": ["Meaning has changed."],
            "feedback": "Important meaning was lost.",
        }
    )

    mock_client.models.generate_content.return_value = mock_response

    checker = QualityChecker(mock_client)

    result = checker.check_quality(
        original_text="I will attend the meeting.",
        back_translated_text="I will cancel the meeting.",
    )

    assert result.quality_score == 35
    assert result.confidence_level == "Low"
    assert result.meaning_preserved is False
    assert len(result.warnings) > 0


def test_low_score_generates_warning():
    mock_client = MagicMock()

    mock_response = MagicMock()
    mock_response.text = json.dumps(
        {
            "quality_score": 40,
            "confidence_level": "Low",
            "meaning_preserved": False,
            "warnings": [],
            "feedback": "Important meaning was lost.",
        }
    )

    mock_client.models.generate_content.return_value = mock_response

    checker = QualityChecker(mock_client)

    result = checker.check_quality(
        original_text="I will attend the meeting.",
        back_translated_text="I will cancel the meeting.",
    )

    assert result.confidence_level == "Low"
    assert result.meaning_preserved is False
    assert len(result.warnings) >= 2


def test_medium_score_generates_warning():
    mock_client = MagicMock()

    mock_response = MagicMock()
    mock_response.text = json.dumps(
        {
            "quality_score": 75,
            "confidence_level": "Medium",
            "meaning_preserved": True,
            "warnings": [],
            "feedback": "Some stylistic differences exist.",
        }
    )

    mock_client.models.generate_content.return_value = mock_response

    checker = QualityChecker(mock_client)

    result = checker.check_quality(
        original_text="Good morning. How are you?",
        back_translated_text="Good morning. How do you feel?",
    )

    assert result.confidence_level == "Medium"
    assert any("manual review" in warning.lower() for warning in result.warnings)
