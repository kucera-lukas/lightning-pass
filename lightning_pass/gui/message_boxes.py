"""Module containing the MessageBoxes class used for showing various message boxes."""
import contextlib
import functools
from typing import Any, Callable, Optional, Union

from PyQt5 import QtGui
from PyQt5.QtWidgets import (
    QInputDialog,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QWidget,
)

from lightning_pass.util.credentials import Password


def partial_factory(func: Callable, *args: Optional[Any], **kwargs: Optional[Any]):
    """Return a new partial function.

    :param func: The function which will be made partial
    :param args: Optional positional arguments
    :param kwargs: Optional keyword arguments

    :returns: the partial function

    """
    return functools.partial(func, *args, **kwargs)


def event_handler_factory(options: dict[str, Callable[[], None]]) -> Callable[[], None]:
    """Generate a new event handler.

    :param options: Dictionary containing keys and functions tied to them.

    :returns: the event handler

    """

    def handler(btn: QPushButton) -> None:
        """Handle clicks on message box window.

        :param btn: Clicked button

        """
        with contextlib.suppress(KeyError):
            event = options[btn.text()]
        with contextlib.suppress(UnboundLocalError):
            event()

    return handler


class MessageBoxes(QWidget):
    """This class holds the functionality to show various message boxes."""

    def __init__(self, child: QMainWindow, parent: QMainWindow) -> None:
        """Class constructor."""
        super().__init__(parent)
        self.main_win = child
        self.parent = parent
        self.events = parent.events
        self.title = child.windowTitle()

    def message_box_factory(
        self,
        parent_lbl: str,
        text: str,
        icon: QMessageBox.Icon = QMessageBox.Warning,
        informative_text: str = None,
        standard_buttons: Union[
            QMessageBox.StandardButtons,
            QMessageBox.StandardButton,
        ] = None,
        default_button: QMessageBox.StandardButton = None,
        event_handler: Callable = None,
    ) -> QMessageBox:
        """Return a message box initialized with the given params.

        :param parent_lbl: Specifies which window instantiated the new message box
        :param text: Main text to be displayed on the message box
        :param icon: Message box icon type, defaults to QMessageBox.Warning
        :param informative_text: Additional text, defaults to None
        :param standard_buttons: Extra buttons to be shown on the message box, defaults to None
        :param default_button: Default button, defaults to None
        :param event_handler: Handler for clicks on buttons, defaults to None

        :returns: the message box

        """
        box = QMessageBox(self.main_win)
        box.setWindowTitle(f"{self.title} - {parent_lbl}")
        box.setText(text)
        box.setIcon(icon)
        box.setInformativeText(informative_text)

        # supress TypeError if this information is missing
        with contextlib.suppress(TypeError):
            box.setStandardButtons(standard_buttons)
            box.setDefaultButton(default_button)
            box.buttonClicked.connect(event_handler)

        return box

    def _invalid_item_box(self, item: str, parent_lbl: str) -> message_box_factory:
        """Show message box indicating that the entered value is not correct.

        :param str item: Specifies which detail was incorrect
        :param str parent_lbl: Specifies which window instantiated current box

        """
        return partial_factory(
            self.message_box_factory,
            parent_lbl,
            f"This {item} is invalid.",
            QMessageBox.Warning,
        )

    def _item_already_exists_box(
        self, item: str, parent_lbl: str
    ) -> message_box_factory:
        """Handle message boxes with information about existence of entered values.

        :param str parent_lbl: Specifies which window instantiated current box

        """
        return partial_factory(
            self.message_box_factory,
            parent_lbl,
            f"This {item} already exists. Please use different {item}.",
            QMessageBox.Warning,
        )

    def _yes_no_box(self, handler, default_btn: str = "No") -> message_box_factory:
        """Return a partially initialized message box with yes and no buttons.

        :param default_btn: Which button should me the default one, defaults to "No"
        :param handler: Event handler for click on the two yes | no buttons

        """
        return partial_factory(
            self.message_box_factory,
            standard_buttons=QMessageBox.Yes | QMessageBox.No,
            default_button=getattr(QMessageBox, default_btn),
            event_handler=handler,
        )

    def invalid_username_box(self, parent_lbl: str) -> None:
        """Show invalid username message box.

        :param str parent_lbl: Specifies which window instantiated current box

        """
        box = self._invalid_item_box("username", parent_lbl)
        box(informative_text="Username be at least 5 characters long.").exec()

    def invalid_password_box(self, parent_lbl: str, item: str = "password") -> None:
        """Show invalid password message box.

        :param parent_lbl: Specifies which window instantiated current box
        :param item: Optional argument to change the invalid item
            (should be connected to password due to informative text), defaults to "password"

        """
        box = self._invalid_item_box(item, parent_lbl)
        item = item[0].upper() + item[1::1]
        box(
            informative_text=(
                f"""{item} must be at least 8 characters long,
contain at least 1 capital letter,
contain at least 1 number and
contain at least one special character."""
            )
        ).exec()

    def invalid_email_box(self, parent_lbl: str) -> None:
        """Show invalid email message box.

        :param str parent_lbl: Specifies which window instantiated current box

        """
        self._invalid_item_box("email", parent_lbl)().exec()

    def invalid_token_box(self, parent_lbl: str) -> None:
        """Show invalid token message box.

        :param str parent_lbl: Specifies which window instantiated current box

        """
        event_handler = event_handler_factory(
            {"&Yes": self.events.forgot_password_event}
        )

        box = self._yes_no_box(event_handler, "Yes")
        box(
            parent_lbl,
            text="This token is invalid",
            informative_text="Would you like to generate a token?",
        ).exec()

    def username_already_exists_box(self, parent_lbl: str) -> None:
        """Show username already exists message box.

        :param str parent_lbl: Specifies which window instantiated current box

        """
        self._item_already_exists_box("username", parent_lbl)().exec()

    def email_already_exists_box(self, parent_lbl: str) -> None:
        """Show email already exists message box.

        :param str parent_lbl: Specifies which window instantiated current box

        """
        self._item_already_exists_box("email", parent_lbl)().exec()

    def passwords_do_not_match_box(self, parent_lbl: str) -> None:
        """Show passwords do not match message box.

        :param str parent_lbl: Specifies which window instantiated current box

        """
        self.message_box_factory(
            parent_lbl,
            text="Passwords don't match.",
            informative_text="Please try again.",
        ).exec()

    def account_creation_box(self, parent_lbl: Optional[str] = "Register") -> None:
        """Show successful account creation message box.

        :param str parent_lbl: Specifies which window instantiated current box, defaults to "Register"

        """
        event_handler = event_handler_factory(
            {"&Yes": self.events.login_event, "&No": self.events.register_event},
        )

        box = self._yes_no_box(event_handler, "Yes")
        box(
            parent_lbl,
            text="Account successfully created.",
            icon=QMessageBox.Question,
            informative_text="Would you like to move to the login page?",
        ).exec()

    def invalid_login_box(self, parent_lbl: str) -> None:
        """Show invalid login message box.

        :param str parent_lbl: Specifies which window instantiated current box

        """
        event_handler = event_handler_factory(
            {"&Yes": self.events.forgot_password_event}
        )

        box = self._yes_no_box(event_handler, "Yes")
        box(
            parent_lbl,
            text="Could not authenticate an account with the given credentials.",
            informative_text="Forgot password?",
        ).exec()

    def login_required_box(self, parent_lbl: str, page: Optional[str] = None) -> None:
        """Show message box indicating that password can't be generated with current case type option.

        :param parent_lbl: Specifies which window instantiated current box
        :param page: The page which the user tried to access, defaults to None

        """
        event_handler = event_handler_factory({"&Yes": self.events.login_event})

        text = (
            f"Please log in to access the {page} page."
            if page
            else f"Please log in to access that page."
        )

        box = self._yes_no_box(event_handler, "No")
        box(
            parent_lbl,
            text,
            informative_text="Would you like to move to the login page?",
        ).exec()

    def detail_updated_box(
        self,
        parent_lbl: str,
        detail: str,
    ) -> None:
        """Show message box indicating that a user details has been successfully updated.

        :param str detail: Specifies which detail was updated
        :param str parent_lbl: Specifies which window instantiated current box

        """
        self.message_box_factory(
            parent_lbl,
            text=f"Your {detail} has been successfully updated!",
            icon=QMessageBox.Question,
        ).exec()

    def reset_email_sent_box(self, parent_lbl: str) -> None:
        """Show message box indicating that a reset email has been sent.

        :param str parent_lbl: Specifies which window instantiated current box

        """
        event_handler = event_handler_factory({"&Yes": self.events.reset_token_event})

        box = self._yes_no_box(event_handler, "Yes")
        box(
            parent_lbl,
            text="The reset email has been sent.",
            icon=QMessageBox.Question,
            informative_text="Would you like to move to the token page now?",
        ).exec()

    def no_options_generate_box(self, parent_lbl: str) -> None:
        """Show a message box indicating that password can't be generated without a single option.

        :param str parent_lbl: Specifies which window instantiated current box

        """
        self.message_box_factory(
            parent_lbl,
            text="Password can't be generate without a single parameter.",
        ).exec()

    def master_password_required_box(
        self, parent_lbl: Optional[str] = "Master Password", page: Optional[str] = None
    ) -> None:
        """Show message box indicating that the current user needs to setup master password to proceed.

        :param parent_lbl: The window which instantiated the current box, defaults to "Master Password"
        :param page: The page which the user tried to access

        """
        event_handler = event_handler_factory(
            {"&Yes": self.events.master_password_event},
        )

        text = (
            f"You need to set up a master password to access the {page} page."
            if page
            else f"You need to set up a master password to proceed."
        )

        box = self._yes_no_box(event_handler, "No")
        box(
            parent_lbl,
            text,
            informative_text="Would you like to move to the master password page?",
        ).exec()

    def vault_unlock_required_box(
        self,
        parent_lbl: Optional[str] = "Vault",
        page: Optional[str] = None,
    ) -> None:
        """Show a message box indicating that the current user needs unlock the master vault to proceed.

        :param parent_lbl: Specifies which window instantiated the current box
        :param page: The page which the user tried to access

        """
        event_handler = event_handler_factory(
            {"&Yes": self.events.master_password_dialog_event},
        )

        text = (
            f"Please unlock your vault to access the {page} page."
            if page
            else "Please unlock your vault to access that page."
        )

        box = self._yes_no_box(event_handler, "Yes")
        box(
            parent_lbl,
            text,
            informative_text="Would you like to unlock it?",
        ).exec()


class InputDialogs(QWidget):
    def __init__(self, child: QMainWindow, parent: QMainWindow) -> None:
        """Class constructor."""
        super().__init__(parent)
        self.events = parent.events
        self.main_win = child
        self.title = "Lightning Pass"

    def master_password_dialog(
        self,
        parent_lbl: str,
        account_username: str,
    ) -> Union[str, bool]:
        """Show a dialog asking user to enter their master password.

        :param parent_lbl: The window which instantiated the current dialog
        :param account_username: The username of the current user

        """
        password, i = QInputDialog.getText(
            self.main_win,
            parent_lbl,
            f"Master password for {account_username}:",
            QLineEdit.Password,
        )

        return password if i else False


__all__ = [
    "MessageBoxes",
]
