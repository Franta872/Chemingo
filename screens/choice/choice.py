# TEXTUAL imports
from textual.screen import Screen
from textual.widgets import Static, TabbedContent, SelectionList, \
                            Select
from textual.containers import Container, HorizontalGroup
from textual import events, on
# APP imports
from data.database import periodic_table, compounds_categories, compounds_by_formula, \
                          all_languages_select, elements_by_symbol
from utils.translatable_widgets import TransLabel, TransElementButton, TransTabPane, \
                                       TransCompoundLabel, TransButton
# PYTHON import
from typing import Literal

from textual.widgets._toggle_button import ToggleButton
ToggleButton.BUTTON_INNER = "●" # changing "X" in SelectionList to "●".
# This is is not intended function of textual, so it's small hack.

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
                    Container(id="elements-grid"),
                    id="elements-scroll"
                )
            with TransTabPane("compounds", *st):
                yield Container(
                    Container(id="compounds-container-left"),
                    Container(id="compounds-container-right"),
                    id="main-compounds-container"
                    )
            with TransTabPane("testing", *st):
                yield Container(id="testing-container")

    def on_mount(self) -> None:
        # Build periodic table
        st = "choice", self.app.translate
        buttons_were = False
        for row in periodic_table:
            for element in row:
                if element[0] is None:
                    if not element[1] == "absent":
                        self.query_one("#elements-grid", Container).mount(
                            Static(classes=element[1]) # blank square
                            )
                    elif not buttons_were: # and element[1] == "absent"
                        self.query_one("#elements-grid", Container).mount(
                            Container(
                            TransButton("select_all", *st, variant="success", 
                            id="elements-select", classes="elements-selection-buttons"),
                            TransButton("deselect_all", *st, variant="error", 
                            id="elements-deselect", classes="elements-selection-buttons"),
                            TransButton("invert_all", *st, variant="primary", 
                            id="elements-invert", classes="elements-selection-buttons"),
                            id="elements-selection-container"
                        )
                        )
                        buttons_were = True
                else: # type(element) is str
                    self.query_one("#elements-grid", Container).mount(
                        TransElementButton(element[0], self.app.translate, id=element[0],
                                           classes=f"element {element[1]}")
                        # button with the element symbol
                        )
    @on(events.Enter, ".sensitive, #elements-selection-container, .elements-selection-buttons")
    def mouse_entered_sensitive_area(self, _: events.Enter):
        for button in self.query(".elements-selection-buttons"):
            button.visible = True
    @on(events.Leave, ".sensitive, #elements-selection-container")
    def mouse_left_sensitive_area(self, _: events.Leave):
        for button in self.query(".elements-selection-buttons"):
            button.visible = False

    async def on_select_changed(self, event: Select.Changed):
        # changing language in whole screen
        if event.select.id == "language-select":
            for widget in self.query("TransLabel, TransElementButton, TransTabPane, TransCompoundLabel, TransButton"):
                self.app.translate.language = event.value
                
                widget.update_language()
                # telling widgets they need to change their language
                
        # clearing and adding options to SelectionList, because
        # Textual doesn't have build in function for that
        selected: dict[str, list[str]] = dict()
        if not self.query_one("#compounds-container-left").is_empty and \
           not self.query_one("#compounds-container-right").is_empty:
            for category in compounds_categories:
                selected.update({category: self.query_one(f"#{category}", SelectionList).selected})
        # saving selections of the user

        await self.query_one("#compounds-container-left").remove_children()
        await self.query_one("#compounds-container-right").remove_children()
        await self.add_compounds()
        
        for category in selected:
            for item in selected[category]:
                self.query_one(f"#{category}", SelectionList).select(item)

        
    async def add_compounds(self):
        """
        function for adding compounds to blank containers.
        """
        num_of_categories = [0, len(compounds_categories)]
        for category_id in compounds_categories:
            category_container_site = "left" if num_of_categories[0] < num_of_categories[1] // 2.5 else "right"
            num_of_categories[0] += 1
            # deciding to which site the container with compound category should be mounted

            compound_selection_list = SelectionList(id=category_id, classes="compounds-selection-list")
            
            for compound in compounds_by_formula:
                if compounds_by_formula[compound]["category_id"] == category_id:
                    compound_selection_list.add_option(
                        (f"{compounds_by_formula[compound]['formula_unicode']}: {compounds_by_formula[compound]['names'][self.app.translate.language]}",
                         compound)
                    )
            # adding options to SelectionList

            self.query_one(f"#compounds-container-{category_container_site}", Container).mount(
                Container(
                    TransCompoundLabel(compounds_categories[category_id]["names"][self.app.translate.language],
                        self.app.translate, classes="compounds-category-label", id=f"{category_id}-label"),
                        compound_selection_list,
                    id=f"{category_id}-container", classes="compound-category-container"
                )
            )
            # adding Container, Label and SelectionList to left or right container
    def on_button_pressed(self, event: TransElementButton.Pressed):
        if event.button.has_class("element"):
            if event.button.has_class("selected"):
                self.query_one(f"#{event.button.id}").remove_class("selected")
                self.app.state.selected_elements.discard(event.button.id)
            else: # not event.button.has_class("selected")
                self.query_one(f"#{event.button.id}").add_class("selected")
                self.app.state.selected_elements.add(event.button.id)
        # adding and removing selected class from clicked elements in periodic table

        elif event.button.has_class("compounds-selection-button"):
            selection_list = event.button.parent.parent.query_one(".compounds-selection-list", SelectionList)
            if event.button.id == "compounds-selection-select":
                selection_list.select_all()
            elif event.button.id == "compounds-selection-deselect":
                selection_list.deselect_all()
            else: # event.button.id == "compounds-selection-invert"
                selection_list.toggle_all()
        # handling select, deselect and invert buttons for compound categories

        elif event.button.has_class("elements-selection-buttons"):
            if event.button.id == "elements-select":
                self.elements_action("select")
            elif event.button.id == "elements-deselect":
                self.elements_action("deselect")
            else: # event.button.id == "elements-invert"
                self.elements_action("invert")
        # detecting select, deselect and invert buttons for periodic table


    def elements_action(self, action: Literal["select", "deselect", "invert"]):
        """
        handling select, deselect and invert buttons for periodic table.
        """
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
        """
        Adding button to edit selected compounds when mouse enters certain 
        compounds category.
        """
        if event.node.has_class("compound-category-container"):
            container = event.node
        else:
            container = event.node.parent

        st = "choice", self.app.translate
        if not container.query(".compounds-selection-container"):
            self.query(".compounds-selection-button").remove()
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
        """
        Removes buttons when mouse leaves compounds category.
        """
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