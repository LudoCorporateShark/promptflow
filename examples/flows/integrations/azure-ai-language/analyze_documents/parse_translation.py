#parse_translation.py
from promptflow import tool

@tool
def parse_translation(translation_results: dict, language: str) -> str:
    try:
        # Convert language to an integer if needed
        language_key = int(language)

        # Access the translation result using the integer key
        return translation_results.get(language_key, "Language not found")

    except ValueError:
        # Handle the case where language is not a valid integer
        return "Invalid language code: must be an integer"

    except Exception as e:
        # Handle any other exceptions that might occur
        return f"Error: {str(e)}"
