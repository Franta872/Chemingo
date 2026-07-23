# PYTHON imports
from typing import TYPE_CHECKING
from difflib import SequenceMatcher
if TYPE_CHECKING:
    from typing import Literal
# TEXTUAL imports
from textual.app import ComposeResult
from textual.containers import Container, HorizontalGroup
from textual.widget import Widget
from textual.widgets import Button
from textual.message import Message
from textual import on
if TYPE_CHECKING:
    from textual.screen import Screen
    from textual.app import ComposeResult
# APP import
from utils.translatable_widgets import TransLabel, TransInput, TransButton

class TypingQuestion(Container):
    def __init__(self,
                quiz_screen: Screen,
                answer: dict[str, str], 
                item: dict[str, str],
                *children: Widget,
                **kwargs) -> None:

        self.quiz_screen = quiz_screen
        self.item = item
        self.answer = answer

        super().__init__(*children, **kwargs)

    def compose(self) -> ComposeResult:
        st = "quiz", self.app.translate # type: ignore[attr-defined]
        if self.item["type"] == "element":
            if self.answer["appearance"] == "name":
                label_input = "name_of_element"
            else: # self.answer["appearance"] == "symbol":
                label_input = "symbol_of_element"
        else: # self.item["type"] == "compound":
            if self.answer["appearance"] == "name":
                label_input = "name_of_compound"
            else: # self.answer["appearance"] == "symbol":
                label_input = "formula_of_compound"
            

        with Container(id="label-container"):
            yield TransLabel(label_input, *st, {"1": self.item})
        with HorizontalGroup(id="input-container"):
            yield TransInput("answer", *st, id="answer-input")
            yield Button("✓", variant="success", id="check-mark-button")

    class UserAnswered(Message):
        def __init__(self, value: Literal["correct", "wrong"]) -> None:
            self.value = value
            super().__init__()

    @on(TransInput.Submitted, "#answer-input")
    @on(Button.Pressed, "#check-mark-button")
    def answer_check(self):
        st = "quiz", self.app.translate # type: ignore[attr-defined]
        self.users_answer = self.query_one("#answer-input",TransInput).value.strip()
        self.percent = SequenceMatcher(
            a=st[1].t((("n", "<1>"),), "", {"1": self.answer}), # type: ignore[attr-defined]
            b=self.users_answer, 
            autojunk=False
            ).ratio()
        input_container = self.query_one("#input-container", HorizontalGroup)
        input_container.remove_children()
        if self.percent == 1:
            self.app.state.statistics["typing"]["absolutely_correct"] += 1 # type: ignore[attr-defined]
            self.app.state.statistics["correct"] += 1 # type: ignore[attr-defined]
            input_container.mount(
                TransButton((
                    ("w", "absolutely_correct"),
                    ("n", "\n"),
                    ("w", "your_answer"),
                    ("n", f": {self.users_answer}")
                    ),
                *st,
                variant="success",
                id="answer-button")
            )
        elif self.percent >= 0.85:
            input_container.mount(
                self.get_answer_button("correct", "success")
            )
        elif self.percent >= 0.7:
            input_container.mount(
                self.get_answer_button("rather_correct", "success")
            )
        elif self.percent >= 0.5:
            input_container.mount(
                self.get_answer_button("rather_wrong", "error")
            )
        elif self.percent >= 0.25:
            input_container.mount(
                self.get_answer_button("wrong", "error")
            )
        else: # self.percent < 0.25
            input_container.mount(
                self.get_answer_button("completely_wrong", "error")
            )

    def get_answer_button(self,
                          status: Literal["absolutely_correct", "correct", "rather_correct", "rather_wrong", "wrong", "completely_wrong"],
                          variant: Literal["success", "error"]
                          ) -> TransButton:
        st = "quiz", self.app.translate # type: ignore[attr-defined]
        self.app.state.statistics["typing"][status] += 1 # type: ignore[attr-defined]
        if variant == "success":
            self.app.state.statistics["correct"] += 1 # type: ignore[attr-defined]
        if variant == "error":
            self.app.state.statistics["wrong"] += 1 # type: ignore[attr-defined]
        return TransButton((
                        ("w", status),
                        ("n", "\n") if status == "completely_wrong" else ("n", f"\n{round(self.percent*100, 1)}%\n"),
                        ("w", "your_answer") if self.users_answer else ("n", ""),
                        ("n", f": {self.users_answer}") if self.users_answer else ("w", "answer_nothing"),
                        ("n", "\n"),
                        ("w", "correct_answer"),
                        ("n", f": <1>")
                    ),
                    *st,
                    {"1": self.answer},
                    variant=variant,
                    id="answer-button")

    def on_button_pressed(self, event: TransButton.Pressed):
        if event.button.id == "answer-button":
            if self.percent >= 0.7:
                self.post_message(self.UserAnswered("correct"))
            else: # self.percent < 0.7
                self.post_message(self.UserAnswered("wrong"))