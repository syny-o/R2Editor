import sys
import pywinstyles

from PyQt5.QtCore import Qt, QTimer, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplitter, QVBoxLayout, QLabel, QFrame

from app_settings import AppSettings
from application_lifecycle import ApplicationLifecycle
from components.notification_widget import NotificationWidget
from config.settings_controller import SettingsController
from dashboard.dashboard import Dashboard
from data_manager import project_manager
from data_manager.data_manager import DataManager
from data_manager.project_actions import ProjectActions
from file_browser.tree_file_browser import FileSystemView
from text_editor.document_actions import DocumentActions
from text_editor.editor_controller import EditorController
from text_editor.outline_controller import OutlineController
from text_editor.tab_manager import EditorTabManager
from text_editor.tabs import Tabs
from ui.main_ui import Ui_MainWindow
from window_controller import WindowController
from config.icon_manager import IconManager
from components.widgets.widgets_pointing_hand import TreeWidgetPointingHand


# pyinstaller -w --icon=R2Editor.ico --name=R2Editor main.py


class MainWindow(QMainWindow, Ui_MainWindow):

    open_project = pyqtSignal(str)
    save_project = pyqtSignal(str)
    script_requirement_reference_changed = pyqtSignal(set, str)

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.window_controller = WindowController(self)
        self.application_lifecycle = ApplicationLifecycle(
            self,
            project_manager,
        )
        self.ICON_MANAGER = IconManager()
        self.window_controller.configure_icons(self.ICON_MANAGER)
        self.project_actions = ProjectActions(
            self,
            project_manager,
            self.show_notification,
        )
        self.document_actions = DocumentActions(self)
        

        ################################################################################################################
        # APP SETTINGS CONFIGURATION
        ################################################################################################################
        self.app_settings = AppSettings(self)
        self.editor_controller = EditorController(self)
        self.editor_controller.connect_actions(self.document_actions)

        
        ################################################################################################################
        # GLOBAL TIMERS START
        ################################################################################################################

        self.timer_project_autosave = QTimer()  # initialize timer - one global timer (even if it is not used - when value is Off)
        self.timer_project_autosave.timeout.connect(self.project_actions.autosave)
        self.settings_controller = SettingsController(self)
        self.settings_controller.apply()


        ################################################################################################################
        # GLOBAL TIMERS END
        ################################################################################################################


        self.resize(1920, 1080)

        self.setWindowIcon(QIcon('R2Editor.ico'))
        self.setWindowTitle("Editor")
        self.frame_top.setVisible(False)
          
        ## CONNECT BUTTONS        
        self.btn_app_exit.clicked.connect(self.close)

        self.btn_project_open.clicked.connect(self.project_actions.open)
        self.btn_project_new.clicked.connect(self.project_actions.new)
        self.btn_project_save.clicked.connect(self.project_actions.save)
        self.btn_project_save_as.clicked.connect(self.project_actions.save_as)

        self.uiFrameFileManager.setVisible(False)
        self.frame_2.setVisible(False)
        ## TOGGLE/BURGUER MENU
        ########################################################################
        self.btn_toggle_menu.clicked.connect(
            lambda: self.window_controller.toggle_menu(
                self.uiFrameLeftMenu,
                70,
                210,
            )
        )
        self.btn_close.clicked.connect(self.close)

        self.VERSION = '2021-03-04'
        ################################################################################################################
        # POINTER TO ACTUAL TEXTEDIT, ACTUAL TABS
        ################################################################################################################
        self._actual_text_edit = None
        self.actual_tabs = None 

        ################################################################################################################
        # TREE FILE BROWSER CONFIGURATION
        ################################################################################################################
        uiLeftPanelSplitter = QSplitter()
        uiLeftPanelSplitter.setOrientation(Qt.Vertical)
        self.uiLayoutFileManager.addWidget(uiLeftPanelSplitter)
        self.tree_file_browser = FileSystemView(self, project_manager)
        uiLeftPanelSplitter.addWidget(self.tree_file_browser)

        ################################################################################################################
        # TREE OUTLINE CONFIGURATION
        ################################################################################################################
        
        uiLayoutOutline = QVBoxLayout()
        uiLayoutOutline.setContentsMargins(0, 0, 0, 0)
        uiLayoutOutline.addWidget(QLabel("Outline"), alignment=Qt.AlignCenter)
        self.uiTreeOutline = TreeWidgetPointingHand()
        uiLayoutOutline.addWidget(self.uiTreeOutline)
        self.uiTreeOutline.setHeaderHidden(True)
        self.outline_controller = OutlineController(self, self.uiTreeOutline)
        self.uiTreeOutline.itemClicked.connect(
            self.outline_controller.click_item
        )
        self.timer_4_updating_outline = QTimer()
        self.timer_4_updating_outline.timeout.connect(
            self.outline_controller.update
        )
        self.timer_4_updating_outline.start(500)
        uiFrameOutline = QFrame()
        uiFrameOutline.setObjectName("objNameFrameOutline")
        uiFrameOutline.setLayout(uiLayoutOutline)
        uiLeftPanelSplitter.addWidget(uiFrameOutline)

        ################################################################################################################
        # DATA MANAGER CONFIGURATION
        ################################################################################################################
        self.data_manager = DataManager(self, project_manager)
        self.script_requirement_reference_changed.connect(self.data_manager.script_requirement_reference_changed)

        ################################################################################################################
        # DASHBOARD CONFIGURATION
        ################################################################################################################
        self.dashboard = Dashboard(self, project_manager)

        ################################################################################################################
        # CONNECT PROJECT MANAGER WITH PROJECT LISTENERS
        ################################################################################################################        
        project_manager.set_listeners(self, self.dashboard, self.data_manager, self.tree_file_browser)

        ################################################################################################################
        # TABS CONFIGURATION
        ################################################################################################################
        self.left_tabs = Tabs(self, True, 'LEFT_TABS')
        self.left_tabs.currentChanged.connect(
            self.editor_controller.update_find_replace
        )

        self.right_tabs = Tabs(self, False, 'RIGHT_TABS')
        self.right_tabs.currentChanged.connect(
            self.editor_controller.update_find_replace
        )

        self.tab_manager = EditorTabManager(
            self,
            self.left_tabs,
            self.right_tabs,
        )
        self.tab_manager.connect_signals()

        self.tabs_splitter = QSplitter()
        self.tabs_splitter.addWidget(self.left_tabs)
        self.tabs_splitter.addWidget(self.right_tabs)
        self.tabs_splitter.setStretchFactor(2, 1)

        ################################################################################################################
        # STACKEDWIDGET CONFIGURATION
        ################################################################################################################
        
        self.stackedWidget.addWidget(self.tabs_splitter)
        self.stackedWidget.addWidget(self.data_manager)
        self.stackedWidget.addWidget(self.app_settings)
        self.stackedWidget.addWidget(self.dashboard)
        self.stackedWidget.setCurrentWidget(self.dashboard)

        self.ui_btn_text_editor.clicked.connect(
            lambda: self.manage_right_menu(
                self.tabs_splitter,
                self.ui_btn_text_editor,
            )
        )
        self.ui_btn_data_manager.clicked.connect(
            lambda: self.manage_right_menu(
                self.data_manager,
                self.ui_btn_data_manager,
            )
        )
        self.ui_btn_home.clicked.connect(
            lambda: self.manage_right_menu(
                self.dashboard,
                self.ui_btn_home,
            )
        )
        self.btn_app_settings.clicked.connect(
            lambda: self.manage_right_menu(
                self.app_settings,
                self.btn_app_settings,
            )
        )

        ################################################################################################################
        # NOTIFICATION WIDGET CONFIGURATION
        ################################################################################################################
        self.notification_widget = NotificationWidget(self)

        self.update_actual_information()



    ################################################################################################################
    # SETTINGS WAS UPDATED START
    ################################################################################################################

    @pyqtSlot()
    def settings_was_updated(self):
        self.settings_controller.apply()




    @property
    def actual_text_edit(self):
        return self._actual_text_edit


    @actual_text_edit.setter
    def actual_text_edit(self, text_edit):
        self._actual_text_edit = text_edit
     


    def keyPressEvent(self, e) -> None:
        if e.key() == Qt.Key_Escape:
            self.editor_controller.close_find_replace()
        return super().keyPressEvent(e)



    def manage_right_menu(self, widget, button):
        self.window_controller.show_page(widget, button)




########################################################################################################################
# UPDATES:  START
########################################################################################################################
    def receive_parameters_from_project_manager(self, parameters: dict):
        self.window_controller.update_project_title(parameters)
        

    def update_actual_information(self):
        self.window_controller.update_editor_state()
   
    
    def show_notification(self, notification_text):
        self.window_controller.show_notification(notification_text)



########################################################################################################################
# UPDATES:  END
########################################################################################################################

    # SAVE WINDOW SIZE, POSITION BEFORE CLOSE APP AND CHECK IF ALL SCRIPTS ARE SAVED
    def closeEvent(self, event):
        self.application_lifecycle.close(event)





if __name__ == "__main__":
    app = QApplication([])    
    app.setStyle('Fusion')        
    window = MainWindow()
    pywinstyles.apply_style(window,"dark")
    window.show()    
    sys.exit(app.exec_())

