# TEXTUAL imports
from textual.screen import Screen
from textual.widgets import TabbedContent, SelectionList, Select
from textual.containers import HorizontalGroup
from textual import on
# APP imports
from data.database import all_languages_select
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
    NAME = "choice"
    HORIZONTAL_BREAKPOINTS = [
        (0, "small"),
        (70, "wide")
    ]

    def compose(self):
        yield HorizontalGroup(
            TransLabel("language", id="language-label"),
            Select(all_languages_select, allow_blank=False, compact=True, id="language-select",
                   value=self.app.translate.language),
            id="language-horizontal"
            )

        with TabbedContent():
            with TransTabPane("periodic_table", id="periodic-table"):
                yield PeriodicTableTab()
            with TransTabPane("compounds", id="compounds"):
                yield CompoundsTab()
            with TransTabPane("quiz_settings", id="quiz-settings"):
                yield QuizSettingsTab()

    def return_selected(self, elements: bool = False) -> dict[str, set|list]:
        """Return selected compounds and optionally selected elements."""
        selected: dict[str, set|list] = self.app.state.selected_compounds.copy()
        if elements:
            selected.update({"elements": sorted(list(self.app.state.selected_elements))})
        return selected

    async def on_select_changed(self, event: Select.Changed):
        # changing language in whole screen
        if event.select.id == "language-select":
            await self.change_language()
    async def change_language(self):
        self.app.translate.language = self.query_one("#language-select").value
        # sets the language in the whole app
        for widget in self.query("TransLabel, TransElementButton, TransTabPane, TransCompoundLabel, TransButton, TransRadioButton, TransBorderContainer, TransInput"):
            widget.update_language()
            # telling widgets they need to change their language

        # clearing and adding options to SelectionList, because
        # Textual doesn't have built-in function for that

        await self.query_one("#compounds-container-left").remove_children()
        await self.query_one("#compounds-container-right").remove_children()
        await self.query_one("CompoundsTab", CompoundsTab).add_compounds()

        for category in self.return_selected():
            for item in self.return_selected()[category]:
                self.query_one(f"#{category}", SelectionList).select(item)

        self.query_one("QuizSettingsTab", QuizSettingsTab).quiz_settings_summary_render()

    @on(TabbedContent.TabActivated)
    def tab_changed(self, event: TabbedContent.TabActivated) -> None:
        if event.pane.id == "quiz-settings":
            self.query_one("QuizSettingsTab", QuizSettingsTab).quiz_settings_summary_render()
            # Refresh the summary because the selection may have changed.
    
    async def on_screen_resume(self) -> None:
        self.query_one("#language-select").value = self.app.translate.language
        await self.change_language()