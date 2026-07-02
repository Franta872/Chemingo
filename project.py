# TEXTUAL imports
from textual.app import App
from textual.widgets import Header, Footer, Label, Button
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.reactive import reactive
# PYTHON import
from dataclasses import dataclass
# APP import
# from folder.folder.file import class
from screens.welcome.welcome import WelcomeScreen

@dataclass
class AppState:
    language: str = "en"

class ChemistryQuiz(App):
    CSS_PATH = "project.tcss"

    SCREENS = {
        "welcome": WelcomeScreen
    }

    def compose(self):
        yield Header()
        yield Footer()

    def on_mount(self):
        self.state = AppState()
        self.push_screen("welcome")



if __name__ == "__main__":
    ChemistryQuiz().run()