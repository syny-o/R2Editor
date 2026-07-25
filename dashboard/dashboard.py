from pathlib import Path

from PyQt5.QtWidgets import (
    QFileDialog,
    QHeaderView,
    QInputDialog,
    QMessageBox,
    QToolButton,
    QTreeWidgetItem,
    QWidget,
)
from PyQt5.QtCore import QSize, Qt, pyqtSignal, QTimer

from config.icon_manager import IconManager
from dashboard.recent_projects import project_last_modified_text
from ui.dashboard_ui import Ui_Form
from dialogs.dialog_message import dialog_message
from components.widgets.widgets_pointing_hand import TreeWidgetPointingHand


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

        self.uiListWidgetRecentProjects = TreeWidgetPointingHand()
        self.uiListWidgetRecentProjects.setObjectName(
            "uiTreeRecentProjects"
        )
        self.uiListWidgetRecentProjects.setColumnCount(3)
        self.uiListWidgetRecentProjects.setHeaderLabels(
            ["Project", "Last modified", ""]
        )
        self.uiListWidgetRecentProjects.setRootIsDecorated(False)
        self.uiListWidgetRecentProjects.setAlternatingRowColors(True)
        self.uiListWidgetRecentProjects.header().setSectionResizeMode(
            0,
            QHeaderView.Stretch,
        )
        self.uiListWidgetRecentProjects.header().setSectionResizeMode(
            1,
            QHeaderView.ResizeToContents,
        )
        self.uiListWidgetRecentProjects.header().setSectionResizeMode(
            2,
            QHeaderView.Fixed,
        )
        self.uiListWidgetRecentProjects.header().setStretchLastSection(False)
        self.uiListWidgetRecentProjects.setColumnWidth(2, 34)
        self.uiLayoutRecentProjects.addWidget(self.uiListWidgetRecentProjects)
        self.uiListWidgetRecentProjects.itemClicked.connect(self.open_project)
        # self.settings = {}
        # self.settings = QSettings(r'.\app-config.ini', QSettings.IniFormat)
        # self.recent_projects = self.settings.value('RECENT_PROJECTS')


        if self.recent_projects: 
            self.populate_list_widget()

        self.ui_btn_remove.setVisible(False)
        self.ui_btn_new_project.clicked.connect(self.new_project)
        self.ui_btn_open_project.clicked.connect(self.open_from_disk)
        self.ui_btn_configuration.clicked.connect(lambda: self.main_window.manage_right_menu(self.main_window.app_settings, self.main_window.btn_app_settings))
        self.ui_btn_editor.clicked.connect(lambda: self.main_window.manage_right_menu(self.main_window.tabs_splitter, self.main_window.ui_btn_text_editor))


    def populate_list_widget(self):
        if self.recent_projects:
            self.uiListWidgetRecentProjects.clear()
            for project_path in self.recent_projects:
                item = QTreeWidgetItem(
                    [
                        str(project_path),
                        project_last_modified_text(project_path),
                    ]
                )
                item.setData(0, Qt.UserRole, project_path)
                self.uiListWidgetRecentProjects.addTopLevelItem(item)
                self.uiListWidgetRecentProjects.setItemWidget(
                    item,
                    2,
                    self._create_remove_button(item),
                )

            self.uiListWidgetRecentProjects.clearSelection()
            self.uiListWidgetRecentProjects.setCurrentItem(None)
            self.uiListWidgetRecentProjects.setFocus()
            


    # @INTERFACE TO PROJECT MANAGER
    def receive_parameters_from_project_manager(self, parameters: dict):
        # print(parameters.get("recent_projects"))
        self.populate_list_widget()


    def new_project(self):
        self.main_window.project_actions.new()
        self.main_window.manage_right_menu(self.main_window.data_manager, self.main_window.ui_btn_data_manager)




    def open_project(self):
        if not self.PROJECT_MANAGER.is_project_saved():
            proceed = QMessageBox.question(self,
                            "R2ScriptEditor",
                            "Current project is not saved.\n\nDo you want to proceed (all changes will be lost)?",
                            QMessageBox.Yes | QMessageBox.No)
            if proceed == QMessageBox.No:
                return         
        project_path = Path(
            self.uiListWidgetRecentProjects.currentItem().data(
                0,
                Qt.UserRole,
            )
        )
        project_name = project_path.name
        
        self.main_window.show_notification(f"Loading {project_name}...")  
        QTimer.singleShot(500, lambda: self.trigger_opening_project())
             

        


    def trigger_opening_project(self):       
        project_path = self.uiListWidgetRecentProjects.currentItem().data(
            0,
            Qt.UserRole
        )
        success, message = self.PROJECT_MANAGER.open_project(project_path)
        if not success:
            dialog_message(self, f"Failed to Open Project!\n{message}")
        self.main_window.manage_right_menu(self.main_window.data_manager, self.main_window.ui_btn_data_manager)        

    def _create_remove_button(self, item):
        button = QToolButton()
        button.setAutoRaise(True)
        button.setCursor(Qt.PointingHandCursor)
        button.setIcon(
            self.main_window.ICON_MANAGER.ICON_REMOVE_RECENT_PROJECT
        )
        button.setIconSize(QSize(20, 20))
        button.setToolTip("Remove from recent projects")
        button.setAccessibleName("Remove from recent projects")
        button.clicked.connect(
            lambda checked=False: self._remove_recent_project(item)
        )
        return button

    def _remove_recent_project(self, item):
        current_row = self.uiListWidgetRecentProjects.indexOfTopLevelItem(
            item
        )
        if current_row == -1:
            return

        project_path = item.data(
            0,
            Qt.UserRole
        )
        self.recent_projects.remove(project_path)
        self.uiListWidgetRecentProjects.takeTopLevelItem(current_row)
        self.main_window.app_settings.settings.setValue('RECENT_PROJECTS', self.recent_projects)
        
        if len(self.recent_projects) == 0:
            self.ui_btn_ok.setEnabled(False)


    def open_from_disk(self):
        self.main_window.project_actions.open()
