from textual.widgets import Label, Button
from textual_pyfiglet import FigletWidget


class TransLabel(Label):
    """
    Ordinary Textual Label, but it can translate itself 
    with ```update_language()``` function.
    """
    def __init__(self, word: str, screen: str, trans, *args, **kwargs):
        self._word = word
        self._screen = screen
        self.translate = trans

        super().__init__(*args, **kwargs)

    def on_mount(self) -> None:
        self.update_language()
    
    def update_language(self) -> None:
        """
        This function will send order to translate itself to currently set language.
        """
        self.update(self.translate.t(self._word, self._screen))


class TransButton(Button):
    """
    Ordinary Textual Button, but it can translate itself 
    with ```update_language()``` function.
    """
    def __init__(self, word: str, screen: str, trans, *args, **kwargs):
        self._word = word
        self._screen = screen
        self.translate = trans

        super().__init__(*args, **kwargs)

    def on_mount(self) -> None:
        self.update_language()
    
    def update_language(self) -> None:
        """
        This function will send order to translate itself to currently set language.
        """
        self.label = self.translate.t(self._word, self._screen)


class TransFigletWidget(FigletWidget):
    """
    Ordinary Textual Figlet Widget, but it can translate itself 
    with ```update_language()``` function.
    """
    def __init__(self, word: str, screen: str, trans, *args, **kwargs):
        self._word = word
        self._screen = screen
        self.translate = trans

        super().__init__(*args, **kwargs)

    def on_mount(self) -> None:
        self.update_language()
    
    def update_language(self) -> None:
        """
        This function will send order to translate itself to currently set language.
        """
        self.update(self.translate.t(self._word, self._screen))

from data.database import elements_by_symbol
class TransElementButton(Button):
    """
    This is is Textual Button, but it can translate it's toolbox 
    to currently set language.
    """
    def __init__(self, label, trans, *args, **kwargs):
        self._label = label
        self.translate = trans

        super().__init__(*args, **kwargs)

    def on_mount(self) -> None:
        self.label = self._label
        self.update_language()
    
    def update_language(self) -> None:
        """
        This function will send order to translate itself's 
        toolbox to currently set language.
        """
        self.tooltip = elements_by_symbol[self.id]["names"][self.translate.language]

from data.database import compounds_categories
class TransCompoundLabel(Label):
    """
    This is is Textual Label, but it can translate it's compound category value
    to currently set language.
    """
    def __init__(self, label, trans, *args, **kwargs):
        self._label = label
        self.translate = trans

        super().__init__(*args, **kwargs)

    def on_mount(self) -> None:
        self.label = self._label
        self.update_language()
    
    def update_language(self) -> None:
        """
        This function will send order to translate itself's 
        toolbox to currently set language.
        """
        self.update(compounds_categories[self.id.split("-")[0]]["names"][self.translate.language])

from textual.widgets import TabPane, TabbedContent
class TransTabPane(TabPane):
    """
    Ordinary Textual Tab Pane, but it can translate itself 
    with ```update_language()``` function.
    """
    def __init__(self, word: str, screen: str, trans, *args, **kwargs):
        self._word = word
        self._screen = screen
        self.translate = trans

        super().__init__("", *args, **kwargs)
        """empty string: it wants some value, so I'am giving it empty string and it will change later."""

    def on_mount(self) -> None:
        self.update_language()
    
    def update_language(self) -> None:
        """
        This function will send order to translate itself to currently set language.
        """
        self.screen.query_one(TabbedContent).get_tab(self.id).label = self.translate.t(self._word, self._screen)
