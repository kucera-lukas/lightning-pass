import pathlib
import re

import clipboard
import qdarkstyle
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from lightning_pass.gui.mouse_randomness.mouse_tracker import MouseTracker
from lightning_pass.password_generator.collector import Collector
from lightning_pass.password_generator.generator import Generator
from lightning_pass.users.exceptions import (
    EmailAlreadyExists,
    InvalidEmail,
    InvalidPassword,
    InvalidUsername,
    PasswordsDoNotMatch,
    UsernameAlreadyExists,
)
from lightning_pass.users.register import RegisterUser


class Ui_LightningPass(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        """Main window constructor"""
        super().__init__(parent)
        self.main_win = QMainWindow()
        self.setupUi(self.main_win)
        self.stackedWidget.setCurrentWidget(self.home)
        self.setup_buttons()
        self.setup_menu_bar()
        # Dark mode is the default theme.
        self.toggle_stylesheet_dark()

    def show(self):
        """Show main window."""
        self.main_win.show()

    def toggle_stylesheet_light(self, *args):
        """Change stylesheet to light mode."""
        self.main_win.setStyleSheet("")

    def toggle_stylesheet_dark(self, *args):
        """ Change stylesheet to dark mode. """
        self.main_win.setStyleSheet(qdarkstyle.load_stylesheet(qt_api="pyqt5"))

    def setupUi(self, lightning_pass):
        lightning_pass.setObjectName("lightning_pass")
        lightning_pass.resize(671, 352)
        self.centralwidget = QtWidgets.QWidget(lightning_pass)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 612, 281))
        self.stackedWidget.setObjectName("stackedWidget")
        self.home = QtWidgets.QWidget()
        self.home.setObjectName("home")
        self.gridLayout = QtWidgets.QGridLayout(self.home)
        self.gridLayout.setObjectName("gridLayout")
        self.home_register_btn = QtWidgets.QPushButton(self.home)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(16)
        self.home_register_btn.setFont(font)
        self.home_register_btn.setObjectName("home_register_btn")
        self.gridLayout.addWidget(self.home_register_btn, 2, 1, 1, 1)
        self.home_login_btn = QtWidgets.QPushButton(self.home)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(16)
        self.home_login_btn.setFont(font)
        self.home_login_btn.setObjectName("home_login_btn")
        self.gridLayout.addWidget(self.home_login_btn, 1, 1, 1, 1)
        self.home_welcome_lbl = QtWidgets.QLabel(self.home)
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(26)
        font.setBold(False)
        font.setWeight(50)
        self.home_welcome_lbl.setFont(font)
        self.home_welcome_lbl.setLocale(
            QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates)
        )
        self.home_welcome_lbl.setObjectName("home_welcome_lbl")
        self.gridLayout.addWidget(self.home_welcome_lbl, 0, 0, 1, 2)
        self.home_generate_password_btn = QtWidgets.QPushButton(self.home)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(16)
        self.home_generate_password_btn.setFont(font)
        self.home_generate_password_btn.setObjectName("home_generate_password_btn")
        self.gridLayout.addWidget(self.home_generate_password_btn, 1, 0, 2, 1)
        self.stackedWidget.addWidget(self.home)
        self.login = QtWidgets.QWidget()
        self.login.setObjectName("login")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.login)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.log_login_lbl = QtWidgets.QLabel(self.login)
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(26)
        self.log_login_lbl.setFont(font)
        self.log_login_lbl.setObjectName("log_login_lbl")
        self.gridLayout_2.addWidget(self.log_login_lbl, 0, 0, 1, 2)
        self.log_entry_username_lbl = QtWidgets.QLabel(self.login)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.log_entry_username_lbl.setFont(font)
        self.log_entry_username_lbl.setObjectName("log_entry_username_lbl")
        self.gridLayout_2.addWidget(self.log_entry_username_lbl, 1, 0, 1, 1)
        self.log_username_line_edit = QtWidgets.QLineEdit(self.login)
        self.log_username_line_edit.setText("")
        self.log_username_line_edit.setObjectName("log_username_line_edit")
        self.gridLayout_2.addWidget(self.log_username_line_edit, 1, 1, 1, 1)
        self.log_entry_register_lbl = QtWidgets.QLabel(self.login)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.log_entry_register_lbl.setFont(font)
        self.log_entry_register_lbl.setObjectName("log_entry_register_lbl")
        self.gridLayout_2.addWidget(self.log_entry_register_lbl, 2, 0, 1, 1)
        self.log_password_line_edit = QtWidgets.QLineEdit(self.login)
        self.log_password_line_edit.setText("")
        self.log_password_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.log_password_line_edit.setObjectName("log_password_line_edit")
        self.gridLayout_2.addWidget(self.log_password_line_edit, 2, 1, 1, 1)
        self.log_login_btn_2 = QtWidgets.QPushButton(self.login)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.log_login_btn_2.setFont(font)
        self.log_login_btn_2.setObjectName("log_login_btn_2")
        self.gridLayout_2.addWidget(self.log_login_btn_2, 3, 0, 1, 2)
        self.log_forgot_pass_btn = QtWidgets.QPushButton(self.login)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.log_forgot_pass_btn.setFont(font)
        self.log_forgot_pass_btn.setObjectName("log_forgot_pass_btn")
        self.gridLayout_2.addWidget(self.log_forgot_pass_btn, 3, 2, 1, 1)
        self.log_main_btn = QtWidgets.QPushButton(self.login)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.log_main_btn.setFont(font)
        self.log_main_btn.setObjectName("log_main_btn")
        self.gridLayout_2.addWidget(self.log_main_btn, 3, 3, 1, 1)
        self.stackedWidget.addWidget(self.login)
        self.register_2 = QtWidgets.QWidget()
        self.register_2.setObjectName("register_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.register_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.reg_conf_pass_entry_lbl = QtWidgets.QLabel(self.register_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.reg_conf_pass_entry_lbl.setFont(font)
        self.reg_conf_pass_entry_lbl.setObjectName("reg_conf_pass_entry_lbl")
        self.gridLayout_3.addWidget(self.reg_conf_pass_entry_lbl, 3, 0, 1, 1)
        self.reg_register_lbl = QtWidgets.QLabel(self.register_2)
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(26)
        self.reg_register_lbl.setFont(font)
        self.reg_register_lbl.setObjectName("reg_register_lbl")
        self.gridLayout_3.addWidget(self.reg_register_lbl, 0, 0, 1, 4)
        self.reg_username_entry_lbl = QtWidgets.QLabel(self.register_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.reg_username_entry_lbl.setFont(font)
        self.reg_username_entry_lbl.setObjectName("reg_username_entry_lbl")
        self.gridLayout_3.addWidget(self.reg_username_entry_lbl, 1, 0, 1, 1)
        self.reg_password_entry_lbl = QtWidgets.QLabel(self.register_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.reg_password_entry_lbl.setFont(font)
        self.reg_password_entry_lbl.setObjectName("reg_password_entry_lbl")
        self.gridLayout_3.addWidget(self.reg_password_entry_lbl, 2, 0, 1, 1)
        self.reg_email_entry_lbl = QtWidgets.QLabel(self.register_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.reg_email_entry_lbl.setFont(font)
        self.reg_email_entry_lbl.setObjectName("reg_email_entry_lbl")
        self.gridLayout_3.addWidget(self.reg_email_entry_lbl, 4, 0, 1, 1)
        self.reg_conf_pass_line = QtWidgets.QLineEdit(self.register_2)
        self.reg_conf_pass_line.setText("")
        self.reg_conf_pass_line.setEchoMode(QtWidgets.QLineEdit.Password)
        self.reg_conf_pass_line.setObjectName("reg_conf_pass_line")
        self.gridLayout_3.addWidget(self.reg_conf_pass_line, 3, 1, 1, 1)
        self.reg_email_line = QtWidgets.QLineEdit(self.register_2)
        self.reg_email_line.setText("")
        self.reg_email_line.setObjectName("reg_email_line")
        self.gridLayout_3.addWidget(self.reg_email_line, 4, 1, 1, 1)
        self.reg_password_line = QtWidgets.QLineEdit(self.register_2)
        self.reg_password_line.setEchoMode(QtWidgets.QLineEdit.Password)
        self.reg_password_line.setObjectName("reg_password_line")
        self.gridLayout_3.addWidget(self.reg_password_line, 2, 1, 1, 1)
        self.reg_username_line = QtWidgets.QLineEdit(self.register_2)
        self.reg_username_line.setText("")
        self.reg_username_line.setObjectName("reg_username_line")
        self.gridLayout_3.addWidget(self.reg_username_line, 1, 1, 1, 1)
        self.reg_register_btn = QtWidgets.QPushButton(self.register_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.reg_register_btn.setFont(font)
        self.reg_register_btn.setObjectName("reg_register_btn")
        self.gridLayout_3.addWidget(self.reg_register_btn, 5, 0, 1, 2)
        self.reg_main_btn = QtWidgets.QPushButton(self.register_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.reg_main_btn.setFont(font)
        self.reg_main_btn.setObjectName("reg_main_btn")
        self.gridLayout_3.addWidget(self.reg_main_btn, 5, 2, 1, 3)
        self.stackedWidget.addWidget(self.register_2)
        self.forgot_password = QtWidgets.QWidget()
        self.forgot_password.setObjectName("forgot_password")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.forgot_password)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.forgot_pass_lbl = QtWidgets.QLabel(self.forgot_password)
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(26)
        self.forgot_pass_lbl.setFont(font)
        self.forgot_pass_lbl.setObjectName("forgot_pass_lbl")
        self.gridLayout_4.addWidget(self.forgot_pass_lbl, 0, 0, 1, 2)
        self.forgot_pass_email_entry_lbl = QtWidgets.QLabel(self.forgot_password)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.forgot_pass_email_entry_lbl.setFont(font)
        self.forgot_pass_email_entry_lbl.setObjectName("forgot_pass_email_entry_lbl")
        self.gridLayout_4.addWidget(self.forgot_pass_email_entry_lbl, 1, 0, 1, 1)
        self.forgot_pass_email_line = QtWidgets.QLineEdit(self.forgot_password)
        self.forgot_pass_email_line.setObjectName("forgot_pass_email_line")
        self.gridLayout_4.addWidget(self.forgot_pass_email_line, 1, 1, 1, 1)
        self.forgot_pass_reset_btn = QtWidgets.QPushButton(self.forgot_password)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.forgot_pass_reset_btn.setFont(font)
        self.forgot_pass_reset_btn.setObjectName("forgot_pass_reset_btn")
        self.gridLayout_4.addWidget(self.forgot_pass_reset_btn, 2, 0, 1, 2)
        self.forgot_pass_main_menu_btn = QtWidgets.QPushButton(self.forgot_password)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.forgot_pass_main_menu_btn.setFont(font)
        self.forgot_pass_main_menu_btn.setObjectName("forgot_pass_main_menu_btn")
        self.gridLayout_4.addWidget(self.forgot_pass_main_menu_btn, 2, 2, 1, 1)
        self.stackedWidget.addWidget(self.forgot_password)
        self.generate_pass = QtWidgets.QWidget()
        self.generate_pass.setObjectName("generate_pass")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.generate_pass)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.generate_pas_main_lbl = QtWidgets.QLabel(self.generate_pass)
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(26)
        self.generate_pas_main_lbl.setFont(font)
        self.generate_pas_main_lbl.setObjectName("generate_pas_main_lbl")
        self.gridLayout_5.addWidget(self.generate_pas_main_lbl, 0, 0, 1, 6)
        self.generate_pass_length_lbl = QtWidgets.QLabel(self.generate_pass)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.generate_pass_length_lbl.setFont(font)
        self.generate_pass_length_lbl.setObjectName("generate_pass_length_lbl")
        self.gridLayout_5.addWidget(self.generate_pass_length_lbl, 1, 0, 1, 1)
        self.generate_pass_spin_box = QtWidgets.QSpinBox(self.generate_pass)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.generate_pass_spin_box.setFont(font)
        self.generate_pass_spin_box.setMinimum(16)
        self.generate_pass_spin_box.setMaximum(64)
        self.generate_pass_spin_box.setObjectName("generate_pass_spin_box")
        self.gridLayout_5.addWidget(self.generate_pass_spin_box, 1, 1, 1, 1)
        self.generate_pass_numbers_check = QtWidgets.QCheckBox(self.generate_pass)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.generate_pass_numbers_check.setFont(font)
        self.generate_pass_numbers_check.setChecked(True)
        self.generate_pass_numbers_check.setObjectName("generate_pass_numbers_check")
        self.gridLayout_5.addWidget(self.generate_pass_numbers_check, 1, 2, 1, 1)
        self.generate_pass_symbols_check = QtWidgets.QCheckBox(self.generate_pass)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.generate_pass_symbols_check.setFont(font)
        self.generate_pass_symbols_check.setChecked(True)
        self.generate_pass_symbols_check.setObjectName("generate_pass_symbols_check")
        self.gridLayout_5.addWidget(self.generate_pass_symbols_check, 1, 3, 1, 1)
        self.generate_pass_lower_check = QtWidgets.QCheckBox(self.generate_pass)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.generate_pass_lower_check.setFont(font)
        self.generate_pass_lower_check.setChecked(True)
        self.generate_pass_lower_check.setObjectName("generate_pass_lower_check")
        self.gridLayout_5.addWidget(self.generate_pass_lower_check, 1, 4, 1, 1)
        self.generate_pass_upper_check = QtWidgets.QCheckBox(self.generate_pass)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.generate_pass_upper_check.setFont(font)
        self.generate_pass_upper_check.setChecked(True)
        self.generate_pass_upper_check.setObjectName("generate_pass_upper_check")
        self.gridLayout_5.addWidget(self.generate_pass_upper_check, 1, 5, 1, 1)
        self.generate_pass_generate_btn = QtWidgets.QPushButton(self.generate_pass)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.generate_pass_generate_btn.setFont(font)
        self.generate_pass_generate_btn.setObjectName("generate_pass_generate_btn")
        self.gridLayout_5.addWidget(self.generate_pass_generate_btn, 2, 0, 1, 5)
        self.generate_pass_main_menu_btn = QtWidgets.QPushButton(self.generate_pass)
        self.generate_pass_main_menu_btn.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.generate_pass_main_menu_btn.setFont(font)
        self.generate_pass_main_menu_btn.setObjectName("generate_pass_main_menu_btn")
        self.gridLayout_5.addWidget(self.generate_pass_main_menu_btn, 2, 5, 1, 1)
        self.stackedWidget.addWidget(self.generate_pass)
        self.generate_pass_phase2 = QtWidgets.QWidget()
        self.generate_pass_phase2.setObjectName("generate_pass_phase2")
        self.generate_pass_p2_prgrs_bar = QtWidgets.QProgressBar(
            self.generate_pass_phase2
        )
        self.generate_pass_p2_prgrs_bar.setEnabled(True)
        self.generate_pass_p2_prgrs_bar.setGeometry(QtCore.QRect(10, 140, 591, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.generate_pass_p2_prgrs_bar.setFont(font)
        self.generate_pass_p2_prgrs_bar.setProperty("value", 0)
        self.generate_pass_p2_prgrs_bar.setTextVisible(True)
        self.generate_pass_p2_prgrs_bar.setObjectName("generate_pass_p2_prgrs_bar")
        self.generate_pass_p2_rnd_lbl = QtWidgets.QLabel(self.generate_pass_phase2)
        self.generate_pass_p2_rnd_lbl.setEnabled(True)
        self.generate_pass_p2_rnd_lbl.setGeometry(QtCore.QRect(10, 0, 471, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.generate_pass_p2_rnd_lbl.setFont(font)
        self.generate_pass_p2_rnd_lbl.setObjectName("generate_pass_p2_rnd_lbl")
        self.generate_pass_p2_tracking_lbl = QtWidgets.QLabel(self.generate_pass_phase2)
        self.generate_pass_p2_tracking_lbl.setEnabled(True)
        self.generate_pass_p2_tracking_lbl.setGeometry(QtCore.QRect(10, 40, 591, 91))
        self.generate_pass_p2_tracking_lbl.setMouseTracking(True)
        self.generate_pass_p2_tracking_lbl.setStyleSheet(
            "background-color: blue; border: 3px solid black"
        )
        self.generate_pass_p2_tracking_lbl.setText("")
        self.generate_pass_p2_tracking_lbl.setObjectName(
            "generate_pass_p2_tracking_lbl"
        )
        self.generate_pass_p2_final_lbl = QtWidgets.QLabel(self.generate_pass_phase2)
        self.generate_pass_p2_final_lbl.setGeometry(QtCore.QRect(10, 170, 161, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.generate_pass_p2_final_lbl.setFont(font)
        self.generate_pass_p2_final_lbl.setObjectName("generate_pass_p2_final_lbl")
        self.generate_pass_p2_final_pass_line = QtWidgets.QLineEdit(
            self.generate_pass_phase2
        )
        self.generate_pass_p2_final_pass_line.setGeometry(
            QtCore.QRect(170, 170, 431, 41)
        )
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.generate_pass_p2_final_pass_line.setFont(font)
        self.generate_pass_p2_final_pass_line.setText("")
        self.generate_pass_p2_final_pass_line.setReadOnly(True)
        self.generate_pass_p2_final_pass_line.setObjectName(
            "generate_pass_p2_final_pass_line"
        )
        self.generate_pass_p2_copy_btn = QtWidgets.QPushButton(
            self.generate_pass_phase2
        )
        self.generate_pass_p2_copy_btn.setGeometry(QtCore.QRect(10, 220, 481, 28))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.generate_pass_p2_copy_btn.setFont(font)
        self.generate_pass_p2_copy_btn.setObjectName("generate_pass_p2_copy_btn")
        self.generate_pass_p2_main_btn = QtWidgets.QPushButton(
            self.generate_pass_phase2
        )
        self.generate_pass_p2_main_btn.setGeometry(QtCore.QRect(500, 220, 101, 28))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.generate_pass_p2_main_btn.setFont(font)
        self.generate_pass_p2_main_btn.setObjectName("generate_pass_p2_main_btn")
        self.stackedWidget.addWidget(self.generate_pass_phase2)
        lightning_pass.setCentralWidget(self.centralwidget)
        self.menu_bar = QtWidgets.QMenuBar(lightning_pass)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 671, 26))
        self.menu_bar.setObjectName("menu_bar")
        self.menu_users = QtWidgets.QMenu(self.menu_bar)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.menu_users.setFont(font)
        self.menu_users.setObjectName("menu_users")
        self.menu_account = QtWidgets.QMenu(self.menu_users)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.menu_account.setFont(font)
        self.menu_account.setObjectName("menu_account")
        self.menu_password = QtWidgets.QMenu(self.menu_bar)
        self.menu_password.setObjectName("menu_password")
        self.menu_general = QtWidgets.QMenu(self.menu_bar)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.menu_general.setFont(font)
        self.menu_general.setObjectName("menu_general")
        self.menu_theme = QtWidgets.QMenu(self.menu_general)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.menu_theme.setFont(font)
        self.menu_theme.setObjectName("menu_theme")
        lightning_pass.setMenuBar(self.menu_bar)
        self.statusbar = QtWidgets.QStatusBar(lightning_pass)
        self.statusbar.setObjectName("statusbar")
        lightning_pass.setStatusBar(self.statusbar)
        self.actionlogin = QtWidgets.QAction(lightning_pass)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.actionlogin.setFont(font)
        self.actionlogin.setObjectName("actionlogin")
        self.actionregister = QtWidgets.QAction(lightning_pass)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.actionregister.setFont(font)
        self.actionregister.setObjectName("actionregister")
        self.action_generate = QtWidgets.QAction(lightning_pass)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.action_generate.setFont(font)
        self.action_generate.setObjectName("action_generate")
        self.action_login = QtWidgets.QAction(lightning_pass)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.action_login.setFont(font)
        self.action_login.setObjectName("action_login")
        self.action_register = QtWidgets.QAction(lightning_pass)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.action_register.setFont(font)
        self.action_register.setObjectName("action_register")
        self.action_forgot_password = QtWidgets.QAction(lightning_pass)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.action_forgot_password.setFont(font)
        self.action_forgot_password.setObjectName("action_forgot_password")
        self.action_main_menu = QtWidgets.QAction(lightning_pass)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.action_main_menu.setFont(font)
        self.action_main_menu.setObjectName("action_main_menu")
        self.action_light = QtWidgets.QAction(lightning_pass)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.action_light.setFont(font)
        self.action_light.setObjectName("action_light")
        self.action_dark = QtWidgets.QAction(lightning_pass)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.action_dark.setFont(font)
        self.action_dark.setObjectName("action_dark")
        self.menu_account.addAction(self.action_login)
        self.menu_account.addAction(self.action_register)
        self.menu_account.addAction(self.action_forgot_password)
        self.menu_users.addAction(self.menu_account.menuAction())
        self.menu_password.addAction(self.action_generate)
        self.menu_theme.addAction(self.action_light)
        self.menu_theme.addAction(self.action_dark)
        self.menu_general.addAction(self.action_main_menu)
        self.menu_general.addAction(self.menu_theme.menuAction())
        self.menu_bar.addAction(self.menu_general.menuAction())
        self.menu_bar.addAction(self.menu_password.menuAction())
        self.menu_bar.addAction(self.menu_users.menuAction())

        self.retranslateUi(lightning_pass)
        self.stackedWidget.setCurrentIndex(5)
        QtCore.QMetaObject.connectSlotsByName(lightning_pass)

    def retranslateUi(self, lightning_pass):
        _translate = QtCore.QCoreApplication.translate
        lightning_pass.setWindowTitle(_translate("lightning_pass", "Lightning Pass"))
        self.home_register_btn.setText(_translate("lightning_pass", "Register"))
        self.home_login_btn.setText(_translate("lightning_pass", "Login"))
        self.home_welcome_lbl.setText(
            _translate("lightning_pass", "Welcome to Lightning Pass!")
        )
        self.home_generate_password_btn.setText(
            _translate("lightning_pass", "Generate Password")
        )
        self.log_login_lbl.setText(_translate("lightning_pass", "Login"))
        self.log_entry_username_lbl.setText(_translate("lightning_pass", "Username:"))
        self.log_entry_register_lbl.setText(_translate("lightning_pass", "Password:"))
        self.log_login_btn_2.setText(_translate("lightning_pass", "Login"))
        self.log_forgot_pass_btn.setText(
            _translate("lightning_pass", "Forgot Password?")
        )
        self.log_main_btn.setText(_translate("lightning_pass", "Main Menu"))
        self.reg_conf_pass_entry_lbl.setText(
            _translate("lightning_pass", "Confirm Password:")
        )
        self.reg_register_lbl.setText(_translate("lightning_pass", "Register"))
        self.reg_username_entry_lbl.setText(_translate("lightning_pass", "Username:"))
        self.reg_password_entry_lbl.setText(_translate("lightning_pass", "Password:"))
        self.reg_email_entry_lbl.setText(_translate("lightning_pass", "Email:"))
        self.reg_register_btn.setText(_translate("lightning_pass", "Register"))
        self.reg_main_btn.setText(_translate("lightning_pass", "Main Menu"))
        self.forgot_pass_lbl.setText(_translate("lightning_pass", "Forgot Password"))
        self.forgot_pass_email_entry_lbl.setText(_translate("lightning_pass", "Email:"))
        self.forgot_pass_reset_btn.setText(
            _translate("lightning_pass", "Send reset token")
        )
        self.forgot_pass_main_menu_btn.setText(
            _translate("lightning_pass", "Main Menu")
        )
        self.generate_pas_main_lbl.setText(
            _translate("lightning_pass", "Generate Password")
        )
        self.generate_pass_length_lbl.setText(
            _translate("lightning_pass", "Password length:")
        )
        self.generate_pass_numbers_check.setText(
            _translate("lightning_pass", "Numbers")
        )
        self.generate_pass_symbols_check.setText(
            _translate("lightning_pass", "Symbols")
        )
        self.generate_pass_lower_check.setText(
            _translate("lightning_pass", "Lowercase")
        )
        self.generate_pass_upper_check.setText(
            _translate("lightning_pass", "Uppercase")
        )
        self.generate_pass_generate_btn.setText(
            _translate("lightning_pass", "Generate")
        )
        self.generate_pass_main_menu_btn.setText(
            _translate("lightning_pass", "Main Menu")
        )
        self.generate_pass_p2_rnd_lbl.setText(
            _translate(
                "lightning_pass",
                "Generate randomness by moving the mouse over the blue area.",
            )
        )
        self.generate_pass_p2_final_lbl.setText(
            _translate("lightning_pass", "Generated password:")
        )
        self.generate_pass_p2_copy_btn.setText(
            _translate("lightning_pass", "Copy Password")
        )
        self.generate_pass_p2_main_btn.setText(
            _translate("lightning_pass", "Main Menu")
        )
        self.menu_users.setTitle(_translate("lightning_pass", "users"))
        self.menu_account.setTitle(_translate("lightning_pass", "account"))
        self.menu_password.setTitle(_translate("lightning_pass", "password"))
        self.menu_general.setTitle(_translate("lightning_pass", "general"))
        self.menu_theme.setTitle(_translate("lightning_pass", "theme"))
        self.actionlogin.setText(_translate("lightning_pass", "login"))
        self.actionregister.setText(_translate("lightning_pass", "register"))
        self.action_generate.setText(_translate("lightning_pass", "generate"))
        self.action_login.setText(_translate("lightning_pass", "login"))
        self.action_register.setText(_translate("lightning_pass", "register"))
        self.action_forgot_password.setText(
            _translate("lightning_pass", "forgot_password")
        )
        self.action_main_menu.setText(_translate("lightning_pass", "main menu"))
        self.action_light.setText(_translate("lightning_pass", "light"))
        self.action_dark.setText(_translate("lightning_pass", "dark"))

    def setup_buttons(self):
        """Connect all buttons."""
        self.home_login_btn.clicked.connect(self.login_event)
        self.home_register_btn.clicked.connect(self.register_event)
        self.home_generate_password_btn.clicked.connect(self.generate_pass_event)

        self.log_main_btn.clicked.connect(self.home_event)
        self.log_forgot_pass_btn.clicked.connect(self.forgot_password_event)

        self.reg_main_btn.clicked.connect(self.home_event)
        self.reg_register_btn.clicked.connect(self.register_user_event)

        self.forgot_pass_main_menu_btn.clicked.connect(self.home_event)

        self.generate_pass_generate_btn.clicked.connect(self.generate_pass_phase2_event)
        self.generate_pass_main_menu_btn.clicked.connect(self.home_event)
        self.generate_pass_p2_main_btn.clicked.connect(self.home_event)
        self.generate_pass_p2_copy_btn.clicked.connect(self.copy_password_event)

    def setup_menu_bar(self):
        """Connect menu bar."""
        self.action_main_menu.triggered.connect(self.home_event)
        self.action_light.triggered.connect(
            lambda: self.toggle_stylesheet_light(
                f"{pathlib.Path(__file__).parent}\\static\\light.qss"
            )
        )
        self.action_dark.triggered.connect(
            lambda: self.toggle_stylesheet_dark(
                f"{pathlib.Path(__file__).parent}\\static\\dark.qss"
            )
        )
        self.action_generate.triggered.connect(self.generate_pass_event)
        self.action_login.triggered.connect(self.login_event)
        self.action_register.triggered.connect(self.register_event)
        self.action_forgot_password.triggered.connect(self.forgot_password_event)

    def home_event(self):
        """Switch to home widget."""
        self.stackedWidget.setCurrentWidget(self.home)

    def login_event(self):
        """Switch to login widget and reset previous values."""
        self.log_username_line_edit.setText("")
        self.log_password_line_edit.setText("")
        self.stackedWidget.setCurrentWidget(self.login)

    def register_event(self):
        """Switch to register widget and reset previous values."""
        self.reg_username_line.setText("")
        self.reg_password_line.setText("")
        self.reg_conf_pass_line.setText("")
        self.reg_email_line.setText("")
        self.stackedWidget.setCurrentWidget(self.register_2)

    def register_user_event(self):
        """Try to register a user. If succesful, show login widget."""

        user_to_register = RegisterUser(
            self.reg_username_line.text(),
            self.reg_password_line.text(),
            self.reg_conf_pass_line.text(),
            self.reg_email_line.text(),
        )
        title_register = "Lightning Pass - Register"
        try:
            user_to_register.insert_into_db()
        except InvalidUsername:
            self.show_message_box(
                title_register,
                "This username is invalid.",
                QMessageBox.Warning,
            )
        except InvalidPassword:
            self.show_message_box(
                title_register,
                "This password is invalid.",
                QMessageBox.Warning,
            )
        except InvalidEmail:
            self.show_message_box(
                title_register,
                "This email is invalid.",
                QMessageBox.Warning,
            )
        except UsernameAlreadyExists:
            self.show_message_box(
                title_register,
                "This username already exists.",
                QMessageBox.Warning,
            )
        except EmailAlreadyExists:
            self.show_message_box(
                title_register,
                "This email already exists.",
                QMessageBox.Warning,
            )
        except PasswordsDoNotMatch:
            self.show_message_box(
                title_register,
                "The passwords you entered do not match.",
                QMessageBox.Warning,
            )
        else:
            self.show_message_box(
                title_register,
                "Account successfully created!",
                QMessageBox.Question,
                successful_registration=True,
            )

    def forgot_password_event(self):
        """Switch to forgot password widget and reset previous email."""
        self.forgot_pass_email_line.setText("")
        self.stackedWidget.setCurrentWidget(self.forgot_password)

    def generate_pass_event(self):
        """Switch to first password generation widget and reset previous password options."""
        self.pass_vals = Collector()
        self.generate_pass_spin_box.setValue(16)
        self.generate_pass_numbers_check.setChecked(True)
        self.generate_pass_symbols_check.setChecked(True)
        self.generate_pass_lower_check.setChecked(True)
        self.generate_pass_upper_check.setChecked(True)
        self.stackedWidget.setCurrentWidget(self.generate_pass)

    def generate_pass_phase2_event(self):
        """Switch to second password generation widget and reset previous values."""
        MouseTracker.setup_tracker(
            self.generate_pass_p2_tracking_lbl, self.on_position_changed
        )
        self.progress = 0
        self.generate_pass_p2_prgrs_bar.setValue(self.progress)
        self.generate_pass_p2_final_pass_line.setText("")
        self.password_generated = False
        if (
            not self.generate_pass_lower_check.isChecked()
            and not self.generate_pass_upper_check.isChecked()
        ):
            self.show_message_box(
                "Lightning Pass - Generator",
                "Can't generate password without any case type.",
                QMessageBox.Warning,
            )
        else:
            self.password_generated = False
            self.stackedWidget.setCurrentWidget(self.generate_pass_phase2)

    def copy_password_event(self):
        """Copy generated password into clipboard."""
        clipboard.copy(self.generate_pass_p2_final_pass_line.text())

    @QtCore.pyqtSlot(QtCore.QPoint)
    def on_position_changed(self, pos):
        """Handler for changes in mouse position over connected label."""
        val = self.pass_vals.collect_position(pos)
        if val == "Done":
            if not self.password_generated:
                self.pass_gen = Generator(
                    self.pass_vals.randomness_lst,
                    self.generate_pass_spin_box.value(),
                    True if self.generate_pass_numbers_check.isChecked() else False,
                    True if self.generate_pass_symbols_check.isChecked() else False,
                    True if self.generate_pass_lower_check.isChecked() else False,
                    True if self.generate_pass_upper_check.isChecked() else False,
                )
                self.generate_pass_p2_final_pass_line.setText(
                    self.pass_gen.generate_password()
                )
            self.password_generated = True
        elif val is True:
            self.progress += 1
            self.generate_pass_p2_prgrs_bar.setValue(self.progress)

    def message_box_event(self, btn):
        """Handler for clicks on message box window"""
        print(btn.text())
        if re.findall("Yes", btn.text()):
            self.login_event()
        if re.findall("Cancel", btn.text()):
            self.register_event()

    def show_message_box(self, title, text, icon, successful_registration=False):
        """Show message box with information about registration process"""
        er = QMessageBox(self.main_win)
        er.setWindowTitle(title)
        er.setText(text)
        er.setIcon(icon)
        if successful_registration is True:
            er.setInformativeText("Would you like to move to the login page?")
            er.setStandardButtons(QMessageBox.Yes | QMessageBox.Close)
            er.setDefaultButton(QMessageBox.Yes)
            er.buttonClicked.connect(self.message_box_event)
        _ = er.exec_()
