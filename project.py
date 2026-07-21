# TEXTUAL imports
from textual.app import App
# PYTHON import
from dataclasses import dataclass, field
# APP imports
# from folder.folder.file import class
from screens.welcome.welcome import WelcomeScreen
from screens.choice.choice import ChoiceScreen
#from screens.quiz.quiz import QuizScreen
from data.locales.ui.translation import Translate
from data.database import compounds_categories

@dataclass
class AppState:
    """
    Main app class for storing data among the screens.
    """
    selected_elements: set[str] = field(default_factory=set)
    selected_compounds: dict[str, set] = field(
        default_factory=lambda: {x: set() for x in compounds_categories.keys()}
        )
    question_answers: dict[str, bool] = field(default_factory=dict)
    num_of_questions: int|float = 5

class ChemistryQuiz(App):
    SCREENS = {
        "welcome": WelcomeScreen,
        "choice": ChoiceScreen
        # a new instance of a QuizScreen is made every time you enter it
    }

    def on_mount(self):
        self.translate = Translate("en")

        self.state = AppState()
        self.push_screen("welcome")


def is_blank_dictionary(dictionary: dict[str, list]| dict[str, bool]):
    """
    This function check if a dictionary's lists are completely blank or if 
    the dictionary stores all ```False``` values.
    """
    #This function doesn't fit in this file, but it's here because of 
    #the conditions of the CS50P final project.
    for item in dictionary.values():
        if (isinstance(item, list) and item != []) or (isinstance(item, bool) and item):
            return False
    return True

def count_dictionary_list_items(dictionary: dict[str, list|set|tuple]) -> int:
    num = 0
    for value in dictionary.values():
        num += len(value)
    return num

def main(): # this is useless, but it's here because of the
            # conditions of the CS50P final project.
    ChemistryQuiz().run()

if __name__ == "__main__":
    main()