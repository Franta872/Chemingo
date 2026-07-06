from textual.screen import Screen
from textual.widgets import Static, TabbedContent, SelectionList, \
                            Select
from textual.containers import Container, HorizontalGroup

from data.database import periodic_table, compounds_categories, compounds_by_formula, \
                          all_languages_select
from utils.translatable_widgets import TransLabel, TransElementButton, TransTabPane, \
                                       TransCompoundLabel

from textual.widgets._toggle_button import ToggleButton
ToggleButton.BUTTON_INNER = "●"

class ChoiceScreen(Screen):
    CSS_PATH = "choice.tcss"
    HORIZONTAL_BREAKPOINTS = [
        (0, "small"),
        (70, "wide")
    ]

    def compose(self):
        st = "choice", self.app.translate

        yield HorizontalGroup(
            TransLabel("language", *st, id="language-label"),
            Select(all_languages_select, allow_blank=False, compact=True, id="language-select",
                   value=self.app.translate.language),
            id="language-horizontal"
            )

        with TabbedContent():
            with TransTabPane("periodic_table", *st):
                yield Container(
                Container(id="elements-grid"),
                id="elements-scroll"
                )
            with TransTabPane("compounds", *st):
                yield Container(
                    Container(id="compounds-container-1"),
                    Container(id="compounds-container-2"),
                    id="main-compounds-container"
                    )
            with TransTabPane("testing", *st):
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
                        TransElementButton(element[0], self.app.translate, id=element[0],
                                           classes=f"element {element[1]}")
                        # button with the element symbol
                        )
        # compounds
        # self.add_compounds()


    async def on_select_changed(self, event: Select.Changed):
        if event.select.id == "language-select":
            for widget in self.query("TransLabel, TransElementButton, TransTabPane, TransCompoundLabel"):
                self.app.translate.language = event.value
                
                widget.update_language()
        
        selected: dict[str, list[str]] = dict()
        if not self.query_one("#compounds-container-1").is_empty and \
           not self.query_one("#compounds-container-2").is_empty:
            for category in compounds_categories:
                selected.update({category: self.query_one(f"#{category}", SelectionList).selected})

        await self.query_one("#compounds-container-1").remove_children()
        await self.query_one("#compounds-container-2").remove_children()
        self.add_compounds()
        
        for category in selected:
            for item in selected[category]:
                self.query_one(f"#{category}", SelectionList).select(item)

        
    def add_compounds(self):
        num_of_categories = [0, len(compounds_categories)]
        for category_id in compounds_categories:
            category_container_num = "1" if num_of_categories[0] < num_of_categories[1] // 2.5 else "2"
            num_of_categories[0] += 1
            self.query_one(f"#compounds-container-{category_container_num}", Container).mount(
                TransCompoundLabel(compounds_categories[category_id]["names"][self.app.translate.language],
                    self.app.translate, classes="compounds-category-label", id=f"{category_id}-label"),
                SelectionList(id=category_id, classes="compounds-selection-list")
            )
            for compound in compounds_by_formula:
                if compounds_by_formula[compound]["category_id"] == category_id:
                    self.query_one(f"#{category_id}", SelectionList).add_option(
                        (f"{compounds_by_formula[compound]["formula_unicode"]}: {compounds_by_formula[compound]["names"][self.app.translate.language]}",
                         compound)
                    )