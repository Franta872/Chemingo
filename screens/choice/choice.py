from textual.screen import Screen
from textual.widgets import Static, TabbedContent, SelectionList, \
                            Select
from textual.containers import Container, HorizontalGroup

from data.database import periodic_table, compounds_categories, compounds_by_formula, \
                          all_languages_select, elements_by_symbol
from utils.translatable_widgets import TransLabel, TransElementButton, TransTabPane, \
                                       TransCompoundLabel, TransButton
from textual import events, on
from typing import Literal

from textual.widgets._toggle_button import ToggleButton
ToggleButton.BUTTON_INNER = "●"

class ChoiceScreen(Screen):
    CSS_PATH = ["choice.tcss", "choice_periodic_table.tcss", "choice_compounds.tcss"]
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
                    TransButton("select_all", *st, variant="success", 
                    id="elements-select", classes="elements-selection-buttons"),
                    TransButton("deselect_all", *st, variant="error", 
                    id="elements-deselect", classes="elements-selection-buttons"),
                    TransButton("invert_all", *st, variant="primary", 
                    id="elements-invert", classes="elements-selection-buttons"),
                    id="elements-selection-container"
                )
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

    async def on_select_changed(self, event: Select.Changed):
        if event.select.id == "language-select":
            for widget in self.query("TransLabel, TransElementButton, TransTabPane, TransCompoundLabel, TransButton"):
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

            compound_selection_list = SelectionList(id=category_id, classes="compounds-selection-list")
            
            for compound in compounds_by_formula:
                if compounds_by_formula[compound]["category_id"] == category_id:
                    compound_selection_list.add_option(
                        (f"{compounds_by_formula[compound]['formula_unicode']}: {compounds_by_formula[compound]['names'][self.app.translate.language]}",
                         compound)
                    )

            self.query_one(f"#compounds-container-{category_container_num}", Container).mount(
                Container(
                    TransCompoundLabel(compounds_categories[category_id]["names"][self.app.translate.language],
                        self.app.translate, classes="compounds-category-label", id=f"{category_id}-label"),
                        compound_selection_list,
                    id=f"{category_id}-container", classes="compound-category-container"
                )
            )

    def on_button_pressed(self, event: TransElementButton.Pressed):
        if event.button.has_class("element"):
            if not event.button.has_class("selected"):
                self.query_one(f"#{event.button.id}").add_class("selected")
                self.app.state.selected_elements.add(event.button.id)
            elif event.button.has_class("selected"):
                self.query_one(f"#{event.button.id}").remove_class("selected")
                self.app.state.selected_elements.discard(event.button.id)

        elif event.button.has_class("compounds-selection-button"):
            selection_list = event.button.parent.parent.query_one(".compounds-selection-list", SelectionList)
            if event.button.id == "compounds-selection-select":
                selection_list.select_all()
            elif event.button.id == "compounds-selection-deselect":
                selection_list.deselect_all()
            elif event.button.id == "compounds-selection-invert":
                selection_list.toggle_all()

        elif event.button.has_class("elements-selection-buttons"):
            if event.button.id == "elements-select":
                self.elements_action("select")
            elif event.button.id == "elements-deselect":
                self.elements_action("deselect")
            else: # event.button.id == "elements-invert"
                self.elements_action("invert")


    def elements_action(self, action: Literal["select", "deselect", "invert"]):
        selected_elements: set[str] = self.app.state.selected_elements
        if action == "select":
            for element in self.query(".element"):
                element.add_class("selected")
                selected_elements = set(elements_by_symbol.keys())
        elif action == "deselect":
            for element in self.query(".selected"):
                element.remove_class("selected")
                selected_elements.clear()
        else: # action == invert
            for element in self.query(".element"):
                if element.has_class("selected"):
                    element.remove_class("selected")
                    selected_elements.discard(element.id)
                else: # not element.has_class("selected")
                    element.add_class("selected")
                    selected_elements.add(element.id)
            

    @on(events.Enter, ".compounds-category-label, .compounds-selection-list, .compound-category-container")
    def mouse_entered_container(self, event: events.Enter) -> None:
        if event.node.has_class("compound-category-container"):
            container = event.node
        else:
            container = event.node.parent

        st = "choice", self.app.translate
        if not container.query(".compounds-selection-container"):
            container.mount(
                Container(
                TransButton("select_all", *st, variant="success", id="compounds-selection-select", classes="compounds-selection-button"),
                TransButton("deselect_all", *st, variant="error", id="compounds-selection-deselect", classes="compounds-selection-button"),
                TransButton("invert_all", *st, variant="primary", id="compounds-selection-invert", classes="compounds-selection-button"),
                classes="compounds-selection-container"
                ),
                after=0
            )
    @on(events.Leave, ".compounds-category-label, .compounds-selection-list, .compound-category-container, .compounds-selection-container")
    async def mouse_left_container(self, event: events.Leave) -> None:
        if event.node.has_class("compound-category-container"):
            container = event.node
        else:
            container = event.node.parent
        try:
            if container.query(".compounds-selection-container") and \
                not container.is_mouse_over and \
                not container.query_one(".compounds-selection-container").is_mouse_over:
                container.query_one(".compounds-selection-container", Container).remove()
        except AttributeError:
            pass