# PYTHON import
from typing import TYPE_CHECKING
# TEXTUAL imports
from textual.screen import Screen
from textual.containers import VerticalScroll
from textual.widgets import Static
from textual import on
if TYPE_CHECKING:
    from textual.app import ComposeResult
# APP import
from screens.quiz.question_types.boolean import BooleanQuestion
from screens.quiz.random_question import random_question

class QuizScreen(Screen):
    CSS_PATH = "quiz.tcss"

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="main-container"):
            yield Static()
    
    def on_mount(self) -> None:
        self.query_one("#main-container", VerticalScroll).remove_children()
        self.next_question()

    def next_question(self) -> None:
        random = random_question(
            self.app.state.selected_elements, # type: ignore[attr-defined]
            self.app.state.selected_compounds, # type: ignore[attr-defined]
            self.app.state.question_answers # type: ignore[attr-defined]
            )
        if random[0] == "boolean":
            self.query_one("#main-container", VerticalScroll).mount(
                BooleanQuestion(
                    quiz_screen=self,
                    **random[1]
                )
            )


    @on(BooleanQuestion.UserAnswered)
    def user_answered_boolean(self, message: BooleanQuestion.UserAnswered):
        self.query_one(BooleanQuestion).remove()
        self.next_question()