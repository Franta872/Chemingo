# PYTHON imports
from typing import TYPE_CHECKING
from math import isinf
# TEXTUAL imports
from textual.screen import Screen
from textual.containers import VerticalScroll, HorizontalScroll
from textual.widgets import Static, Select
from textual import on
from textual.reactive import reactive
if TYPE_CHECKING:
    from textual.app import ComposeResult
# APP import
from screens.quiz.question_types.boolean import BooleanQuestion
from screens.quiz.question_types.choice import ChoiceQuestion
from screens.quiz.random_question import random_question
from utils.translatable_widgets import TransLabel
from data.database import all_languages_select

class QuizScreen(Screen):
    CSS_PATH = "quiz.tcss"
    num_of_questions: reactive[int|float] = reactive(0)

    def compose(self) -> ComposeResult:
        st = "quiz", self.app.translate # type: ignore[attr-defined]
        with HorizontalScroll(id="top-container"):
            yield TransLabel("remaining_questions", *st, id="remaining-questions-label")
            yield TransLabel((("w", "language"), ( "n", ":")), *st, id="language-label")
            yield Select(all_languages_select, allow_blank=False, id="language-select",
                   value=self.app.translate.language) # type: ignore[attr-defined]
        with VerticalScroll(id="main-container"):
            yield Static()
    
    def on_mount(self) -> None:
        self.query_one("#main-container", VerticalScroll).remove_children(selector=Static)
        self.num_of_questions = self.app.state.num_of_questions # type: ignore[attr-defined]
        self.next_question()

    def watch_num_of_questions(self, old_value: reactive[int], new_value: reactive[int]):
        self.app.state.num_of_questions = new_value # type: ignore[attr-defined]
        self.query_one("#remaining-questions-label", TransLabel).update(
            self.app.translate.t(
                (
                ("w", "remaining_questions"),   
                ("n", f": {"♾️" if isinf(float(new_value)) else int(new_value)}")
                ), 
                "quiz")
            )

    def next_question(self) -> None:
        self.app.state.num_of_questions -= 1 # type: ignore[attr-defined]
        self.num_of_questions -= 1
        if self.app.state.num_of_questions <= 0:
            self.app.pop_screen()
        random = random_question(
            self.app.state.selected_elements, # type: ignore[attr-defined]
            self.app.state.selected_compounds, # type: ignore[attr-defined]
            self.app.state.question_answers # type: ignore[attr-defined]
            )
        if random["random_question"] == "boolean":
            self.query_one("#main-container", VerticalScroll).mount(
                BooleanQuestion(
                    quiz_screen=self,
                    dict_1=random["1"],
                    dict_2=random["2"],
                    answer=random["answer"]
                )
            )
        elif random["random_question"] == "choice":
            self.query_one("#main-container", VerticalScroll).mount(
                ChoiceQuestion(
                    quiz_screen=self,
                    asked=random["asked"],
                    item_1=random["1"],
                    item_2=random["2"],
                    item_3=random["3"],
                    item_4=random["4"]
                )
            )

    @on(BooleanQuestion.UserAnswered)
    def user_answered_boolean(self, message: BooleanQuestion.UserAnswered):
        self.query_one(BooleanQuestion).remove()
        self.next_question()
    @on(ChoiceQuestion.UserAnswered)
    def user_answered_choice(self, message: ChoiceQuestion.UserAnswered):
        self.query_one(ChoiceQuestion).remove()
        self.next_question()
    
    def on_select_changed(self, event: Select.Changed):
        # changing language in whole screen
        if event.select.id == "language-select":
            self.app.translate.language = event.value # type: ignore[attr-defined]
            for widget in self.query("TransLabel, TransButton"):
                widget.update_language() # type: ignore[attr-defined]
            self.watch_num_of_questions(*(self.num_of_questions,)*2)