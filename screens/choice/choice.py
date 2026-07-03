from textual.screen import Screen
from textual.widgets import Button, Static
from textual.containers import Container

from data.database import periodic_table

class ChoiceScreen(Screen):
    CSS_PATH = "choice.tcss"

    def compose(self):
        yield Container(id="grid")

    def on_mount(self) -> None:
        for row in periodic_table:
            for element in row:
                if element is None:
                    self.query_one("#grid", Container).mount(Static())
                else: # type(element) is str
                    self.query_one("#grid", Container).mount(Button(element, id=element.lower(), classes="element"))