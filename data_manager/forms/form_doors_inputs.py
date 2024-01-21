from PyQt5.QtWidgets import QWidget, QPushButton, QToolBar, QVBoxLayout, QLabel, QListWidget, QLineEdit, QComboBox, QHBoxLayout, QInputDialog, QListWidgetItem
from PyQt5.QtCore import Qt, pyqtSignal, QSettings
from PyQt5.QtGui import QFont, QPalette, QIcon

from ui.form_general_ui import Ui_Form

from components.helper_functions import validate_line_edits





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
        
        # self.setStyleSheet(style)
        self.uiLabelTitle.setStyleSheet("")

        self.uiBtnTitleBarClose.clicked.connect(self.close)
        self.uiBtnStatusBarClose.clicked.connect(self.close)
        self.uiBtnOK.clicked.connect(self._ok_clicked)
        
        self.DATA_MANAGER = DATA_MANAGER
        self.send_inputs_from_doors_connection_form.connect(self.DATA_MANAGER.receive_inputs_from_doors_connection_form)

        self.all_modules = all_modules

        self.settings = QSettings(r'.\app_config.ini', QSettings.IniFormat)
        self.app_path = self.settings.value('doors/doors_app_path')
        self.database_path = self.settings.value('doors/doors_database_path')
        self.user_name = self.settings.value('doors/doors_user_name')        

        self._generate_layout()

        self.show()  



    def _show_password(self):
        if self.uiBtnShowPassword.isChecked():
            self.uiLineEditPassword.setEchoMode(QLineEdit.Password)
        else:
            self.uiLineEditPassword.setEchoMode(QLineEdit.Normal)

    def _ok_clicked(self):
        success = validate_line_edits(self.uiLineEditUser, self.uiLineEditPassword, self.uiLineEditApplicationPath, invalid_chars=())
        if success:
            self.send_inputs_from_doors_connection_form.emit(
                self.all_modules, 
                self.uiLineEditApplicationPath.text(),
                self.uiComboDatabase.currentText(), 
                self.uiLineEditUser.text(), 
                self.uiLineEditPassword.text())
            self.close()




    def _generate_layout(self):
        self.uiMainLayout_2.setSpacing(10)

        uiLayoutApplicationPath = QHBoxLayout()
        self.uiLineEditApplicationPath = QLineEdit()
        self.uiLineEditApplicationPath.setText(self.app_path)
        uiLayoutApplicationPath.addWidget(QLabel("Path:"))
        uiLayoutApplicationPath.addWidget(self.uiLineEditApplicationPath)        

        uiLayoutDatabase = QHBoxLayout()
        self.uiComboDatabase = QComboBox()
        self.uiComboDatabase.addItems(["36677@skobde-doors9db.ad.trw.com", "36677@ssh2cn-doors9db.ad.trw.com"])
        self.uiComboDatabase.setCurrentText(self.database_path)
        self.uiComboDatabase.setMinimumWidth(450)
        uiLayoutDatabase.addWidget(QLabel("Database:"))
        uiLayoutDatabase.addWidget(self.uiComboDatabase)

        uiLayoutUser = QHBoxLayout()
        self.uiLineEditUser = QLineEdit()
        self.uiLineEditUser.setText(self.user_name)
        uiLayoutUser.addWidget(QLabel("User:"))
        uiLayoutUser.addWidget(self.uiLineEditUser)

        uiLayoutPassword = QHBoxLayout()
        self.uiLineEditPassword = QLineEdit()
        uiLayoutPassword.addWidget(QLabel("Password:"))
        uiLayoutPassword.addWidget(self.uiLineEditPassword)
        self.uiLineEditPassword.setEchoMode(QLineEdit.Password)
        self.uiLineEditPassword.setPlaceholderText("Enter password")
        self.uiBtnShowPassword = QPushButton(QIcon(u"ui/icons/16x16/cil-low-vision"), "")
        self.uiBtnShowPassword.setCheckable(True)
        self.uiBtnShowPassword.clicked.connect(self._show_password)
        self.uiBtnShowPassword.setMaximumWidth(30)
        self.uiBtnShowPassword.setChecked(True)
        self.uiBtnShowPassword.setToolTip("Show password")
        self.uiBtnShowPassword.setCursor(Qt.PointingHandCursor)
        uiLayoutPassword.addWidget(self.uiBtnShowPassword)

        self.uiMainLayout_2.addLayout(uiLayoutApplicationPath)
        self.uiMainLayout_2.addLayout(uiLayoutDatabase)
        self.uiMainLayout_2.addLayout(uiLayoutUser)
        self.uiMainLayout_2.addLayout(uiLayoutPassword)


