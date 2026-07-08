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



if __name__ == "__main__":
    ChemistryQuiz().run()