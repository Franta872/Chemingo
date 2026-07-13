from pathlib import Path
import json
from data.database import all_languages_codes

class Translate:
    """
    Class for storing current language and returning needed words.
    """
    def __init__(self, language: str = "en"):
        self._language = language

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, lang: str):
        if lang not in all_languages_codes:
            raise KeyError(f"{lang} is not in supported languages.")
        else:
            self._language = lang
    
    def t(self, word: str, screen: str) -> str:
        path = Path(__file__).parent / f"screens/{screen}/{self._language}.json"
        with path.open(encoding="utf-8") as file:
            screen_json = json.load(file)
            if word == "":
                return ""
            elif isinstance(screen_json[word], list):
                return "\n".join(screen_json[word])
            else:
                return screen_json[word]
        # finds a word translation based on a language, screen and key word 