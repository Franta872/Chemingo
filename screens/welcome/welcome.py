# TEXTUAL imports
from textual.screen import Screen
from textual.widgets import Button, Select
from textual.containers import Horizontal
# APP imports
from data.database import all_languages_select
from utils.translatable_widgets import TransLabel, TransButton, TransFigletWidget

class WelcomeScreen(Screen):
    CSS_PATH = "welcome.tcss"
    NAME = "welcome"

    def compose(self):
        yield TransLabel("language")
        yield Select(all_languages_select, allow_blank=False)

        yield TransFigletWidget(
            "welcome",
            colors=["#00ff88", "#00aaff"],
            animate=True,
            font="doom",
            id="figlet1"
        )
        yield TransFigletWidget(
            "slogan",
            colors=["#ff0000", "#ffdd00"],
            animate=True,
            font="threepoint",
            animation_type="smooth_strobe",
            id="figlet2"
        )
        yield Horizontal(
            TransButton("choose_topic", variant="primary")
            )
        
    def on_select_changed(self, event: Select.Changed):
        """Update the active language and refresh translated widgets."""
        self.app.translate.language = event.value
        for widget in self.query("TransLabel, TransButton, TransFigletWidget"):
            widget.update_language()
        
    def on_button_pressed(self, event: Button.Pressed):
        self.app.push_screen("choice")