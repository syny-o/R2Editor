import sys, pywinstyles
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow
from app_settings import AppSettings
from application_lifecycle import ApplicationLifecycle
from config.settings_controller import SettingsController
from data_manager.projects import manager as project_manager
from data_manager.projects.actions import ProjectActions
from main_window_builder import MainWindowBuilder
from text_editor.documents.document_actions import DocumentActions
from text_editor.editor_controller import EditorController
from ui.main_ui import Ui_MainWindow
from window_controller import WindowController
from config.icon_manager import IconManager


# pyinstaller -w --icon=R2Editor.ico --name=R2Editor main.py

class MainWindow(QMainWindow, Ui_MainWindow):
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
            lambda: self.manage_right_menu(
                self.data_manager,
                self.ui_btn_data_manager,
            ),
        )
        self.project_actions.connect_actions()
        self.document_actions = DocumentActions(self)
        
        # APP SETTINGS CONFIGURATION
        self.app_settings = AppSettings(self)
        self.editor_controller = EditorController(self)
        self.editor_controller.connect_actions(self.document_actions)
        
        # GLOBAL TIMERS START
        self.timer_project_autosave = QTimer()  # initialize timer - one global timer (even if it is not used - when value is Off)
        self.timer_project_autosave.timeout.connect(self.project_actions.autosave)
        self.settings_controller = SettingsController(self)
        self.settings_controller.apply()

        self.resize(1920, 1080)
        self.setWindowIcon(self.ICON_MANAGER.application_icon())
        self.setWindowTitle("Editor")
        self.frame_top.setVisible(False)
          
        self.uiFrameFileManager.setVisible(False)
        self.frame_2.setVisible(False)
        self.window_controller.connect_window_actions()

        self.VERSION = '2026-07-24'
        
        # POINTER TO ACTUAL TEXTEDIT, ACTUAL TABS
        self._actual_text_edit = None
        self.actual_tabs = None 
        self.window_builder = MainWindowBuilder(self, project_manager)
        self.window_builder.build()

        self.update_actual_information()



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


    # UPDATES:  START
    def receive_parameters_from_project_manager(self, parameters: dict):
        self.window_controller.update_project_title(parameters)
        

    def update_actual_information(self):
        self.window_controller.update_editor_state()
   
    
    def show_notification(self, notification_text):
        self.window_controller.show_notification(notification_text)


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

