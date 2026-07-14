# TEXTUAL imports
from textual.containers import Container
from textual.app import ComposeResult
from textual.widgets import Static
from textual import events, on
# APP imports
from utils.translatable_widgets import TransButton, TransElementButton
from data.database import periodic_table, elements_by_symbol
# PYTHON import
from typing import Literal

class PeriodicTableTab(Container):
    def compose(self) -> ComposeResult:
        yield Container(
            Container(id="elements-grid"),
            id="elements-scroll"
        )
    
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

    def on_button_pressed(self, event: TransElementButton.Pressed):
        if event.button.has_class("element"):
            if event.button.has_class("selected"):
                self.query_one(f"#{event.button.id}").remove_class("selected")
                self.app.state.selected_elements.discard(event.button.id)
            else: # not event.button.has_class("selected")
                self.query_one(f"#{event.button.id}").add_class("selected")
                self.app.state.selected_elements.add(event.button.id)
        # adding and removing selected class from clicked elements in periodic table

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
            selected_elements.clear()
            for element_widget in self.query(".element"):
                element_widget.add_class("selected")
                for element in elements_by_symbol:
                    selected_elements.add(element)
        elif action == "deselect":
            selected_elements.clear()
            for element in self.query(".selected"):
                element.remove_class("selected")
        else: # action == invert
            for element in self.query(".element"):
                if element.has_class("selected"):
                    element.remove_class("selected")
                    selected_elements.discard(element.id)
                else: # not element.has_class("selected")
                    element.add_class("selected")
                    selected_elements.add(element.id)