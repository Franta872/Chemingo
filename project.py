# TEXTUAL imports
from textual.app import App
# PYTHON import
from dataclasses import dataclass, field
# APP imports
# from folder.folder.file import class
from screens.welcome.welcome import WelcomeScreen
from screens.choice.choice import ChoiceScreen
from data.locales.ui.translation import Translate

@dataclass
class AppState:
    """
    Main app class for storing data among the screens.
    """
    selected_elements: set[str] = field(default_factory=set)


class ChemistryQuiz(App):
    SCREENS = {
        "welcome": WelcomeScreen,
        "choice": ChoiceScreen
    }

    def on_mount(self):
        self.translate = Translate("en")

        self.state = AppState()
        self.push_screen("welcome")


def is_blank(dictionary: dict[str, list]):
    """
    This function check if a dictionary is completely blank.
    """
    #This function doesn't fit in this file, but it's here because of 
    #the conditions of the CS50P final project.
    for item in dictionary.values():
        if item != []:
            return False
    return True

def main(): # this is useless, but it's here because of the
            # conditions of the CS50P final project.
    ChemistryQuiz().run()

if __name__ == "__main__":
    main()