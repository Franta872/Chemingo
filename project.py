# TEXTUAL imports
from textual.app import App
from textual.widgets import Header, Footer
# PYTHON import
from dataclasses import dataclass
# APP import
# from folder.folder.file import class
from screens.welcome.welcome import WelcomeScreen
from screens.choice.choice import ChoiceScreen
from data.locales.ui.translation import Translate

@dataclass
class AppState:
    ...

class ChemistryQuiz(App):
    SCREENS = {
        "welcome": WelcomeScreen,
        "choice": ChoiceScreen
    }

    def compose(self):
        yield Header()
        yield Footer()

    def on_mount(self):
        self.translate = Translate("en")

        self.state = AppState()
        self.push_screen("welcome")



if __name__ == "__main__":
    ChemistryQuiz().run()