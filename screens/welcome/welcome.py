# TEXTUAL imports
from textual.screen import Screen
from textual.widgets import Button, Header, Select
from textual.containers import Horizontal

# APP imports
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
            font="doom",
            id="figlet1"
        )
        yield TransFigletWidget(
            "slogan",
            *st,
            colors=["#ff0000", "#ffdd00"],
            animate=True,
            font="threepoint",
            animation_type="smooth_strobe",
            id="figlet2"
        )
        yield Horizontal(
            TransButton("choose_topic", *st, variant="primary")
            )
        
    def on_select_changed(self, event: Select.Changed):
        """when user selects new language"""
        self.app.translate.language = event.value
        #sends a message to the Translation class, language has been changed
        for widget in self.query("TransLabel, TransButton, TransFigletWidget"):
            widget.update_language()
        #sends a message to all widgets in this screen, that they need to change language
        
    def on_button_pressed(self, event: Button.Pressed):
        self.app.push_screen("choice")