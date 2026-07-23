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

            from project import count_dictionary_list_items # accessing it locally because of circular import
            t = self.app.translate.t # type: ignore[attr-defined]
            statistics: dict = self.app.state.statistics # type: ignore[attr-defined]
            tree: Tree[str] = Tree("")

            tree.root.add_leaf(t("remaining_questions", "quiz")+": "+("♾️" if isinf(self.app.state.num_of_questions) else f"[b]{self.app.state.num_of_questions}[/]"))

            chosen_items = tree.root.add_leaf(t("chosen_items", "quiz")+f": [b]{len(self.app.state.selected_elements)+count_dictionary_list_items(self.app.state.selected_compounds)}[/]")
            chosen_items.add_leaf(t("chosen_elements", "quiz")+f": [b]{len(self.app.state.selected_elements)}[/]")
            chosen_items.add_leaf(t("chosen_compounds", "quiz")+f": [b]{count_dictionary_list_items(self.app.state.selected_compounds)}[/]")

            total_answered = tree.root.add_leaf(t("total_answered_questions", "quiz")+f": [b]{statistics["correct"]+statistics["wrong"]}[/]")
            total_answered.add_leaf(t("total_correct_questions", "quiz")+f": [b]{statistics["correct"]}[/]")
            total_answered.add_leaf(t("total_wrong_questions", "quiz")+f": [b]{statistics["wrong"]}[/]")


            boolean_question = tree.root.add(t("boolean_question", "choice"))
            boolean_question_answered = boolean_question.add_leaf(f"{t("answered_questions", "quiz")}: [b]{statistics["boolean"]["correct"]+statistics["boolean"]["wrong"]}[/]")
            boolean_question_answered.add_leaf(f"{t("correct_questions", "quiz")}: [b]{statistics["boolean"]["correct"]}[/]")
            boolean_question_answered.add_leaf(f"{t("wrong_questions", "quiz")}: [b]{statistics["boolean"]["wrong"]}[/]")

            choice_question = tree.root.add(t("choice_question", "choice"))
            choice_question_answered = choice_question.add_leaf(f"{t("answered_questions", "quiz")}: [b]{statistics["choice"]["correct"]+statistics["choice"]["wrong"]}[/]")
            choice_question_answered.add_leaf(f"{t("correct_questions", "quiz")}: [b]{statistics["choice"]["correct"]}[/]")
            choice_question_answered.add_leaf(f"{t("wrong_questions", "quiz")}: [b]{statistics["choice"]["wrong"]}[/]")

            typing_question = tree.root.add(t("typing_question", "choice"))
            typing_question_answered = typing_question.add_leaf(f"{t("answered_questions", "quiz")}: [b]{sum(statistics["typing"].values())}[/]")
            typing_question_answered.add_leaf(f"{t("absolutely_correct", "quiz")[:-1]}: [b]{statistics["typing"]["absolutely_correct"]}[/]")
            typing_question_answered.add_leaf(f"{t("correct", "quiz")[:-1]}: [b]{statistics["typing"]["correct"]}[/]")
            typing_question_answered.add_leaf(f"{t("rather_correct", "quiz")}: [b]{statistics["typing"]["rather_correct"]}[/]")
            typing_question_answered.add_leaf(f"{t("rather_wrong", "quiz")}: [b]{statistics["typing"]["rather_wrong"]}[/]")
            typing_question_answered.add_leaf(f"{t("wrong", "quiz")[:-1]}: [b]{statistics["typing"]["wrong"]}[/]")
            typing_question_answered.add_leaf(f"{t("completely_wrong", "quiz")[:-1]}: [b]{statistics["typing"]["completely_wrong"]}[/]")

            tree.root.expand_all()
            yield tree

            with Container(classes="statistics-center-container"):
                yield TransButton("close", *st, id="close-button", variant="error")
    
    def on_button_pressed(self, event: TransButton.Pressed) -> None:
        if event.button.id == "close-button":
            self.app.pop_screen()