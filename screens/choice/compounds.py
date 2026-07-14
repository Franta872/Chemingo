# TEXTUAL imports
from textual.containers import Container
from textual.app import ComposeResult
from textual.widgets import SelectionList, Button
from textual import events, on

from textual.widgets._toggle_button import ToggleButton
ToggleButton.BUTTON_INNER = "●" # changing "X" in SelectionList to "●".
# This is is not intended function of textual, so it's small hack.

# APP imports
from data.database import compounds_by_formula, compounds_categories
from utils.translatable_widgets import TransCompoundLabel, TransButton

class CompoundsTab(Container):
    def compose(self) -> ComposeResult:
        yield Container(
            Container(id="compounds-container-left"),
            Container(id="compounds-container-right"),
            id="main-compounds-container"
            )
    
    def on_button_pressed(self, event: Button.Pressed): # edit this button hint pls
        if event.button.has_class("compounds-selection-button"):
            selection_list = event.button.parent.parent.query_one(".compounds-selection-list", SelectionList)
            if event.button.id == "compounds-selection-select":
                selection_list.select_all()
            elif event.button.id == "compounds-selection-deselect":
                selection_list.deselect_all()
            else: # event.button.id == "compounds-selection-invert"
                selection_list.toggle_all()
    # handling select, deselect and invert buttons for compound categories

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
    
            await self.query_one(f"#compounds-container-{category_container_site}", Container).mount(
                Container(
                    TransCompoundLabel(compounds_categories[category_id]["names"][self.app.translate.language],
                        self.app.translate, classes="compounds-category-label", id=f"{category_id}-label"),
                        compound_selection_list,
                    id=f"{category_id}-container", classes="compound-category-container"
                )
            )
            # adding Container, Label and SelectionList to left or right container