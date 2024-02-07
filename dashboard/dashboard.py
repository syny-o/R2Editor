from pathlib import Path

from PyQt5.QtWidgets import QWidget, QFileDialog, QListWidget, QInputDialog, QListWidgetItem, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon

from ui.dashboard_ui import Ui_Form
from dialogs.dialog_message import dialog_message
from components.widgets.widgets_pointing_hand import ListWidgetPointingHand


class Dashboard(QWidget, Ui_Form):
    """
    Dashboard
    """
    # SIGNAL DEFINITION
    send_project_data = pyqtSignal(object)

    def __init__(self, main_window, project_manager):
        super().__init__()
        self.setupUi(self)

        self.main_window = main_window
        self.PROJECT_MANAGER = project_manager

        self.recent_projects = main_window.app_settings.recent_projects

        self.uiListWidgetRecentProjects = ListWidgetPointingHand()
        self.uiLayoutRecentProjects.addWidget(self.uiListWidgetRecentProjects)
        self.uiListWidgetRecentProjects.itemClicked.connect(self.open_project)

        # self.settings = {}
        # self.settings = QSettings(r'.\app-config.ini', QSettings.IniFormat)
        # self.recent_projects = self.settings.value('RECENT_PROJECTS')


        if self.recent_projects: 
            self.ui_btn_remove.setEnabled(True)
            self.populate_list_widget()

        self.ui_btn_remove.clicked.connect(self.remove_project)
        self.ui_btn_remove.setShortcut("Del")
        self.ui_btn_new_project.clicked.connect(self.new_project)
        self.ui_btn_open_project.clicked.connect(self.open_from_disk)
        self.ui_btn_configuration.clicked.connect(lambda: self.main_window.manage_right_menu(self.main_window.app_settings, self.main_window.btn_app_settings))
        self.ui_btn_editor.clicked.connect(lambda: self.main_window.manage_right_menu(self.main_window.tabs_splitter, self.main_window.ui_btn_text_editor))


    def populate_list_widget(self):
        if self.recent_projects:
            self.uiListWidgetRecentProjects.clear()
            for item in self.recent_projects:
                item = QListWidgetItem(QIcon(u"ui/icons/16x16/cil-av-timer.png"), item)
                self.uiListWidgetRecentProjects.addItem(item)

            self.uiListWidgetRecentProjects.setCurrentRow(0)
            self.uiListWidgetRecentProjects.setFocus()
            


    # @INTERFACE TO PROJECT MANAGER
    def receive_parameters_from_project_manager(self, parameters: dict):
        # print(parameters.get("recent_projects"))
        self.populate_list_widget()


    def new_project(self):
        self.main_window.project_new()
        self.main_window.manage_right_menu(self.main_window.data_manager, self.main_window.ui_btn_data_manager)




    def open_project(self):
        if not self.PROJECT_MANAGER.is_project_saved():
            proceed = QMessageBox.question(self,
                            "R2ScriptEditor",
                            "Current project is not saved.\n\nDo you want to proceed (all changes will be lost)?",
                            QMessageBox.Yes | QMessageBox.No)
            if proceed == QMessageBox.No:
                return         
        project_path = Path(self.uiListWidgetRecentProjects.currentItem().data(Qt.DisplayRole))
        project_name = project_path.name
        
        self.main_window.show_notification(f"Loading {project_name}...")  
        QTimer.singleShot(500, lambda: self.trigger_opening_project())
             

        


    def trigger_opening_project(self):       
        project_path = self.uiListWidgetRecentProjects.currentItem().data(Qt.DisplayRole) 
        success, message = self.PROJECT_MANAGER.open_project(project_path)
        if not success:
            dialog_message(self, f"Failed to Open Project!\n{message}")
        self.main_window.manage_right_menu(self.main_window.data_manager, self.main_window.ui_btn_data_manager)        

    def remove_project(self):
        project_path = self.uiListWidgetRecentProjects.currentItem().data(Qt.DisplayRole)
        self.recent_projects.remove(project_path)
        self.uiListWidgetRecentProjects.takeItem(self.uiListWidgetRecentProjects.currentRow())
        self.settings.setValue('RECENT_PROJECTS', self.recent_projects)
        
        if len(self.recent_projects) == 0:
            self.ui_btn_remove.setEnabled(False)
            self.ui_btn_ok.setEnabled(False)


    def open_from_disk(self):
        self.main_window.project_open()

        