from textual.screen import Screen
from textual.widgets import Button, Label, Header, Select
from textual_pyfiglet import FigletWidget
from textual.containers import Horizontal

# path from the main file
from screens.welcome.language_select import all_languages

class WelcomeScreen(Screen):
    CSS_PATH = "welcome.tcss"

    def compose(self):
        yield Header()

        yield Label("Language: ")
        yield Select(all_languages(), allow_blank=False)

        yield FigletWidget(
            "Welcome to Chemingo!",
            colors=["#00ff88", "#00aaff"],
            animate=True,
            font="doom"
    )
        yield Horizontal(
            Button("Choose a topic!", variant="primary")
            )
        
    def on_button_pressed(self, event: Button.Pressed):
        ...