import os
import sys
from pathlib import Path

import mysql.connector as mysql
from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication

from lightning_pass.gui.gui import UiLightningPass


def _copy(self, target):
    """Monkey Patching copy functionality into pathlib.Path object."""
    import shutil

    assert self.is_file()
    shutil.copy(str(self), str(target))  # str() only there for Python --version < 3.6


Path.copy = _copy  # type: ignore


def connect_to_database():
    """Initialize database connection."""
    load_dotenv()
    connection = mysql.connect(
        host=os.getenv("LOGINSDB_HOST"),
        user=os.getenv("LOGINSDB_USER"),
        password=os.getenv("LOGINSDB_PASS"),
        database=os.getenv("LOGINSDB_DB"),
    )
    return connection.cursor(), connection


def create_app():
    """App creation"""
    app = QApplication(sys.argv)
    window = UiLightningPass()
    window.show()
    return app
