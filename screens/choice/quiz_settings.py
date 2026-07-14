# TEXTUAL imports
from textual.containers import Container, Center
from textual.app import ComposeResult
from textual.widgets import RadioSet, Label, Static, RadioButton
from textual.validation import Number
# APP import
from utils.translatable_widgets import TransLabel, TransBorderContainer, TransRadioButton, \
                                       TransInput, TransButton
from data.database import compounds_categories

class QuizSettingsTab(Container):
    def compose(self) -> ComposeResult:
        st = "choice", self.app.translate

        with Container(id="testing-container"):
            yield Container(id="summary-container")
            yield TransLabel("quiz_settings", *st, id="quiz-settings-label")

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
    

    def on_button_pressed(self, event: TransButton.Pressed):
        if event.button.id == "start-quiz-button":
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
            from project import is_blank_dictionary # accessing it locally because of circular import
            if is_blank_dictionary(settings_questions):
                error_container.mount(
                    TransLabel("empty_question_types_error", *st, classes="error-label")
                    )
            if input_value < 5:
                error_container.mount(
                    TransLabel("lower_than_five_questions_error", *st, classes="error-label")
                    )
            from project import count_dictionary_list_items # accessing it locally because of circular import
            if count_dictionary_list_items(self.screen.return_selected(elements=True)) < 5:
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

    def quiz_settings_tab_render(self) -> None:
        selected: dict[str, list[str]] = self.screen.return_selected(elements=True)
        self.query_one("#summary-container", Container).remove_children()
        from project import is_blank_dictionary # accessing it locally because of circular import
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
