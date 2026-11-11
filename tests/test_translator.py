from unittest.mock import MagicMock

from app.translator import Translator


def test_translate_text():
    translator = Translator.__new__(Translator)
    translator.client = MagicMock()

    mock_response = MagicMock()
    mock_response.text = "Bonjour tout le monde"

    translator.client.models.generate_content.return_value = mock_response

    result = translator.translate_text(
        "Hello everyone",
        "English",
        "French",
    )

    assert result == "Bonjour tout le monde"


def test_back_translate_text():
    translator = Translator.__new__(Translator)
    translator.client = MagicMock()

    mock_response = MagicMock()
    mock_response.text = "Hello everyone"

    translator.client.models.generate_content.return_value = mock_response

    result = translator.back_translate_text(
        "Bonjour tout le monde",
        "French",
        "English",
    )

    assert result == "Hello everyone"
