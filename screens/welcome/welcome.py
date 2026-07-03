from textual.screen import Screen
from textual.widgets import Button, Header, Select
from textual.containers import Horizontal
from textual_pyfiglet import FigletWidget

# path from the main file
from data.database import all_languages_select

from utils.translatable_widgets import TransLabel, TransButton, TransFigletWidget

class WelcomeScreen(Screen):
    CSS_PATH = "welcome.tcss"

    def compose(self):
        st = "welcome", self.app.translate

        yield Header()

        yield TransLabel("language", *st)
        yield Select(all_languages_select, allow_blank=False)

        yield TransFigletWidget(
            "welcome",
            *st,
            colors=["#00ff88", "#00aaff"],
            animate=True,
            font="doom"
    )
        yield Horizontal(
            TransButton("choose_topic", *st, variant="primary")
            )
        
    def on_select_changed(self, event: Select.Changed):
        self.app.translate.language = event.value
        for widget in self.query("TransLabel, TransButton, TransFigletWidget"):
            widget.update_language()
        
    def on_button_pressed(self, event: Button.Pressed):
        ...