"""Test module for the gui package."""
from __future__ import annotations

import pytest
from PyQt5 import QtCore
from pytestqt.qtbot import QtBot

from lightning_pass.gui.window import LightningPassWindow


@pytest.fixture()
def app(qtbot: QtBot) -> LightningPassWindow:
    """Fixture for GUI tests.

    Args:
        qtbot (QtBot): Click on buttons like a human

    Returns:
        app instance with QtBot widget
    """
    test_app = LightningPassWindow()
    qtbot.addWidget(test_app)
    return test_app


@pytest.mark.parametrize(
    "widget, index",
    [
        ("home_login_btn", 2),
        ("home_register_btn", 3),
        ("home_generate_password_btn", 8),
        ("log_main_btn", 1),
        ("log_forgot_pass_btn", 4),
        ("reg_main_btn", 1),
        ("forgot_pass_main_menu_btn", 1),
        ("reset_token_main_btn", 1),
        ("reset_password_main_btn", 1),
        ("change_password_main_btn", 1),
        ("generate_pass_main_menu_btn", 1),
        ("generate_pass_p2_main_btn", 1),
    ],
)
def test_buttons(
    app: LightningPassWindow,
    qtbot: QtBot,
    widget: str,
    index: int,
) -> None:
    """Test if each button correctly switches to correct stacked_widget index.

    Index description:
        1) index 1: app.ui.home
        2) index 2: app.ui.login
        3) index 3: app.ui.register_2
        4) index 4: app.ui.forgot_password
        5) index 5: app.ui.generate_password
        6) index 6: app.ui.generate_pass_phase2
        7) index 7: app.ui.account

    Fails if stacked_widget didn't change index.

    Args:
        app (LightningPassWindow): Main window instance
        qtbot (QtBot): QtBot instance
        widget (str): QPushButton pointer
        index (int): stacked_widget expected index
    """
    widget = getattr(app.ui, widget)

    qtbot.mouseClick(widget, QtCore.Qt.LeftButton)  # act

    assert app.ui.stacked_widget.currentIndex() == index


@pytest.mark.parametrize(
    "menu_bar_action, index",
    [
        ("action_main_menu", 1),
        ("action_generate", 8),
        ("action_login", 2),
        ("action_register", 3),
        ("action_forgot_password", 4),
    ],
)
def test_menu_bar(app: LightningPassWindow, menu_bar_action: str, index: int) -> None:
    """Test if each menu bar action correctly switches to correct stacked_widget
    index.

    Index description:
        1) index 1: app.ui.home
        2) index 2: app.ui.login
        3) index 3: app.ui.register_2
        4) index 4: app.ui.forgot_password
        5) index 5: app.ui.generate_password
        6) index 6: app.ui.generate_pass_phase2
        7) index 7: app.ui.account

    Fails if stacked_widget didn't change index.

    Args:
        app (LightningPassWindow): Main window instance
        menu_bar_action (str): QPushButton pointer
        index (int): stacked_widget expected index
    """
    action = getattr(app.ui, menu_bar_action)

    action.trigger()  # act

    assert app.ui.stacked_widget.currentIndex() == index


__all__ = ["app", "test_buttons", "test_menu_bar"]
