# TEXTUAL imports
from textual.widgets import Label, Button, TabPane, TabbedContent, RadioButton, Input
from textual_pyfiglet import FigletWidget
from textual.containers import Container
# APP DATABASE imports
from data.database import elements_by_symbol
from data.database import compounds_categories

class TransMixin:
    def __init__(self, word: str | tuple, description: dict | None = None, *args, **kwargs) -> None:
        self._word = word
        self.description = description or {}

        if isinstance(self, TransTabPane):
            super().__init__("", *args, **kwargs)
            # empty string: it wants some value, so I give it an empty string and that will change later.
        else: 
            super().__init__(*args, **kwargs)

    def on_mount(self) -> None:
        if isinstance(self, (TransElementButton, TransCompoundLabel)):
            self.label = self._word
        self.update_language()

    def update_language(self) -> None:
        raise NotImplementedError


class TransLabel(TransMixin, Label):
    """
    Ordinary Textual Label, but it can translate itself 
    with ```update_language()``` function.
    """
    def update_language(self) -> None:
        self.update(self.app.translate.t(self._word, self.screen.NAME, self.description))

class TransButton(TransMixin, Button):
    """
    Ordinary Textual Button, but it can translate itself 
    with ```update_language()``` function.
    """
    def update_language(self) -> None:
        self.label: str = self.app.translate.t(self._word, self.screen.NAME, self.description)

class TransFigletWidget(TransMixin, FigletWidget):
    """
    Ordinary Textual Figlet Widget, but it can translate itself 
    with ```update_language()``` function.
    """
    def update_language(self) -> None:
        self.update(self.app.translate.t(self._word, self.screen.NAME, self.description))

class TransElementButton(TransMixin, Button):
    """
    This is is Textual Button, but it can translate it's toolbox 
    to currently set language.
    """
    def update_language(self) -> None:
        self.tooltip = elements_by_symbol[self.id]["names"][self.app.translate.language] # type: ignore[attr-defined]

class TransCompoundLabel(TransMixin, Label):
    """
    This is is Textual Label, but it can translate it's compound category value
    to currently set language.
    """
    def update_language(self) -> None:
        self.update(compounds_categories[self.id.split("-")[0]]["names"][self.app.translate.language]) # type: ignore[attr-defined]

class TransTabPane(TransMixin, TabPane):
    """
    Ordinary Textual Tab Pane, but it can translate itself 
    with ```update_language()``` function.
    """
    def update_language(self) -> None:
        self.screen.query_one(TabbedContent).get_tab(self.id).label = self.app.translate.t(self._word, self.screen.NAME)

class TransRadioButton(TransMixin, RadioButton):
    """
    Ordinary Textual RadioButton, but it can translate itself 
    with ```update_language()``` function.
    """
    def __init__(self, *args, trans_tooltip: str = "", **kwargs):
        self._trans_tooltip = trans_tooltip
        super().__init__(*args, **kwargs)

    def update_language(self) -> None:
        self.label = self.app.translate.t(self._word, self.screen.NAME)
        self.tooltip = self.app.translate.t(self._trans_tooltip, self.screen.NAME)

class TransBorderContainer(TransMixin, Container):
    """
    Ordinary Textual Container, but it can translate it's border title
    with ```update_language()``` function.
    """
    def update_language(self) -> None:
        self.border_title = self.app.translate.t(self._word, self.screen.NAME)

class TransInput(TransMixin, Input):
    """
    Ordinary Textual Input, but it can translate it's placeholder.
    with ```update_language()``` function.
    """
    def update_language(self) -> None:
        self.placeholder = self.app.translate.t(self._word, self.screen.NAME)