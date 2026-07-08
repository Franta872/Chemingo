from pathlib import Path
import json
from typing import Literal

def all_languages(mode: Literal["select", "codes"]) -> list[tuple[str, str]] | tuple[str, ...]:
    """
    Returns a codes of languages or list of tuples for Textual Select widget 
    based on input.
    """
    path = Path(__file__).parent / "languages.json"
    with path.open(encoding="utf-8") as file:
        langs: dict = json.load(file)

    if mode == "select":
        return list(
            zip(
                (x["native_name"] for x in langs.values()),
                langs.keys()
                )
            )
    elif mode == "codes":
        return tuple(langs.keys())


if __name__ == "__main__":
    print(all_languages("codes"))