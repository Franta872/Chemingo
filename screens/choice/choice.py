from textual.screen import Screen
from textual.widgets import Button, Static, TabbedContent, SelectionList
from textual.containers import Container

from data.database import periodic_table, compounds_categories, compounds_by_formula

class ChoiceScreen(Screen):
    CSS_PATH = "choice.tcss"

    def compose(self):
        with TabbedContent("periodic table", "compounds", "testing"):
            yield Container(
                Container(id="elements-grid"),
                id="elements-scroll"
                )
            yield Container(id="compounds-container")
            yield Container(id="testing-container")

    def on_mount(self) -> None:
        # periodic table
        for row in periodic_table:
            for element in row:
                if element is None:
                    self.query_one("#elements-grid", Container).mount(
                        Static() # blank square
                        )
                else: # type(element) is str
                    self.query_one("#elements-grid", Container).mount(
                        Button(element, id=element.lower(), classes="element")
                        # button with the element symbol
                        )
        # compounds
        for category_id in compounds_categories:
            self.query_one("#compounds-container", Container).mount(
                SelectionList(id=category_id, classes="compounds-selection-list")
            )
            self.query_one(f"#{category_id}", SelectionList).border_title = compounds_categories[category_id]["names"][self.app.translate.language]
            for compound in compounds_by_formula:
                if compounds_by_formula[compound]["category_id"] == category_id:
                    self.query_one(f"#{category_id}", SelectionList).add_option(
                        (f"{compounds_by_formula[compound]["formula_unicode"]}: {compounds_by_formula[compound]["names"][self.app.translate.language]}",)*2
                    )