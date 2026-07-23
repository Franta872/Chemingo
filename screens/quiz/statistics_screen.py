# PYTHON imports
from typing import TYPE_CHECKING
from math import isinf
# TEXTUAL imports
if TYPE_CHECKING:
    from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Tree
from textual.containers import Container
# APP imports
from utils.translatable_widgets import TransLabel, TransButton

class StatisticsScreen(ModalScreen):
    def compose(self) -> ComposeResult:
        st = "quiz", self.app.translate # type: ignore[attr-defined]
        with Container(id="statistics-container"):
            with Container(classes="statistics-center-container"):
                yield TransLabel("statistics", *st, id="statistics-label")
            tree: Tree[str] = Tree("")
            tree.root.add_leaf("♾️" if isinf(self.app.state.num_of_questions) else str(self.app.state.num_of_questions))
            tree.root.expand_all()
            yield tree

            with Container(classes="statistics-center-container"):
                yield TransButton("close", *st, id="close-button", variant="error")
    
    def on_button_pressed(self, event: TransButton.Pressed) -> None:
        if event.button.id == "close-button":
            self.app.pop_screen()