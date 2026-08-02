# PYTHON import
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Literal
# TEXTUAL imports
if TYPE_CHECKING:
    from textual.widget import Widget
    from textual.app import ComposeResult
from utils.translatable_widgets import TransButton, TransLabel
from textual.containers import Container, HorizontalGroup
from textual.message import Message

class BooleanQuestion(Container):
    BINDINGS = [
        ("1", "true", "✅"),
        ("enter", "true"),
        ("2", "false", "❌"),
        ("escape", "false"),
        ("enter", "next_question", "➡️")
    ]
    can_focus = True

    def __init__(self,
                dict_1: dict[str, str],
                dict_2: dict[str, str],
                answer: bool = True, 
                *children: Widget,
                **kwargs
                ) -> None:

        self.type_1 = dict_1["type"]
        self.item_1 = dict_1["item"]
        self.appearance_1 = dict_1["appearance"]
        self.type_2 = dict_2["type"]
        self.item_2 = dict_2["item"]
        self.appearance_2 = dict_2["appearance"]
        self.answer = answer

        super().__init__(*children, **kwargs)
    
    def compose(self) -> ComposeResult:
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
            yield TransLabel("boolean_question_text", label_text)
        with HorizontalGroup(id="input-container"):
            yield TransButton("true", variant="success", id="true")
            yield TransButton("false", variant="error", id="false")

    def on_mount(self):
        self.focus()
    
    class UserAnswered(Message):
        def __init__(self, value: Literal["correct", "wrong"]) -> None:
            self.value = value
            super().__init__()

    def action_true(self):
        self.process_answer(True)
    def action_false(self):
        self.process_answer(False)
    def action_next_question(self):
        self.next_question()

    def check_action(
        self, action: str, parameters: tuple[object, ...]
        ) -> bool:
        """Check if an action may run."""
        if action in ("true", "false"):
            return bool(self.query("#true, #false"))
        elif action == "next_question":
            return bool(self.query("#answer-button"))
        return True

    def process_answer(self, answer: bool) -> None:
        input_container = self.query_one("#input-container", HorizontalGroup)
        input_container.remove_children()
        self.refresh_bindings()
        if (answer and self.answer) or (not answer and not self.answer): # correct answer
            input_container.mount(
                TransButton((
                    ("w", "correct"),
                    ("n", "\n\n[not bold]"),
                    ("w", "your_answer"),
                    ("n", f": {self.app.translate.t(str(answer).lower(), "quiz")}[/not bold]")
                ),
                variant="success",
                id="answer-button")
            )
            self.users_answer = True
        else: # wrong answer
            input_container.mount(
                TransButton((
                    ("w", "wrong"),
                    ("n", "\n\n[not bold]"),
                    ("w", "your_answer"),
                    ("n", f": {self.app.translate.t(str(answer).lower(), "quiz")}[/not bold]")
                ),
                variant="error",
                id="answer-button")
            )
            self.users_answer = False

    def next_question(self) -> None:
        statistics = self.app.state.statistics # type: ignore[attr-defined]
        if self.users_answer:
            statistics["correct"] += 1
            statistics["boolean"]["correct"] += 1
            self.post_message(self.UserAnswered("correct"))
        else: # not self.users_answer
            statistics["wrong"] += 1
            statistics["boolean"]["wrong"] += 1
            self.post_message(self.UserAnswered("wrong"))
    
    def on_button_pressed(self, event: TransButton.Pressed) -> None:
        if event.button.id in ("true", "false"):
            self.process_answer(event.button.id == "true")
        elif event.button.id == "answer-button":
            self.next_question()