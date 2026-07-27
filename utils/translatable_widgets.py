# TEXTUAL imports
from textual.widgets import Label, Button, TabPane, TabbedContent, RadioButton, Input
from textual_pyfiglet import FigletWidget
from textual.containers import Container
# APP DATABASE imports
from data.database import elements_by_symbol
from data.database import compound_categories

class TransMixin:
    """Adds runtime translation support to Textual widgets."""
    def __init__(self, word: str | tuple, description: dict | None = None, *args, **kwargs) -> None:
        self._word = word
        self.description = description or {}

        if isinstance(self, TransTabPane):
            super().__init__("", *args, **kwargs)
            # TabPane requires an initial title; it is translated after mounting.
        else: 
            super().__init__(*args, **kwargs)

    def on_mount(self) -> None:
        if isinstance(self, (TransElementButton, TransCompoundLabel)):
            self.label = self._word
        self.update_language()

    def update_language(self) -> None:
        raise NotImplementedError


class TransLabel(TransMixin, Label):
    """A Textual Label that can update its translated text."""
    def update_language(self) -> None:
        self.update(self.app.translate.t(self._word, self.screen.NAME, self.description))

class TransButton(TransMixin, Button):
    """A Textual Button that can update its translated label."""
    def update_language(self) -> None:
        self.label: str = self.app.translate.t(self._word, self.screen.NAME, self.description)

class TransFigletWidget(TransMixin, FigletWidget):
    """A Textual Figlet Widget that can update its translatable text"""
    def update_language(self) -> None:
        self.update(self.app.translate.t(self._word, self.screen.NAME, self.description))

class TransElementButton(TransMixin, Button):
    """A button whose tooltip contains the translated element name."""
    def update_language(self) -> None:
        self.tooltip = elements_by_symbol[self.id]["names"][self.app.translate.language] # type: ignore[attr-defined]

class TransCompoundLabel(TransMixin, Label):
    """A label that displays a translated compound category name."""
    def update_language(self) -> None:
        self.update(compound_categories[self.id.split("-")[0]]["names"][self.app.translate.language]) # type: ignore[attr-defined]

class TransTabPane(TransMixin, TabPane):
    """A TabPane whose title can be translated at runtime."""
    def update_language(self) -> None:
        self.screen.query_one(TabbedContent).get_tab(self.id).label = self.app.translate.t(self._word, self.screen.NAME)

class TransRadioButton(TransMixin, RadioButton):
    """A RadioButton that can update its translatable text and tooltip"""
    def __init__(self, *args, trans_tooltip: str = "", **kwargs):
        self._trans_tooltip = trans_tooltip
        super().__init__(*args, **kwargs)

    def update_language(self) -> None:
        self.label = self.app.translate.t(self._word, self.screen.NAME)
        self.tooltip = self.app.translate.t(self._trans_tooltip, self.screen.NAME)

class TransBorderContainer(TransMixin, Container):
    """A container with a translatable border title."""
    def update_language(self) -> None:
        self.border_title = self.app.translate.t(self._word, self.screen.NAME)

class TransInput(TransMixin, Input):
    """An Input with a translatable placeholder."""
    def update_language(self) -> None:
        self.placeholder = self.app.translate.t(self._word, self.screen.NAME)