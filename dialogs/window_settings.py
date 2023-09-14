from PyQt5.QtWidgets import QWidget, QLineEdit
from PyQt5.QtCore import Qt, pyqtSignal, QSettings


from ui.ui_app_settings import Ui_Form

class AppSettings(QWidget, Ui_Form):
    """
    This "window" will appear after Settings
    """
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)

        self.settings = {}
        self.settings_doors = QSettings(r'.\doors\doors.ini', QSettings.IniFormat)
        try:
            self.doors_app_path = self.settings_doors.value('doors_app_path')
            self.doors_database_path = self.settings_doors.value('doors_database_path')
            self.doors_user_name = self.settings_doors.value('doors_user_name')
            # self.doors_user_passwd = self.settings_doors.value('doors_user_passwd')
        except:
            self.doors_app_path = None
            self.doors_database_path = None
            self.doors_user_name = None
            self.doors_user_passwd = None

        # self.le_passwd.setEchoMode(QLineEdit.Password)
        self.frame_25.setVisible(False) # HIDE WHOLE PASSWD FRAME


        self.fill_line_edits_with_saved_settings()
        self.le_app_path.setText(r'C:\app\tools\IBM\DOORS\9.6_64\bin\doors.exe')
        # self.le_database_path.setText(r'36677@skobde-doors9db.ad.trw.com')

        self.btn_save.clicked.connect(self.save_settings)


    def fill_line_edits_with_saved_settings(self):
        self.le_app_path.setText(self.doors_app_path)
        self.ui_cb_database.setCurrentText(self.doors_database_path)
        self.le_user.setText(self.doors_user_name)
        # self.le_passwd.setText(self.doors_user_passwd)



    def get_data_from_form(self):
        """
        METHOD for reading texts from all line_edits
        :return: values from line edits
        """
        app_path = self.le_app_path.text()
        database_path = self.ui_cb_database.currentText()
        user_name = self.le_user.text()
        # user_passwd = self.le_passwd.text()

        return [app_path, database_path, user_name]

    def save_settings(self):
        """ METHOD is triggered after pressing Apply/OK --> settings are saved to disk """
        data = self.get_data_from_form()

        for i in range(len(data)):
            data[i] = None if data[i] == '' else data[i]

        self.settings_doors.setValue('doors_app_path', data[0])
        self.settings_doors.setValue('doors_database_path', data[1])
        self.settings_doors.setValue('doors_user_name', data[2])
        # self.settings_doors.setValue('doors_user_passwd', data[3])








