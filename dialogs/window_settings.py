from PyQt5.QtWidgets import QWidget, QLineEdit
from PyQt5.QtCore import Qt, pyqtSignal, QSettings


from ui.app_settings_ui import Ui_Form

class AppSettings(QWidget, Ui_Form):
    """
    This "window" will appear after Settings
    """
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)

        self.frame_25.setVisible(False) # HIDE WHOLE PASSWD FRAME

        # OPEN CONFIG FILE INI:
        self.settings = QSettings(r'.\app_config.ini', QSettings.IniFormat)


        # LOAD ALL DATA and SET to INSTANCE VARIABLES
        # 1. Doors
        self.doors_app_path = self.settings.value('doors/doors_app_path', r'C:\app\tools\IBM\DOORS\9.6_64\bin\doors.exe')
        self.doors_database_path = self.settings.value('doors/doors_database_path')
        self.doors_user_name = self.settings.value('doors/doors_user_name')
        
        # 2. Text Editor
        self.format_code_when_save = bool(self.settings.value('editor/format_code_when_save', True))

        # 3. Recent Projects
        self.recent_projects = self.settings.value('project/recent')
        
        # 4. Print All Data --> CHECK IF OK
        print(self.doors_app_path)
        print(self.doors_database_path)
        print(self.doors_user_name)
        print(self.format_code_when_save)
        print(self.recent_projects)

        # 5. Display loaded data to GUI components
        self.fill_line_edits_with_saved_settings()

        # Connect Save Button with SAVE SLOT 
        self.btn_save.clicked.connect(self.save_settings)
        self.ui_checkBox_format_code_when_save.stateChanged.connect(self.get_data_from_form)


    def fill_line_edits_with_saved_settings(self):
        # DOORS
        self.le_app_path.setText(self.doors_app_path)
        self.ui_cb_database.setCurrentText(self.doors_database_path)
        self.le_user.setText(self.doors_user_name)

        # TEXT EDITOR
        self.ui_checkBox_format_code_when_save.setChecked(self.format_code_when_save)


    def get_data_from_form(self):
        """
        METHOD for reading texts from all line_edits
        :return: values from line edits
        """
        # DOORS
        self.doors_app_path = self.le_app_path.text()
        self.doors_database_path = self.ui_cb_database.currentText()
        self.doors_user_name = self.le_user.text()

        # TEXT EDITOR
        self.format_code_when_save = self.ui_checkBox_format_code_when_save.isChecked()




    def save_settings(self):
        """ METHOD is triggered after pressing Apply/OK --> settings are saved to disk """
        self.get_data_from_form()

        self.settings.beginGroup("project")
        self.settings.setValue('recent', self.recent_projects)
        self.settings.endGroup()
        
        self.settings.beginGroup("editor")
        self.settings.setValue('format_code_when_save', self.format_code_when_save)
        self.settings.endGroup()
        self.settings.beginGroup("doors")
        self.settings.setValue('doors_app_path', self.doors_app_path)
        self.settings.setValue('doors_database_path', self.doors_database_path)
        self.settings.setValue('doors_user_name', self.doors_user_name)
        self.settings.endGroup()










