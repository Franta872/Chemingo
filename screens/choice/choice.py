# TEXTUAL imports
from textual.screen import Screen
from textual.widgets import Static, TabbedContent, SelectionList, \
                            Select, Label, RadioSet, RadioButton
from textual.containers import Container, HorizontalGroup, Center
from textual import events, on
from textual.validation import Number
# APP imports
from data.database import periodic_table, compounds_categories, compounds_by_formula, \
                          all_languages_select, elements_by_symbol
from utils.translatable_widgets import TransLabel, TransElementButton, TransTabPane, \
                                       TransCompoundLabel, TransButton, TransRadioButton, \
                                       TransBorderContainer, TransInput
# PYTHON import
from typing import Literal

from textual.widgets._toggle_button import ToggleButton
ToggleButton.BUTTON_INNER = "●" # changing "X" in SelectionList to "●".
# This is is not intended function of textual, so it's small hack.

class ChoiceScreen(Screen):
    CSS_PATH = [
        "choice.tcss", 
        "choice_periodic_table.tcss", 
        "choice_compounds.tcss",
        "choice_testing_settings.tcss"
        ]
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
            with TransTabPane("periodic_table", *st, id="periodic-table"):
                yield Container(
                    Container(id="elements-grid"),
                    id="elements-scroll"
                )
            with TransTabPane("compounds", *st, id="compounds"):
                yield Container(
                    Container(id="compounds-container-left"),
                    Container(id="compounds-container-right"),
                    id="main-compounds-container"
                    )
            with TransTabPane("testing_settings", *st, id="testing-settings"):
                with Container(id="testing-container"):
                    yield Container(id="summary-container")
                    yield TransLabel("testing_settings", *st, id="testing-settings-label")

                    with TransBorderContainer("boolean_question", *st, classes="settings-question-container", id="settings-bool-container"):
                        yield TransLabel("boolean_description", *st, classes="settings-description-label")
                        with RadioSet(id="boolean-radioset"):
                            yield TransRadioButton("yes", *st, value=True)
                            yield TransRadioButton("no", *st)

                    with TransBorderContainer("choice_question", *st, classes="settings-question-container", id="settings-choice-container"):
                        yield TransLabel("choice_description", *st, classes="settings-description-label")
                        with RadioSet(id="choice-radioset"):
                            yield TransRadioButton("yes", *st, value=True)
                            yield TransRadioButton("no", *st)

                    with TransBorderContainer("typing_question", *st, classes="settings-question-container", id="settings-typing-container"):
                        yield TransLabel("typing_description", *st, classes="settings-description-label")
                        with RadioSet(id="typing-radioset"):
                            yield TransRadioButton("yes", *st, value=True)
                            yield TransRadioButton("no", *st)

                    with TransBorderContainer("num_of_questions", *st, classes="settings-question-container"):
                        yield TransLabel("num_of_questions_description", *st, classes="settings-description-label")
                        with Container(id="amount-question-container"):
                            #with RadioSet(id="amount-question-radioset"):
                            yield TransRadioButton("", *st, classes="amount-question-radiobutton", id="amount-question-radiobutton-1", 
                                                   value=True, trans_tooltip="number")
                            yield TransInput("number", *st, type="integer", valid_empty=False,
                                    validators=[Number(minimum=5)], id="amount-question-input")
                            yield TransRadioButton("", *st, classes="amount-question-radiobutton", id="amount-question-radiobutton-2",
                                                   trans_tooltip="infinity")
                            yield Label("♾️", id="infinity-label")
                    
                    with Center(id="error-container"):
                        yield Static("") # Textual doesn't like empty containers.
                    with Center(id="start-quiz-container"):
                        yield TransButton("start_quiz", *st, id="start-quiz-button", variant="primary")

    def count_selected(self, elements: bool = False) -> dict[str, list[str]]:
        selected: dict[str, list[str]] = dict()
        if not self.query_one("#compounds-container-left").is_empty and \
           not self.query_one("#compounds-container-right").is_empty:
            for category in compounds_categories:
                selected.update({category: self.query_one(f"#{category}", SelectionList).selected})
        if elements:
            selected.update({"elements": sorted(list(self.app.state.selected_elements))})
        return selected


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
            for widget in self.query("TransLabel, TransElementButton, TransTabPane, TransCompoundLabel, TransButton, TransRadioButton, TransBorderContainer, TransInput"):
                self.app.translate.language = event.value

                widget.update_language()
                # telling widgets they need to change their language
                
        # clearing and adding options to SelectionList, because
        # Textual doesn't have build in function for that
        selected: dict[str, list[str]] = self.count_selected()
        # saving selections of the user

        await self.query_one("#compounds-container-left").remove_children()
        await self.query_one("#compounds-container-right").remove_children()
        await self.add_compounds()

        for category in selected:
            for item in selected[category]:
                self.query_one(f"#{category}", SelectionList).select(item)
        
        self.testing_settings_tab_render()


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

        elif event.button.id == "start-quiz-button":
            from project import is_blank_dictionary
            if self.query_one("#amount-question-radiobutton-1", TransRadioButton).value:
                input_value = self.query_one("#amount-question-input", TransInput).value
                input_value = 0 if input_value == "" else int(input_value)
            elif self.query_one("#amount-question-radiobutton-2", TransRadioButton).value:
                input_value = float("inf")

            yes = self.app.translate.t("yes", "choice")
            settings_questions = {
                "boolean": self.query_one("#boolean-radioset", RadioSet).pressed_button.label == yes,
                "choice": self.query_one("#choice-radioset", RadioSet).pressed_button.label == yes,
                "typing": self.query_one("#typing-radioset", RadioSet).pressed_button.label == yes
            }
            error_container = self.query_one("#error-container", Center)
            error_container.remove_children()
            st = "choice", self.app.translate
            if is_blank_dictionary(settings_questions):
                error_container.mount(
                    TransLabel("empty_question_types_error", *st, classes="error-label")
                    )
            if input_value < 5:
                error_container.mount(
                    TransLabel("lower_than_five_questions_error", *st, classes="error-label")
                    )
            from project import count_dictionary_list_items
            if count_dictionary_list_items(self.count_selected(elements=True)) < 5:
                # counts number of all selected items
                error_container.mount(
                    TransLabel("lower_than_five_selected_error", *st, classes="error-label")
                    )
            if error_container.is_empty:
                self.query_one("#error-container", Center).remove_children()
                self.app.push_screen("quiz")
                #settings_questions.update({
                #    "num_of_questions": input_value
                #})


    def elements_action(self, action: Literal["select", "deselect", "invert"]):
        """
        handling select, deselect and invert buttons for periodic table.
        """
        selected_elements: set[str] = self.app.state.selected_elements
        if action == "select":
            for element in self.query(".element"):
                element.add_class("selected")
                selected_elements.clear()
                for element in elements_by_symbol:
                    selected_elements.add(element)
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

    @on(TabbedContent.TabActivated)
    def tab_changed(self, event: TabbedContent.TabActivated|None) -> None:
        if event.pane.id == "testing-settings":
            self.testing_settings_tab_render()
            
    def testing_settings_tab_render(self) -> None:
        selected: dict[str, list[str]] = self.count_selected(elements=True)

        self.query_one("#summary-container", Container).remove_children()
        from project import is_blank_dictionary
        if not is_blank_dictionary(selected):
            for category, value in selected.items():

                if value != []:
                    label = Label(", ".join(value), classes="summary-label")
                    self.query_one("#summary-container", Container).mount(
                        label
                    )
                    if category == "elements":
                        label.border_title = self.app.translate.t("elements", "choice")
                    else:
                        label.border_title = compounds_categories[category]["names"][self.app.translate.language]
        else:
            self.query_one("#summary-container", Container).mount(
                Label(self.app.translate.t("nothing_to_show", "choice"), classes="summary-label")
            )
        self.query_one("#summary-container", Container).border_title = self.app.translate.t("summary", "choice")
    
    def on_radio_button_changed(self, event: RadioButton.Changed):
        radio_button1 = self.query_one("#amount-question-radiobutton-1", TransRadioButton)
        radio_button2 = self.query_one("#amount-question-radiobutton-2", TransRadioButton)
        if (event.radio_button.id[-1] == "1" and event.radio_button.value) or \
            (event.radio_button.id[-1] == "2" and not event.radio_button.value):
            radio_button2.value = False
            radio_button1.value = True
            self.query_one("#amount-question-input").disabled = False
        elif (event.radio_button.id[-1] == "2" and event.radio_button.value) or \
            (event.radio_button.id[-1] == "1" and not event.radio_button.value):
            radio_button1.value = False
            radio_button2.value = True
            self.query_one("#amount-question-input").disabled = True
