from pathlib import Path
import json
from data.database import all_languages_codes, compounds_by_formula, elements_by_symbol
import re

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
    
    def t(self, word: str | tuple, screen: str, description: dict | None = None) -> str:
        if isinstance(word, tuple):
            return "".join(
                [(self.t(x[1], screen, description) if x[0] == "w" else x[1]) for x in word]
                )
        path = Path(__file__).parent / f"screens/{screen}/{self._language}.json"
        with path.open(encoding="utf-8") as file:
            screen_json = json.load(file)
            if word == "":
                return ""
            elif isinstance(screen_json[word], list):
                return self.replace_chemical_placeholders("\n".join(screen_json[word]), description)
            else:
                return self.replace_chemical_placeholders(screen_json[word], description)
        # finds a word translation based on a language, screen and key word 

    def replace_chemical_placeholders(
        self,
        word: str,
        description: dict | None
        ) -> str:
        if description is None:
            return word
        for num in description.keys():
            if description[num]["type"] == "element":
                if description[num]["appearance"] == "symbol":
                    item_result = description[num]["item"]
                else: # description[num]["appearance"] == "name"
                    item_result = elements_by_symbol[description[num]["item"]]["names"][self.language]
            else: # description[num]["type"] == "compound"
                if description[num]["appearance"] == "symbol": # (formula)
                    item_result = compounds_by_formula[description[num]["item"]]["formula_unicode"]
                else: # description[num]["appearance"] == "name"
                    item_result = compounds_by_formula[description[num]["item"]]["names"][self.language]
            word = word.replace(f"<{num}>", item_result)
        return word