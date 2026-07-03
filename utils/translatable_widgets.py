from textual.widgets import Label, Button, Input
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