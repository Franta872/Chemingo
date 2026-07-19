# PYTHON import
from typing import TYPE_CHECKING

from textual.widget import Widget
if TYPE_CHECKING:
    from typing import Literal
# TEXTUAL imports
if TYPE_CHECKING:
    from textual.screen import Screen
    from textual.app import ComposeResult
from utils.translatable_widgets import TransButton, TransLabel
from textual.containers import Container, HorizontalGroup
from textual.message import Message
from textual import on

class BooleanQuestion(Container):
    def __init__(self,
                quiz_screen: Screen,
                type_1: Literal["element", "compound"], 
                item_1: str, 
                appearance_1: Literal["symbol", "name"], 
                type_2: Literal["element", "compound"], 
                item_2: str, 
                appearance_2: Literal["symbol", "name"],
                answer: bool = True, 
                *children: Widget,
                **kwargs) -> None:

        self.quiz_screen = quiz_screen
        self.type_1 = type_1
        self.item_1 = item_1
        self.appearance_1 = appearance_1
        self.type_2 = type_2
        self.item_2 = item_2
        self.appearance_2 = appearance_2
        self.answer = answer

        super().__init__(*children, **kwargs)
    
    def compose(self) -> ComposeResult:
        st = "quiz", self.quiz_screen.app.translate  # type: ignore[attr-defined]
        label_text = {
                "1": {
                "type": self.type_1,
                "item": self.item_1,
                "appearance": self.appearance_1,
                },
                "2": {
                "type": self.type_2,
                "item": self.item_2,
                "appearance": self.appearance_2,
                }
            }

        with Container(id="label-container"):
            yield TransLabel("boolean_question_text", *st, label_text)
        with HorizontalGroup(id="input-container"):
            yield TransButton("true", *st, variant="success", id="true")
            yield TransButton("false", *st, variant="error", id="false")
    
    class UserAnswered(Message):
        def __init__(self, value: Literal["correct", "wrong"]) -> None:
            self.value = value
            super().__init__()

    def on_button_pressed(self, event: TransButton.Pressed):
        if event.button.id in ("true", "false"):
            st = "quiz", self.quiz_screen.app.translate  # type: ignore[attr-defined]
            input_container = self.query_one("#input-container", HorizontalGroup)
            input_container.remove_children()
            if (event.button.id == "true" and self.answer) or (event.button.id == "false" and not self.answer):
                # correct
                input_container.mount(
                    TransButton((
                        ("w", "correct"),
                        ("n", "\n\n[not bold]"),
                        ("w", "your_answer"),
                        ("n", f": {st[1].t(event.button.id, st[0])}[/not bold]")
                    ),
                    *st,
                    variant="success",
                    id="answer-button")
                )
                self.users_answer = True
            else: # (event.button.id == "true" and not self.answer) or (event.button.id == "false" and self.answer):
                # wrong
                input_container.mount(
                    TransButton((
                        ("w", "wrong"),
                        ("n", "\n\n[not bold]"),
                        ("w", "your_answer"),
                        ("n", f": {st[1].t(event.button.id, st[0])}[/not bold]")
                    ),
                    *st,
                    variant="error",
                    id="answer-button")
                )
                self.users_answer = False

        elif event.button.id == "answer-button":
            if self.users_answer:
                self.post_message(self.UserAnswered("correct"))
            else: # not self.users_answer
                self.post_message(self.UserAnswered("wrong"))