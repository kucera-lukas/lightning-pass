from __future__ import annotations

from passgen import passgen
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel

from lightning_pass.util.exceptions import StopCollectingPositions


class MouseTracker(QtCore.QObject):
    """This class contains functionality for setting up a mouse tracker over a chosen label.

    :param QLabel widget: QLabel widget which will be used for tracking

    """

    positionChanged = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, widget: QLabel) -> None:
        """Class contructor."""
        super().__init__(widget)
        self._widget = widget
        self.widget.setMouseTracking(True)
        self.widget.installEventFilter(self)

    @property
    def widget(self) -> QLabel:
        return self._widget

    def eventFilter(self, o: QLabel, e: QtCore.QEvent.MouseMove) -> object:
        """Event filter.

        :param QLabel o: Label object
        :param MouseMove e: Mouse move event

        :returns: eventFilter of super class

        """
        if o is self.widget and e.type() == QtCore.QEvent.MouseMove:
            self.positionChanged.emit(e.pos())
        return super().eventFilter(o, e)

    @staticmethod
    def setup_tracker(label: QLabel, on_change) -> None:
        """Setup a mouse tracker over a specified label."""
        tracker = MouseTracker(label)
        tracker.positionChanged.connect(on_change)


class Collector:
    """This class contains functionality for recording current mouse position."""

    def __init__(self):
        """Class contructor."""
        self.randomness_lst = []  # List[Tuple[int, int]]

    def __repr__(self) -> str:
        """Provide information about this class."""
        return f"Collector({self.randomness_lst})"

    def __iter__(self):
        yield from self.randomness_lst

    def collect_position(self, pos: QtCore.QPoint) -> str | bool:
        """Collect mouse position.

        :param QPoint pos: Current cursor position

        :returns: state of the collector list

        :raises StopCollectingPositions: if 1000 mouse positions have been collected

        """
        if len(self.randomness_lst) <= 999:
            self.randomness_lst.append("(%d, %d)" % (pos.x(), pos.y()))
            if len(self.randomness_lst) % 10 == 0:
                return True
        else:
            raise StopCollectingPositions


class PwdGenerator:
    """This class holds user's chosen parameters for password generation
    and contains the password generation functionality.

    :param List[Tuple[int, int]] randomness_lst: Information about mouse positions
    :param int length: Password length
    :param bool numbers: Password option
    :param bool symbols: Password option
    :param bool lowercase: Password option
    :param bool uppercase: Password option

    """

    def __init__(
        self,
        randomness_lst: list[tuple[int, int]],
        length: int,
        numbers: bool,
        symbols: bool,
        lowercase: bool,
        uppercase: bool,
    ) -> None:
        """Class contructor."""
        self.val_lst = randomness_lst
        self.length = length
        self.numbers = numbers
        self.symbols = symbols
        self.lowercase = lowercase
        self.uppercase = uppercase

    def __repr__(self) -> str:
        """Provide information about this class."""
        return f"""Generator(
               {self.val_lst},
               {self.length},
               {self.numbers},
               {self.symbols},
               {self.lowercase},
               {self.uppercase})
               """

    def generate_password(self, case_type: str = "both") -> str:
        """Generate a password by passgen library.
        Password generation is based on the chosen parameters in the GUI.

        :param str case_type: "both" as a default case

        :returns: password generated by passgen

        """
        if self.lowercase and self.uppercase:
            case_type = "both"
        elif self.lowercase is False:
            case_type = "upper"
        elif self.uppercase is False:
            case_type = "lower"

        password = passgen(
            length=self.length,
            punctuation=self.symbols,
            digits=self.numbers,
            case=case_type,
        )
        return password
