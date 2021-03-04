from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class Ui_LightningPass(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_win = QMainWindow()
        self.setupUi(self.main_win)
        self.stackedWidget.setCurrentWidget(self.home)
        self.setup_buttons()

    def show(self):
        self.main_win.show()

    def setupUi(self, lightning_pass):
        lightning_pass.setObjectName("lightning_pass")
        lightning_pass.resize(644, 299)
        self.centralwidget = QtWidgets.QWidget(lightning_pass)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 612, 247))
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
        self.reg_conf_pass_line.setObjectName("reg_conf_pass_line")
        self.gridLayout_3.addWidget(self.reg_conf_pass_line, 3, 1, 1, 1)
        self.reg_email_line = QtWidgets.QLineEdit(self.register_2)
        self.reg_email_line.setText("")
        self.reg_email_line.setObjectName("reg_email_line")
        self.gridLayout_3.addWidget(self.reg_email_line, 4, 1, 1, 1)
        self.reg_password_line = QtWidgets.QLineEdit(self.register_2)
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
        lightning_pass.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(lightning_pass)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 644, 26))
        self.menubar.setObjectName("menubar")
        self.menulogin = QtWidgets.QMenu(self.menubar)
        self.menulogin.setObjectName("menulogin")
        self.menuaccount = QtWidgets.QMenu(self.menulogin)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.menuaccount.setFont(font)
        self.menuaccount.setObjectName("menuaccount")
        self.menupassword = QtWidgets.QMenu(self.menubar)
        self.menupassword.setObjectName("menupassword")
        lightning_pass.setMenuBar(self.menubar)
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
        self.actiongenerate = QtWidgets.QAction(lightning_pass)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.actiongenerate.setFont(font)
        self.actiongenerate.setObjectName("actiongenerate")
        self.actionlogin_2 = QtWidgets.QAction(lightning_pass)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.actionlogin_2.setFont(font)
        self.actionlogin_2.setObjectName("actionlogin_2")
        self.actionregister_2 = QtWidgets.QAction(lightning_pass)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.actionregister_2.setFont(font)
        self.actionregister_2.setObjectName("actionregister_2")
        self.actionforgot_password = QtWidgets.QAction(lightning_pass)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.actionforgot_password.setFont(font)
        self.actionforgot_password.setObjectName("actionforgot_password")
        self.menuaccount.addAction(self.actionlogin_2)
        self.menuaccount.addAction(self.actionregister_2)
        self.menuaccount.addAction(self.actionforgot_password)
        self.menulogin.addAction(self.menuaccount.menuAction())
        self.menupassword.addAction(self.actiongenerate)
        self.menubar.addAction(self.menupassword.menuAction())
        self.menubar.addAction(self.menulogin.menuAction())

        self.retranslateUi(lightning_pass)
        self.stackedWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(lightning_pass)

    def retranslateUi(self, lightning_pass):
        _translate = QtCore.QCoreApplication.translate
        lightning_pass.setWindowTitle(_translate("lightning_pass", "MainWindow"))
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
        self.menulogin.setTitle(_translate("lightning_pass", "users"))
        self.menuaccount.setTitle(_translate("lightning_pass", "account"))
        self.menupassword.setTitle(_translate("lightning_pass", "password"))
        self.actionlogin.setText(_translate("lightning_pass", "login"))
        self.actionregister.setText(_translate("lightning_pass", "register"))
        self.actiongenerate.setText(_translate("lightning_pass", "generate"))
        self.actionlogin_2.setText(_translate("lightning_pass", "login"))
        self.actionregister_2.setText(_translate("lightning_pass", "register"))
        self.actionforgot_password.setText(
            _translate("lightning_pass", "forgot_password")
        )

    def setup_buttons(self):
        self.home_login_btn.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.login)
        )
        self.home_register_btn.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.register_2)
        )
        self.log_main_btn.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.home)
        )
        self.reg_main_btn.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.home)
        )
        self.forgot_pass_main_menu_btn.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.home)
        )
        self.log_forgot_pass_btn.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.forgot_password)
        )
