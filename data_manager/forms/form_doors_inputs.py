from PyQt5.QtWidgets import QWidget, QPushButton, QToolBar, QVBoxLayout, QLabel, QListWidget, QLineEdit, QComboBox, QHBoxLayout, QSizePolicy, QToolButton
from PyQt5.QtCore import Qt, pyqtSignal, QSettings, QSize
from PyQt5.QtGui import QFont, QPalette, QIcon

import qtawesome as qta

from ui.form_general_ui import Ui_Form

from components.helper_functions import validate_line_edits, layout_generate_one_row



class FormDoorsInputs(QWidget, Ui_Form):


    send_inputs_from_doors_connection_form = pyqtSignal(bool, str, str, str, str) # all_modules, app_path, database, user, password

    def __init__(self, DATA_MANAGER, all_modules: bool):
        super().__init__()
        self.setupUi(self)
        self.setWindowOpacity(0.95)  
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)        
        self.setMaximumSize(500, 500)                 
        self.uiLabelTitle.setText("Doors Connection")
        # self.setStyleSheet(STYLES)
        self.uiLabelTitle.setStyleSheet("")

        self.uiBtnTitleBarClose.clicked.connect(self.close)
        self.uiBtnStatusBarClose.clicked.connect(self.close)
        self.uiBtnOK.clicked.connect(self._ok_clicked)
        
        self.DATA_MANAGER = DATA_MANAGER
        self.send_inputs_from_doors_connection_form.connect(self.DATA_MANAGER.receive_inputs_from_doors_connection_form)

        self.all_modules = all_modules

        self.settigs = DATA_MANAGER.MAIN.app_settings
        self.app_path = self.settigs.doors_app_path
        self.database_path = self.settigs.doors_database_path
        self.user_name = self.settigs.doors_user_name

        COLOR = '#8888c8'
        self.ICON_PASSWORD_HIDDEN = qta.icon('fa5s.eye-slash', color=COLOR)
        self.ICON_PASSWORD_VISIBLE = qta.icon('fa5s.eye', color=COLOR)
        self._generate_layout()

        self.show()  

        self.uiLineEditPassword.setFocus()
        self.uiBtnOK.setShortcut("Return")





    def _show_password(self):
        if self.uiLineEditPassword.echoMode() == QLineEdit.Normal:
            self.uiLineEditPassword.setEchoMode(QLineEdit.Password)
            self.action_show_password.setIcon(self.ICON_PASSWORD_HIDDEN)
        else:
            self.uiLineEditPassword.setEchoMode(QLineEdit.Normal)
            self.action_show_password.setIcon(self.ICON_PASSWORD_VISIBLE)

    def _ok_clicked(self):
        success = validate_line_edits(self.uiLineEditUser, self.uiLineEditPassword, self.uiLineEditApplicationPath, invalid_chars=())
        self._update_settings()
        
        if success:
            self.send_inputs_from_doors_connection_form.emit(
                self.all_modules, 
                self.uiLineEditApplicationPath.text(),
                self.uiComboDatabase.currentText(), 
                self.uiLineEditUser.text(), 
                self.uiLineEditPassword.text())
            self.close()


    def _update_settings(self):
        self.settigs.doors_app_path = self.uiLineEditApplicationPath.text()
        self.settigs.doors_database_path = self.uiComboDatabase.currentText()
        self.settigs.doors_user_name = self.uiLineEditUser.text()
        self.settigs._fill_line_edits_with_data()




    def _generate_layout(self):
        self.uiMainLayout_3.setSpacing(10)

        self.uiLineEditApplicationPath = layout_generate_one_row("Path:", self.uiMainLayout_3)
        self.uiLineEditApplicationPath.setText(self.app_path)

        uiLayoutDatabase = QHBoxLayout()
        self.uiComboDatabase = QComboBox()
        self.uiComboDatabase.addItems(["36677@skobde-doors9db.ad.trw.com", "36677@ssh2cn-doors9db.ad.trw.com"])
        self.uiComboDatabase.setCurrentText(self.database_path)
        self.uiComboDatabase.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        uiLabelDatabase = QLabel("Database:")
        uiLabelDatabase.setMinimumWidth(75)
        uiLayoutDatabase.addWidget(uiLabelDatabase)
        uiLayoutDatabase.addWidget(self.uiComboDatabase)
        self.uiMainLayout_3.addLayout(uiLayoutDatabase)

        self.uiLineEditUser = layout_generate_one_row("User:", self.uiMainLayout_3)
        self.uiLineEditUser.setText(self.user_name)

        uiLayoutPassword = QHBoxLayout()
        # self.uiLineEditPassword = QLineEdit()
        # uiLayoutPassword.addWidget(QLabel("Password:"))
        # uiLayoutPassword.addWidget(self.uiLineEditPassword)
        self.uiLineEditPassword = layout_generate_one_row("Password:", uiLayoutPassword)
        self.uiLineEditPassword.setEchoMode(QLineEdit.Password)
        self.uiLineEditPassword.setPlaceholderText("Enter password")

        self.action_show_password = self.uiLineEditPassword.addAction(self.ICON_PASSWORD_HIDDEN, QLineEdit.TrailingPosition)
        # self.action_show_password.setIcon(self.ICON_PASSWORD_HIDDEN)
        self.action_show_password.triggered.connect(self._show_password)
        for widget in self.uiLineEditPassword.findChildren(QToolButton):
            widget.setCursor(Qt.PointingHandCursor)

        self.uiMainLayout_3.addLayout(uiLayoutPassword)

