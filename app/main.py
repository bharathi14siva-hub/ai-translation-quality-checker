
from pathlib import Path

from app.quality_checker import QualityChecker
from app.translator import Translator
from models.schemas import TranslationResult


def run_translation():
    print("\n" + "=" * 55)
    print("       AI TRANSLATION QUALITY CHECKER")
    print("=" * 55)

    original_text = input("\nEnter text to translate: ").strip()

    if not original_text:
        print("Error: Text cannot be empty.")
        return

    source_language = input("Enter source language: ").strip()
    target_language = input("Enter target language: ").strip()

    if not source_language or not target_language:
        print("Error: Language fields cannot be empty.")
        return

    try:
        translator = Translator()
        quality_checker = QualityChecker(translator.client)

        print("\nTranslating text...")
        translated_text = translator.translate_text(
            original_text,
            source_language,
            target_language,
        )

        print("Back-translating text...")
        back_translated_text = translator.back_translate_text(
            translated_text,
            target_language,
            source_language,
        )

        print("Checking translation quality...")
        quality = quality_checker.check_quality(
            original_text,
            back_translated_text,
        )

        result = TranslationResult(
            original_text=original_text,
            source_language=source_language,
            target_language=target_language,
            translated_text=translated_text,
            back_translated_text=back_translated_text,
            quality_score=quality.quality_score,
            confidence_level=quality.confidence_level,
            meaning_preserved=quality.meaning_preserved,
            warnings=quality.warnings,
            feedback=quality.feedback,
        )

        print("\n" + "=" * 55)
        print("             TRANSLATION REPORT")
        print("=" * 55)

        print("\nOriginal Text:")
        print(result.original_text)

        print("\nTranslated Text:")
        print(result.translated_text)

        print("\nBack-Translated Text:")
        print(result.back_translated_text)

        print("\nQuality Score:", f"{result.quality_score}/100")
        print("Confidence Level:", result.confidence_level)
        print("Meaning Preserved:", result.meaning_preserved)

        print("\nFeedback:")
        print(result.feedback)

        print("\nWarnings:")
        if result.warnings:
            for warning in result.warnings:
                print("-", warning)
        else:
            print("No translation issues detected.")

        if (
            result.confidence_level.lower() == "low"
            or result.quality_score < 60
            or not result.meaning_preserved
        ):
            print("\nWARNING: Low-quality translation detected!")
        else:
            print("\nTranslation quality check completed.")

        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        output_file = output_dir / "translation_result.json"

        output_file.write_text(
            result.model_dump_json(indent=4),
            encoding="utf-8",
        )

        print(f"\nResult saved to: {output_file}")

    except (ValueError, RuntimeError, OSError) as error:
        print(f"\nApplication Error: {error}")


if __name__ == "__main__":
    run_translation()
