from PyQt5.QtWidgets import QWidget, QFileDialog, QListWidget, QInputDialog, QListWidgetItem
from PyQt5.QtCore import Qt, pyqtSignal, QSettings
from PyQt5.QtGui import QIcon
from ui.ui_form_recent_projects import Ui_Form




class RecentProjects(QWidget, Ui_Form):
    """
    This "window" will appear after NEW PROJECT or EDIT PROJECT CONFIGURATION
    """
    # SIGNAL DEFINITION
    send_project_data = pyqtSignal(object)

    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.main_window = main_window


        # self.settings = {}
        self.settings = QSettings(r'.\config\configuration.ini', QSettings.IniFormat)
        self.recent_projects = self.settings.value('RECENT_PROJECTS')

        if self.recent_projects: 
            self.ui_btn_remove.setEnabled(True)
            self.ui_btn_ok.setEnabled(True)
        self.ui_btn_remove.clicked.connect(self.remove_project)
        self.ui_btn_close.clicked.connect(self.close)
        self.ui_btn_ok.clicked.connect(self.open_project)
        self.ui_btn_open.clicked.connect(self.open_from_disk)
        self.ui_lw_projects.itemDoubleClicked.connect(self.open_project)


        if self.recent_projects:
            for item in self.recent_projects:
                item = QListWidgetItem(QIcon(u"ui/icons/open-folder.png"), item)
                self.ui_lw_projects.addItem(item)

                self.ui_lw_projects.setCurrentRow(0)


    def open_project(self):
        project_path = self.ui_lw_projects.currentItem().data(Qt.DisplayRole)
        self.main_window.open_project.emit(project_path)
        self.close()

    def remove_project(self):
        project_path = self.ui_lw_projects.currentItem().data(Qt.DisplayRole)
        self.recent_projects.remove(project_path)
        self.ui_lw_projects.takeItem(self.ui_lw_projects.currentRow())
        self.settings.setValue('RECENT_PROJECTS', self.recent_projects)
        
        if len(self.recent_projects) == 0:
            self.ui_btn_remove.setEnabled(False)
            self.ui_btn_ok.setEnabled(False)


    def open_from_disk(self):
        self.main_window.project_open()
        self.close()
        