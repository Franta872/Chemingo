# TEXTUAL imports
from textual.screen import Screen
from textual.widgets import TabbedContent, SelectionList, Select
from textual.containers import HorizontalGroup
from textual import on
# APP imports
from data.database import compounds_categories, all_languages_select
from utils.translatable_widgets import TransLabel, TransTabPane
from screens.choice.periodic_table import PeriodicTableTab
from screens.choice.compounds import CompoundsTab
from screens.choice.quiz_settings import QuizSettingsTab

class ChoiceScreen(Screen):
    CSS_PATH = [
        "tcss/choice.tcss",
        "tcss/choice_periodic_table.tcss",
        "tcss/choice_compounds.tcss",
        "tcss/choice_quiz_settings.tcss"
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
                yield PeriodicTableTab()
            with TransTabPane("compounds", *st, id="compounds"):
                yield CompoundsTab()
            with TransTabPane("quiz_settings", *st, id="quiz-settings"):
                yield QuizSettingsTab()

    def return_selected(self, elements: bool = False) -> dict[str, list[str]]:
        """
        Return a dictionary of selected elements and compounds.
        """
        selected: dict[str, list[str]] = dict()
        if not self.query_one("#compounds-container-left").is_empty and \
           not self.query_one("#compounds-container-right").is_empty:
            for category in compounds_categories:
                selected.update({category: self.query_one(f"#{category}", SelectionList).selected})
        if elements:
            selected.update({"elements": sorted(list(self.app.state.selected_elements))})
        return selected

    async def on_select_changed(self, event: Select.Changed):
        # changing language in whole screen
        if event.select.id == "language-select":
            self.app.translate.language = event.value
            # sets the language in the whole app
            for widget in self.query("TransLabel, TransElementButton, TransTabPane, TransCompoundLabel, TransButton, TransRadioButton, TransBorderContainer, TransInput"):
                widget.update_language()
                # telling widgets they need to change their language

        # clearing and adding options to SelectionList, because
        # Textual doesn't have build in function for that
        selected: dict[str, list[str]] = self.return_selected()
        # saving selections of the user

        await self.query_one("#compounds-container-left").remove_children()
        await self.query_one("#compounds-container-right").remove_children()
        await self.query_one("CompoundsTab", CompoundsTab).add_compounds()

        for category in selected:
            for item in selected[category]:
                self.query_one(f"#{category}", SelectionList).select(item)
        
        self.query_one("QuizSettingsTab", QuizSettingsTab).quiz_settings_tab_render()

    @on(TabbedContent.TabActivated)
    def tab_changed(self, event: TabbedContent.TabActivated) -> None:
        if event.pane.id == "quiz-settings":
            self.query_one("QuizSettingsTab", QuizSettingsTab).quiz_settings_tab_render()
            # recreating settings tab because of possible changes.