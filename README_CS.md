# Chemingo

#### [Video Demo](https://youtu.be/d6RWccxthVU)

## Popis:

Krátké představení aplikace:

- Chemingo je aplikace, kde si uživatel vybere nějaké položky ze seznamu prvků a sloučenin a následně ho z toho aplikace zkouší.
- Aplikace je určená pro lidi, co si chtějí procvičit a případně se naučit pojmenovávat prvky a sloučeniny.
- Uživatel se může naučit pojmenovávat celou periodickou tabulku prvků a také až 12 kategorií sloučenin.
- Aplikaci jsem vytvořil ne z důvodu, že bych osobně měl rád chemii, ale tato myšlenka mi přišla zajímavá a můj kamarád (který se tomuto tématu věnuje) mi vnuknul nápad přidat tam kromě prvků i sloučeniny, a tak se zrodila ta myšlenka to vytvořit.

## Funkce

Popis hlavních funkcí aplikace:

- Součástí aplikace je periodická tabulka, kde uživatel může kliknout na nějaké prvky a ty se tím označí a přidají do seznamu, ze kterého bude uživatel zkoušen. Součástí jsou také tlačítka, která výběr uživateli urychlí.
- Následně aplikace obsahuje seznam kategorií, a v každé kategorii příslušné sloučeniny. Kliknutím na sloučeninu ji uživatel vybere. Zde jsou u každé kategorie také k dispozici tlačítka pro rychlejší výběr.
- Dále je v aplikaci nastavení, kde je možné nastavit, jaké typy otázek budou v následně vytvořeném kvízu a kolik otázek uživatel dostane, než se kvíz zavře a znovu se objeví obrazovka výběru. Je možné si také nastavit neomezený počet otázek.
- Po kliknutí na tlačítko se spustí kvíz. Kvíz obsahuje **tři typy otázek**:
    - **ano/ne otázka**: uživatel se musí rozhodnout, zda jemu předložené tvrzení je pravdivé kliknutím na tlačítka: *pravda* nebo *nepravda*.
    > Např.: \
    > **Otázka**: *Patří <ins>H</ins> k <ins>vodíku</ins>?* \
    > **Možnosti**: *pravda* nebo *nepravda*

    - **vybírací otázka**: uživatel dostane na výběr ze čtyř možností odpovědi a musí vybrat tu správnou.
    > Např.: \
    > **Otázka**: *Vyber značku prvku <ins>vodík</ins>.* \
    > **Možnosti**: *C*, *H*, *Fe*, *Al*

    - **psací otázka**: uživatel dostane prvek nebo sloučeninu a musí napsat její název nebo vzorec.
    > Např.: \
    > **Otázka**: *Napiš značku prvku <ins>železo</ins>.* \
    > **Odpověď**: *Fe*

- Po zodpovězení otázky program okamžitě vyhodnotí odpověď a sdělí ji uživateli. Pokud odpověď nebyla správná, program zobrazí i správnou odpověď. U psací otázky se zobrazí i procento shody se správnou odpovědí (zde není třeba psát dolní index).
- V průběhu zkoušení si uživatel může zobrazit různé údaje o svém výkonu a nastavení otázek přes kliknutí na tlačítko *statistiky*.
- Na hlavních obrazovkách aplikace je dostupná nabídka pro výběr jednoho ze 13 podporovaných jazyků. Po změně jazyka se všechny přeložitelné části aktuální obrazovky okamžitě aktualizují.

## Jak aplikace funguje

Popis běžného průchodu aplikací:

1. Uživatel otevře úvodní obrazovku, kde uvidí pozdrav a klikne na tlačítko, které ho přesune na další obrazovku.
2. Zde si z periodické tabulky prvků vybere prvky a z kategorií sloučenin si vybere příslušné sloučeniny.
3. Nastaví si typy otázek, které chce dostávat a také nastaví kolik chce otázek.
4. Spustí kvíz kliknutím na další tlačítko.
5. Aplikace generuje různé otázky a uživatel na ně odpovídá.
6. Výsledky ukládá do statistik, kde si je uživatel může prohlédnout.

## Struktura projektu

| Soubor nebo složka                  | Účel                                                                                             |
| ----------------------------------- | ------------------------------------------------------------------------------------------------ |
| `project.py`                        | Vstupní bod aplikace, hlavní třída `ChemistryQuiz`, globální stav a testovatelné pomocné funkce. |
| `screens/welcome/`                  | Úvodní obrazovka aplikace.                                                                       |
| `screens/choice/choice.py`          | Řídí obrazovku výběru, přepínání jazyka a jednotlivé záložky.                                    |
| `screens/choice/periodic_table.py`  | Vykresluje interaktivní periodickou tabulku a zpracovává výběr prvků.                            |
| `screens/choice/compounds.py`       | Umožňuje vybírat kategorie a jednotlivé sloučeniny.                                              |
| `screens/choice/quiz_settings.py`   | Nastavení typů otázek a délky kvízu.                                                             |
| `screens/quiz/quiz.py`              | Řídí průběh kvízu, načítání dalších otázek a statistiky.                                         |
| `screens/quiz/question_types/`      | Implementace boolean, choice a typing otázek.                                                    |
| `screens/quiz/random_question.py`   | Náhodně vybírá typ otázky a její chemické položky.                                               |
| `screens/quiz/statistics_screen.py` | Zobrazuje průběžné statistiky odpovědí, vybrané položky, povolené typy otázek a zbývající počet otázek.                                                 |
| `data/database.py`                  | Načítá chemická a jazyková data z JSON souborů.                                                  |
| `data/locales/`                     | Překladové soubory a překladový systém.                                                          |
| `utils/translatable_widgets.py`     | Vlastní Textual widgety schopné měnit jazyk za běhu.                                             |
| `*.tcss`                            | Rozložení a vzhled jednotlivých obrazovek.                                                       |
| `requirements.txt`                  | Závislosti instalované přes `pip`.                                                               |
| `test_project.py`                   | Testy funkcí požadovaných CS50P.                                                                 |


## Překladový systém

Zprvu to byl malý soubor, který jen překládal podle obrazovky, slova a jazyka. Postupem času ale bylo potřeba přidat více funkcí, takže je překladový systém nakonec mnohem složitější, než jsem původně čekal.

### Třída `Translate`

- Jako první se vytvoří třída `Translate`, do které můžeme vložit argument `language`, který udává jazyk a ve výchozím nastavení je nastaven na angličtinu. Jako platný vstup se považuje pouze zkratka podporovaného jazyka.
- Tato třída má svou metodu `t` (jako translate), která má argumenty:
    1. **word**: překladový klíč nebo složený text, který má metoda zpracovat. Může být buď jako obyčejný `str`, nebo můžeme předat `tuple`. V tomto případě to musíme uvádět v tomto formátu:
    ```python
    (
        ("w", "some_word"),
        ("n", "some_note"),
        ("w", "some_other_word")
    )
    ```
    **w – slovo**: slovo, které bude přeloženo. Musí být platné slovo, jinak metoda vyvolá chybu.\
    **n – nepřekládaný text**: Znamená to, že metoda tento text nebude překládat a vloží jej přímo do výsledku.
    Ke konci se všechny tyto části spojí.\
    2. **screen**: obrazovka, ke které dotyčné slovo patří. Pokud je slovo platné, ale obrazovka špatná a naopak, metoda vyvolá chybu.\
    3. **description**: Tento argument je volitelný. Označuje, že když je v textu např. `<1>` má se to nahradit nějakým prvkem, nebo sloučeninou. Je jedno, jestli `word` byl `str` nebo `tuple`. Tato metoda se vztahuje na nepřekládané části i samotná slova.\
    Např.:
    ```python
    Translate(language="cs").t(
        word="symbol_of_element",
        screen="quiz",
        description={
            "1": {
                "type": "element",
                "item": "Fe",
                "appearance": "name"
            }
        }
    )
    ```
    Výstup: `"Jaká je značka prvku [u]železo[/]?"`

### Jazykové JSON soubory

- Jsou uložené ve složkách: `data/locales/ui/screens/<screen>/<language>.json`
- Každý soubor obsahuje jeden velký slovník, kde jsou jako klíče obecné názvy a jako hodnoty konkrétní názvy které uvidí uživatel v nastaveném jazyce.

### Vlastní překladové widgety

Dále jsem potřeboval vyřešit problém s tím, když chci přeložit všechny widgety. Bylo by hloupé přepisovat při překladu na každé obrazovce každý widget zvlášť, tak jsem udělal widgety, které se samy překládají.

- Nacházejí se v `utils/translatable_widgets.py`
- Hlavní je `TransMixin`, který má obecné vlastnosti všech widgetů, jako je třeba přijímaní a ukládání argumentů: `word` a `description`. Jednotlivé widgety si svoji obrazovku zjistí samy podle toho, kde se nacházejí.
- Následně každý typ widgetu dědí ze svého widgetu z Textualu a taky právě z `TransMixin`.
- Každý widget má svou metodu `update_language`, která aktualizuje obsah tohoto widgetu na právě změněný jazyk a jeho slovo. Způsob změnění každého widgetu je trochu jiný, a proto má každý widget svou vlastní metodu překladu.
- Takže každý widget si pamatuje informace o sobě a při překladu stačí zavolat metodu `update_language` pro všechny potomky `TransMixin` a překlad je hotový.


## Generování kvízových otázek

- Aplikace generuje náhodné otázky pomocí funkce random_question() v souboru random_question.py. Tato funkce vybere náhodný typ otázky a vrátí potřebné informace pro její zobrazení a vyhodnocení.
- Po každé otázce `quiz.py` zcela vymaže poslední otázku, nechá `random_question.py` vygenerovat nové informace a podle toho vytvoří novou otázku.
- Každý typ otázky je pouze speciální `Container`, který dostane informace, zobrazí otázku, posoudí odpověď, uloží výsledky, odešle zprávu do `QuizScreen` a ten otázku smaže a vytvoří další.

## Návrhová rozhodnutí

- **Textual**: Vybral jsem ho, protože jsem už zkoušel *PyQt6*, ale připadal mi moc těžký, a tak jsem si říkal, že bych mohl zkusit TUI. A je pravda, že práce s tímto frameworkem není úplně lehká, ale rozhodně lehčí než PyQt6.
- Aplikaci jsem rozdělil na tři různé obrazovky a jedno modální okno se statistikami kvůli přehlednosti. Jednotlivé části aplikace jsou tak oddělené a lze mezi nimi jednoduše přecházet.
- Potřeboval jsem nějak uložit ta všechna data, a tak jsem zvolil JSON. Na něco by lépe sedělo CSV, ale když už, tak jsem to všechno udělal s JSON.
- Abych mohl někde univerzálně ukládat data mezi obrazovkami, vytvořil jsem dataclass `AppState`.
- Zpočátku jsem společný překladový kód opakoval v každém vlastním widgetu. Později jsem to vylepšil a přesunul jsem jej do mixinu `TransMixin`, čímž jsem omezil duplicitu podle principu DRY.
- Chtěl jsem, aby každá otázka byla oddělená od všeho ostatního a aby plnila jen svůj úkol. Pak mi přišlo praktické je prostě udělat jednorázové. A ano, je to velmi praktické.

### Vývojové problémy

Při vývoji bylo obtížnější sledovat stav aplikace, protože běžné použití
funkce `print()` není v terminálovém uživatelském rozhraní příliš
praktické.

Nejvíce problémů mi způsobovalo TCSS. Některé selektory se uplatňovaly
také na widgety na jiných obrazovkách, což vedlo k jejich neočekávanému
mizení nebo změnám rozložení. Problém jsem vyřešil omezením selektorů
na konkrétní obrazovky.

## Instalace

Aplikace vyžaduje Python 3.10 nebo novější. Vyvíjena a testována byla
s následujícími verzemi:

- Python 3.14.6
- Textual 5.3.0
- textual-pyfiglet 1.1.0

Po stažení projektu otevřete terminál v jeho kořenové složce a nainstalujte
potřebné závislosti:

```bash
python -m pip install -r requirements.txt
```

Aplikaci následně spusťte příkazem:

```bash
python project.py
```

## Ovládání a použití

Přestože je to aplikace v terminálu, TUI aplikace se dá v pohodě ovládat myší. Ve kvízové obrazovce jsem přidal ovládání klávesnicí pro pohodlí. Klávesové zkratky se zobrazují v dolní liště v kvízové obrazovce.

## Budoucí vylepšení

Někdy v budoucnu bych chtěl ještě přidat:

- Ne jen náhodné otázky, ale otázky, kde uživatel udělal chybu. Nebo aby se aspoň otázky co nejméně opakovaly.
- Možná více typů otázek.
- Možná více jazyků.

## Zdroje

### Knihovny a frameworky

- `Textual` 5.3.0 – tvorba terminálového uživatelského rozhraní
- `textual-pyfiglet` 1.1.0 – vykreslování animovaných ASCII nadpisů

### Chemická a jazyková data

- ChatGPT – pomoc při sestavování chemických dat, překladů a kontrole dokumentace
