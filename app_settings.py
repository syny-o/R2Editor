from PyQt5.QtWidgets import QWidget, QLineEdit
from PyQt5.QtCore import Qt, pyqtSignal, QSettings

from ui.app_settings_ui import Ui_Form


class AppSettings(QWidget, Ui_Form):

    def __init__(self, MAIN):
        super().__init__()
        self.setupUi(self)

        # HIDE WHOLE PASSWD FRAME
        self.frame_25.setVisible(False) 

        # CREATE LIST OF ALL LINEDITS --> THEN THEY WILL BE CONNECTED TO SLOT
        UI_LINEEDITS_INPUTS = [
            self.le_app_path,
            self.le_user,
        ]

        UI_COMBOBOX_INPUTS = [
            self.ui_cb_database,
            self.uiComboTheme,
        ]
         

        self._load_data_from_disk()
        self._fill_line_edits_with_data()

        # Connect Save Button with SAVE SLOT 
        self.ui_checkBox_format_code_when_save.stateChanged.connect(self._save_data_from_form_2_memory)

        for line_edit_input in UI_LINEEDITS_INPUTS:
            line_edit_input.editingFinished.connect(self._save_data_from_form_2_memory)

        for combo_box_input in UI_COMBOBOX_INPUTS:
            combo_box_input.currentTextChanged.connect(self._save_data_from_form_2_memory)           

        self.uiComboTheme.currentTextChanged.connect(MAIN.change_theme)




    def _load_data_from_disk(self):
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

        # 4. Appearance
        self.theme = self.settings.value('appearance/theme', 'Light')    




    def _fill_line_edits_with_data(self):
        # DOORS
        self.le_app_path.setText(self.doors_app_path)
        self.ui_cb_database.setCurrentText(self.doors_database_path)
        self.le_user.setText(self.doors_user_name)

        # TEXT EDITOR
        self.ui_checkBox_format_code_when_save.setChecked(self.format_code_when_save)

        # THEME
        self.uiComboTheme.setCurrentText(self.theme)



    def _save_data_from_form_2_memory(self):
        """
        METHOD for reading texts from all line_edits
        """
        # DOORS
        self.doors_app_path = self.le_app_path.text()
        self.doors_database_path = self.ui_cb_database.currentText()
        self.doors_user_name = self.le_user.text()

        # TEXT EDITOR
        self.format_code_when_save = self.ui_checkBox_format_code_when_save.isChecked()

        # THEME
        self.theme = self.uiComboTheme.currentText()




    def save_settings_2_disk(self):
        """ METHOD is triggered after pressing Apply/OK --> settings are saved to MEMORY """

        self.settings.beginGroup("project")
        self.settings.setValue('recent', self.recent_projects)
        self.settings.endGroup()

        self.settings.beginGroup("appearance")
        self.settings.setValue('theme', self.theme)
        self.settings.endGroup()        
        
        self.settings.beginGroup("editor")
        self.settings.setValue('format_code_when_save', self.format_code_when_save)
        self.settings.endGroup()
        self.settings.beginGroup("doors")
        self.settings.setValue('doors_app_path', self.doors_app_path)
        self.settings.setValue('doors_database_path', self.doors_database_path)
        self.settings.setValue('doors_user_name', self.doors_user_name)
        self.settings.endGroup()


