from pathlib import Path

from PyQt5.QtWidgets import QWidget, QFileDialog, QListWidget, QInputDialog, QListWidgetItem
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon
from ui.dashboard_ui import Ui_Form




class Dashboard(QWidget, Ui_Form):
    """
    Dashboard
    """
    # SIGNAL DEFINITION
    send_project_data = pyqtSignal(object)

    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)

        self.main_window = main_window

        self.recent_projects = main_window.app_settings.recent_projects


        # self.settings = {}
        # self.settings = QSettings(r'.\app-config.ini', QSettings.IniFormat)
        # self.recent_projects = self.settings.value('RECENT_PROJECTS')


        if self.recent_projects: 
            self.ui_btn_remove.setEnabled(True)

        self.ui_btn_remove.clicked.connect(self.remove_project)
        self.ui_btn_remove.setShortcut("Del")
        self.ui_btn_new_project.clicked.connect(self.main_window.project_new)
        self.ui_btn_open_project.clicked.connect(self.open_from_disk)
        self.ui_lw_projects.itemDoubleClicked.connect(self.open_project)
        self.ui_btn_configuration.clicked.connect(lambda: self.main_window.manage_right_menu(self.main_window.app_settings, self.main_window.btn_app_settings))
        self.ui_btn_editor.clicked.connect(lambda: self.main_window.manage_right_menu(self.main_window.tabs_splitter, self.main_window.ui_btn_text_editor))


        if self.recent_projects:
            for item in self.recent_projects:
                item = QListWidgetItem(QIcon(u"ui/icons/16x16/cil-av-timer.png"), item)
                self.ui_lw_projects.addItem(item)

            self.ui_lw_projects.setCurrentRow(0)
            self.ui_lw_projects.setFocus()
            


    def open_project(self):
        project_path = Path(self.ui_lw_projects.currentItem().data(Qt.DisplayRole))
        project_name = project_path.name
        
        self.main_window.show_notification(f"Loading {project_name}...")  
        QTimer.singleShot(500, lambda: self.trigger_opening_project())
             
        


    def trigger_opening_project(self):
        project_path = self.ui_lw_projects.currentItem().data(Qt.DisplayRole) 
        self.main_window.open_project.emit(project_path)
        self.main_window.manage_right_menu(self.main_window.data_manager, self.main_window.ui_btn_data_manager)        

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

        