from pathlib import Path
import json

def all_languages() -> list:
    path = Path(__file__).parent.parent.parent / "data" / "languages.json"
    with path.open(encoding="utf-8") as file:
        langs = json.load(file)

    return list(
        zip(
            (x["native_name"] for x in langs.values()),
            langs.keys()
            )
        )


if __name__ == "__main__":
    print(all_languages())