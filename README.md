# Chemingo

#### [Video Demo](https://youtu.be/d6RWccxthVU)

## Description

A short introduction to the application:

- Chemingo is an application where users select items from a list of elements and compounds, and the application then quizzes them on those items.
- The application is intended for people who want to practice or learn how to name elements and compounds.
- Users can learn the names and symbols of the entire periodic table, as well as compounds from up to 12 different categories.
- I did not create the application because I personally love chemistry. I created it because the idea seemed interesting to me, and my friend, who is interested in this subject, suggested adding compounds as well as elements. That is how the idea for Chemingo was born.

## Features

A description of the application's main features:

- The application contains an interactive periodic table. Users can click on elements to select them and add them to the list of items they will be quizzed on. There are also buttons that make selecting elements faster.
- The application also contains a list of categories with their corresponding compounds. Users can select a compound by clicking on it. Each category also has buttons for faster selection.
- The settings allow users to choose which question types will appear in the quiz and how many questions they will receive before the quiz closes and the selection screen appears again. It is also possible to choose an unlimited number of questions.
- Clicking the button starts the quiz. The quiz contains **three question types**:
    - **true/false question**: the user must decide whether the displayed statement is true by clicking either *true* or *false*.
    > Example: \
    > **Question**: *Does <ins>H</ins> correspond to <ins>hydrogen</ins>?* \
    > **Options**: *true* or *false*

    - **multiple-choice question**: the user chooses the correct answer from four options.
    > Example: \
    > **Question**: *Select the symbol of the element <ins>hydrogen</ins>.* \
    > **Options**: *C*, *H*, *Fe*, *Al*

    - **typing question**: the user is shown an element or compound and must type its name, symbol, or formula.
    > Example: \
    > **Question**: *Write the symbol of the element <ins>iron</ins>.* \
    > **Answer**: *Fe*

- After a question is answered, the program immediately evaluates the answer and tells the user whether it was correct. If the answer was incorrect, the program also displays the correct answer. Typing questions also show the percentage of similarity to the correct answer. Subscripts do not have to be typed.
- During the quiz, users can open the *statistics* screen to see information about their performance and the current question settings.
- A language selection menu is available on the application's main screens. Users can choose any of the 13 supported languages, and all translatable parts of the current screen update immediately.

## How the Application Works

A description of a normal walkthrough of the application:

1. The user opens the welcome screen, sees a greeting, and clicks a button to continue to the next screen.
2. The user selects elements from the periodic table and compounds from the available categories.
3. The user chooses which question types they want to receive and sets the number of questions.
4. The user starts the quiz by clicking another button.
5. The application generates different questions, and the user answers them.
6. The results are stored in the statistics, where the user can view them.

## Project Structure

| File or directory                    | Purpose                                                                                                              |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------- |
| `project.py`                         | The application's entry point, the main `ChemistryQuiz` class, shared state, and testable helper functions.          |
| `screens/welcome/`                   | The application's welcome screen.                                                                                    |
| `screens/choice/choice.py`           | Controls the selection screen, language switching, and its individual tabs.                                          |
| `screens/choice/periodic_table.py`   | Renders the interactive periodic table and handles element selection.                                                 |
| `screens/choice/compounds.py`        | Allows users to select compound categories and individual compounds.                                                 |
| `screens/choice/quiz_settings.py`    | Contains the question type and quiz length settings.                                                                 |
| `screens/quiz/quiz.py`               | Controls the quiz, loads new questions, and manages statistics.                                                       |
| `screens/quiz/question_types/`       | Contains the implementations of boolean, multiple-choice, and typing questions.                                      |
| `screens/quiz/random_question.py`    | Randomly selects the question type and its chemical items.                                                            |
| `screens/quiz/statistics_screen.py`  | Displays current answer statistics, selected items, enabled question types, and the number of remaining questions.   |
| `data/database.py`                   | Loads chemical and language data from JSON files.                                                                    |
| `data/locales/`                      | Contains the translation files and translation system.                                                               |
| `utils/translatable_widgets.py`      | Contains custom Textual widgets that can change language at runtime.                                                  |
| `*.tcss`                             | Defines the layout and appearance of the individual screens.                                                         |
| `requirements.txt`                   | Contains the dependencies installed using `pip`.                                                                     |
| `test_project.py`                    | Contains tests for the functions required by CS50P.                                                                  |

## Translation System

At first, it was a small file that only translated text based on the screen, word, and language. Over time, I needed to add more features, so the translation system ended up much more complicated than I originally expected.

### The `Translate` Class

- First, an instance of the `Translate` class is created. It can receive a `language` argument, which determines the active language and is set to English by default. Only the code of a supported language is considered valid.
- This class has a method named `t` (short for translate), which accepts the following arguments:
    1. **word**: a translation key or composed text that the method should process. It can be passed as a normal `str`, or as a `tuple`. In that case, it must use the following format:
    ```python
    (
        ("w", "some_word"),
        ("n", "some_note"),
        ("w", "some_other_word")
    )
    ```
    **w – word**: a translation key that will be translated. It must be valid, otherwise the method raises an error.\
    **n – untranslated text**: the method does not translate this text and inserts it directly into the result.\
    In the end, all of these parts are joined together.\
    2. **screen**: the screen to which the given word belongs. If the word is valid but the screen is incorrect, or the other way around, the method raises an error.\
    3. **description**: this argument is optional. It specifies that a placeholder such as `<1>` should be replaced with an element or compound. It does not matter whether `word` was a `str` or a `tuple`. The replacement also works inside untranslated parts of the text.\
    Example:
    ```python
    Translate(language="en").t(
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
    Output: `"What is the symbol of the element [u]iron[/]?"`

### Language JSON Files

- They are stored in: `data/locales/ui/screens/<screen>/<language>.json`
- Each file contains one large dictionary where the keys are internal names and the values are the actual texts shown to the user in the selected language.

### Custom Translatable Widgets

I also needed to solve the problem of translating all widgets. Rewriting every widget separately on every screen whenever the language changed would be stupid, so I created widgets that translate themselves.

- They are located in `utils/translatable_widgets.py`.
- The main part is `TransMixin`, which contains the shared properties of all translatable widgets, such as receiving and storing the `word` and `description` arguments. Each widget finds its screen automatically based on where it is located.
- Each widget type then inherits from its original Textual widget as well as from `TransMixin`.
- Every widget has its own `update_language` method, which updates its contents to the currently selected language. The way each widget changes is slightly different, so each widget type has its own translation method.
- This means that every widget remembers its own information, and changing the language only requires calling `update_language` for every descendant of `TransMixin`.

## Generating Quiz Questions

- The application generates random questions using the `random_question()` function in `random_question.py`. This function selects a random question type and returns the information needed to display and evaluate it.
- After every question, `quiz.py` completely removes the previous question, asks `random_question.py` to generate new information, and creates a new question from it.
- Each question type is a special `Container`. It receives the necessary information, displays the question, evaluates the answer, stores the results, sends a message to `QuizScreen`, and is then removed while the next question is created.

## Design Choices

- **Textual**: I chose it because I had already tried *PyQt6*, but it seemed too difficult, so I thought I could try making a TUI instead. Working with this framework is not exactly easy either, but it is definitely easier than PyQt6.
- I divided the application into three different screens and one modal statistics window to keep everything organized. The individual parts of the application are separated, and it is easy to move between them.
- I needed a way to store all the data, so I chose JSON. CSV might have been a better fit for some parts, but since I was already using JSON, I used it for everything.
- To store data shared between screens in one place, I created the `AppState` dataclass.
- At first, I repeated the shared translation code inside every custom widget. Later, I improved it and moved the code into the `TransMixin` mixin, reducing duplication according to the DRY principle.
- I wanted every question to be separate from everything else and to perform only its own task. Then it seemed practical to make the questions disposable, one-time widgets. And yes, it is very practical.

### Development Problems

It was more difficult to monitor the application's state during development because using the `print()` function is not very practical inside a terminal user interface.

TCSS caused me the most problems. Some selectors also applied to widgets on other screens, which caused them to disappear unexpectedly or changed their layout. I solved this by limiting the selectors to specific screens.

## Installation

The application requires Python 3.10 or newer. It was developed and tested with the following versions:

- Python 3.14.6
- Textual 5.3.0
- textual-pyfiglet 1.1.0

After downloading the project, open a terminal in its root directory and install the required dependencies:

```bash
python -m pip install -r requirements.txt
```

Then run the application using:

```bash
python project.py
```

## Controls and Usage

Although it runs in a terminal, the TUI application can be comfortably controlled with a mouse. I also added keyboard controls to the quiz screen for convenience. The keyboard shortcuts are displayed in the footer of the quiz screen.

## Future Improvements

In the future, I would like to add:

- Questions based on the user's previous mistakes instead of only random questions, or at least a way to prevent the same questions from repeating too often.
- Possibly more question types.
- Possibly more languages.

## Sources

### Libraries and Frameworks

- `Textual` 5.3.0 – used to create the terminal user interface
- `textual-pyfiglet` 1.1.0 – used to render animated ASCII headings

### Chemical and Language Data

- ChatGPT – helped with compiling the chemical data, translations, and checking the documentation
