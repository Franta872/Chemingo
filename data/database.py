from pathlib import Path
import json

from data.locales.all_languages.language_select import all_languages

def open_json_file(path: str) -> dict:
    with Path(path).open(encoding="utf-8") as file:
        return json.load(file)


compounds_by_formula: dict = open_json_file("data/compounds/by_formula.json")
"""
A large dictionary of **compounds sorted by formula**.
Example:
```
{
    "formula": {
      "id": "...",
      "category_id": "...",
      "formula": "...",
      "formula_unicode": "...",
    "names": {
      "language code": "name in that language",
      ...
    },
  ...
}
```
"""
compounds_categories: dict = open_json_file("data/compounds/categories.json")
"""
A dictionary of **compounds categories sorted by their id** (englisch name).
Example:
```
{
"(id)": {
  "names": {
    "(language code)": "(language code)",
    ...
  },
  "compound_count": ...
},
...
}
```
"""
elements_by_symbol: dict = open_json_file("data/elements/by_symbol.json")
"""
A dictionary of **elements sorted by their symbol**:
Example:
```
{
  "(symbol)": {
    "id": "...",
    "atomic_number": ...,
    "symbol": "...",
    "names": {
      "(language code)": "(language code)",
      ...
    }
  },
  ...
}
```
"""
all_languages_select: list[tuple[str, str]] = all_languages("select")
"""
A list of tuples and in each tuple is name of the language in the language
and it's language code. Languages are languages, that this app supports.
Example:
```
[('English', 'en'), ('Latina', 'la'), ('Čeština', 'cs'), ...]
``` 
"""
all_languages_codes: tuple[str, ...] = all_languages("codes")
"""
A tuple of all language codes of languages, that this app supports.
Example: 
```
('en', 'la', 'cs', 'de', ...)
"""

if __name__ == "__main__":
    print(compounds_categories)