import pytest
from project import count_dictionary_list_items, is_blank_dictionary, translate

def test_count_dictionary_list_items():
    assert count_dictionary_list_items(
        {
            "test_1": [1, 2, 3],
            "test_2": {"a", "b", "c"},
            "test_3": (True, False)
            }
        ) == 8
    assert count_dictionary_list_items({}) == 0
    assert count_dictionary_list_items(
        {
            "test_1": [],
            "test_2": (),
            "test_3": set()
            }
        ) == 0
    assert count_dictionary_list_items(
        {
            "first": [1, 2],
            "second": {"a", "b", "c"},
            "third": ("x",),
        }
    ) == 6
    with pytest.raises(AttributeError):
        count_dictionary_list_items(True)
    with pytest.raises(AttributeError):
        count_dictionary_list_items([])
    with pytest.raises(TypeError):
        count_dictionary_list_items()
    with pytest.raises(TypeError):
        count_dictionary_list_items({"a": True, "b": 1})


def test_is_blank_dictionary():
    assert is_blank_dictionary({}) is True
    assert is_blank_dictionary({"test_1": 123}) is False
    assert is_blank_dictionary(
        {
            "test_1": True,
            "test_2": {},
            "test_3": ()
            }
        ) is False
    with pytest.raises(TypeError):
        is_blank_dictionary()
    with pytest.raises(TypeError):
        is_blank_dictionary(True)
    with pytest.raises(TypeError):
        is_blank_dictionary([])


def test_translate():
    assert translate("welcome", "welcome", "de") == "Willkommen bei Chemingo!"
    assert translate("language", "welcome", "ko") == "언어: "
    assert translate("welcome", "welcome", "cs") == "Vitej v Chemingo!"
    assert translate("welcome", "welcome", "es") == "¡Bienvenido a Chemingo!"
    assert translate("welcome", "welcome", "pl") == "Witaj w Chemingo!"
    assert translate("welcome", "welcome", "it") == "Benvenuto in Chemingo!"
    assert translate("welcome", "welcome", "hu") == "Üdvözlünk a Chemingo alkalmazasban!"

    assert translate("language", "choice", "de") == "Sprache: "
    assert translate("compounds", "choice", "cs") == "Sloučeniny"
    assert translate("elements", "choice", "ko") == "원소"
    assert translate("elements", "choice", "fr") == "éléments"
    assert translate("compounds", "choice", "pl") == "Związki chemiczne"

    assert translate("language", "quiz", "ja") == "言語"
    assert translate("language", "quiz", "fr") == "Langue"
    assert translate("language", "quiz", "uk") == "Мова"
    assert translate("language", "quiz", "zh") == "语言"

    with pytest.raises(FileNotFoundError):
        translate("welcome", "non_existing_screen", "en")
    with pytest.raises(KeyError):
        translate("non_existing_word", "welcome", "en")
    with pytest.raises(FileNotFoundError):
        translate("welcome", "welcome", "tat")