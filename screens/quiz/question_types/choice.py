# PYTHON import
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Literal
# TEXTUAL imports
from textual.app import ComposeResult
from textual.containers import Container, HorizontalGroup
from textual.widget import Widget
from textual.message import Message
if TYPE_CHECKING:
    from textual.screen import Screen
    from textual.app import ComposeResult
# APP import
from utils.translatable_widgets import TransButton, TransLabel

class ChoiceQuestion(Container):
    def __init__(
            self, 
            quiz_screen: Screen,
            asked: dict[str, str],
            item_1: dict[str, str],
            item_2: dict[str, str],
            item_3: dict[str, str],
            item_4: dict[str, str],
            *children: Widget, 
            **kwargs
            ) -> None:
        self.quiz_screen = quiz_screen
        self.asked = asked
        self.item_1 = item_1
        self.item_2 = item_2
        self.item_3 = item_3
        self.item_4 = item_4
        super().__init__(*children, **kwargs)

    def compose(self) -> ComposeResult:
        st = "quiz", self.quiz_screen.app.translate  # type: ignore[attr-defined]
        with Container(id="label-container"):
            yield TransLabel("which_one", *st, {"1": self.asked})
        with HorizontalGroup(id="input-container"):
            yield TransButton((("n", "<1>",),), *st, {"1": self.item_1}, variant="warning", classes="choice-button", id="choice-button-1")
            yield TransButton((("n", "<2>",),), *st, {"2": self.item_2}, variant="error", classes="choice-button", id="choice-button-2")
            yield TransButton((("n", "<3>",),), *st, {"3": self.item_3}, variant="success", classes="choice-button", id="choice-button-3")
            yield TransButton((("n", "<4>",),), *st, {"4": self.item_4}, variant="primary", classes="choice-button", id="choice-button-4")

    class UserAnswered(Message):
        def __init__(self, value: Literal["correct", "wrong"]) -> None:
            self.value = value
            super().__init__()

    def on_button_pressed(self, event: TransButton.Pressed):
        if event.button.has_class("choice-button"):
            st = "quiz", self.quiz_screen.app.translate # type: ignore[attr-defined]
            input_container = self.query_one("#input-container", HorizontalGroup)
            input_container.remove_children()
            if event.button.description[event.button.id[-1]]["item"] == self.asked["item"]:
                # correct
                input_container.mount(
                    TransButton((
                        ("w", "correct"),
                        ("n", "\n\n[not bold]"),
                        ("w", "your_answer"),
                        ("n", ": [u]<1>[/u][/not bold]")
                    ),
                    *st,
                    {"1": event.button.description[event.button.id[-1]]},
                    variant="success",
                    id="answer-button")
                )
                self.users_answer = True
            else: 
                # wrong
                input_container.mount(
                    TransButton((
                        ("w", "wrong"),
                        ("n", "\n\n[not bold]"),
                        ("w", "your_answer"),
                        ("n", ": [u]<1>[/u]\n"),
                        ("w", "correct_answer"),
                        ("n", ": [u]<2>[/u][/not bold]")
                    ),
                    *st,
                    {"1": event.button.description[event.button.id[-1]],
                     "2": self.asked | {"appearance": self.item_1["appearance"]}},
                    variant="error",
                    id="answer-button")
                )
                self.users_answer = False

        elif event.button.id == "answer-button":
            if self.users_answer:
                self.post_message(self.UserAnswered("correct"))
            else: # not self.users_answer
                self.post_message(self.UserAnswered("wrong"))