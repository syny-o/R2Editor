import re
import sys
import pywinstyles

from PyQt5.QtCore import QSettings, Qt, QTimer, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor, QFontDatabase, QIcon, QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QShortcut, QSplitter, QVBoxLayout, QLabel, QFrame, QSystemTrayIcon, QMenu

from app_settings import AppSettings
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
        self.ICON_MANAGER = IconManager()
        self.project_actions = ProjectActions(
            self,
            project_manager,
            self.show_notification,
        )
        self.document_actions = DocumentActions(self)
        

        self.ui_btn_home.setIcon(IconManager().ICON_DASHBOARD)
        self.ui_btn_data_manager.setIcon(IconManager().ICON_DATA_MANAGER)
        self.ui_btn_text_editor.setIcon(IconManager().ICON_CODE_EDITOR)
        self.btn_app_settings.setIcon(IconManager().ICON_SETTINGS)
        self.btn_app_exit.setIcon(IconManager().ICON_APP_EXIT)
        self.btn_project_open.setIcon(IconManager().ICON_PROJECT_OPEN)
        self.btn_project_new.setIcon(IconManager().ICON_PROJECT_NEW)
        self.btn_project_save.setIcon(IconManager().ICON_PROJECT_SAVE)
        self.btn_project_save_as.setIcon(IconManager().ICON_PROJECT_SAVE_AS)
        self.btn_toggle_menu.setIcon(IconManager().ICON_MENU)

        self.btn_script_new.setIcon(IconManager().ICON_NEW_SCRIPT)
        self.btn_script_open.setIcon(IconManager().ICON_OPEN_SCRIPT)
        self.btn_script_save.setIcon(IconManager().ICON_SAVE_SCRIPT)
        self.btn_script_save_as.setIcon(IconManager().ICON_SAVE_SCRIPT_AS)

        self.btn_insert_chapter.setIcon(IconManager().ICON_INSERT_CHAPTER)
        self.btn_insert_testcase.setIcon(IconManager().ICON_INSERT_TESTCASE)
        self.btn_insert_command.setIcon(IconManager().ICON_INSERT_COMMAND)
        self.btn_comment_uncomment.setIcon(IconManager().ICON_COMMENT_UNCOMMENT)        
        self.btn_format_code.setIcon(IconManager().ICON_FORMAT_CODE)

        self.btn_zoom_in.setIcon(IconManager().ICON_ZOOM_IN)
        self.btn_zoom_out.setIcon(IconManager().ICON_ZOOM_OUT)
        self.btn_zoom_default.setIcon(IconManager().ICON_ZOOM_RESET)
        
        
        ################################################################################################################
        # APP SETTINGS CONFIGURATION
        ################################################################################################################
        self.app_settings = AppSettings(self)
        self.editor_controller = EditorController(self)

        
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

        self.btn_script_new.clicked.connect(self.document_actions.new)
        self.btn_script_new.setShortcut('Ctrl+n')
        self.btn_script_save.clicked.connect(self.document_actions.save)
        self.btn_script_save.setShortcut('Ctrl+s')
        self.btn_script_save_as.clicked.connect(self.document_actions.save_as)
        self.btn_script_open.clicked.connect(self.document_actions.open_from_dialog)
        self.btn_insert_chapter.clicked.connect(
            self.editor_controller.insert_chapter
        )
        self.btn_insert_chapter.setShortcut('Ctrl+Shift+a')
        self.btn_insert_chapter.setToolTip('Chapter (Ctrl+Shift+A)')
        self.btn_insert_testcase.clicked.connect(
            self.editor_controller.insert_testcase
        )
        self.btn_insert_testcase.setShortcut('Ctrl+Shift+t')
        self.btn_insert_testcase.setToolTip('Testcase (Ctrl+Shift+T)')
        self.btn_insert_command.clicked.connect(
            self.editor_controller.insert_command
        )
        self.btn_insert_command.setShortcut('Ctrl+Shift+c')
        self.btn_insert_command.setToolTip('Command (Ctrl+Shift+C)')
        self.btn_comment_uncomment.clicked.connect(
            self.editor_controller.toggle_comment
        )
        self.btn_comment_uncomment.setShortcut('Ctrl+/')
        self.btn_comment_uncomment.setToolTip('(Un)Comment (Ctrl+"/")')
        self.btn_format_code.clicked.connect(
            self.editor_controller.format_code
        )
        self.btn_format_code.setShortcut(('Ctrl+Shift+f'))
        self.btn_format_code.setToolTip(('Format Code (Ctrl+Shift+F)'))
        self.btn_lock_unlock.clicked.connect(self.document_actions.toggle_read_only)
        # self.btn_find_replace.clicked.connect(lambda is_pressed: self.find_replace(is_pressed, only_find=False))
        # self.btn_find_replace.setShortcut('Ctrl+h')
        # self.btn_find_replace.setToolTip('Ctrl + "H"')
        # self.btn_undo.clicked.connect(self.perform_undo)
        # self.btn_redo.clicked.connect(self.perform_redo)
        self.btn_zoom_in.clicked.connect(self.editor_controller.font_increase)
        self.btn_zoom_in.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Plus))
        self.btn_zoom_in.setToolTip("Zoom In (Ctrl+Plus)")
        self.btn_zoom_out.clicked.connect(self.editor_controller.font_decrease)
        self.btn_zoom_out.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Minus))        
        self.btn_zoom_out.setToolTip("Zoom Out (Ctrl+Minus)")
        self.btn_zoom_default.clicked.connect(self.editor_controller.font_reset)
        self.btn_zoom_default.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_0))
        self.btn_zoom_default.setToolTip("Reset Zoom (Ctrl+0)")

        QShortcut('Ctrl+f', self).activated.connect(
            lambda: self.editor_controller.show_find_replace(only_find=True)
        )
        QShortcut('Ctrl+h', self).activated.connect(
            lambda: self.editor_controller.show_find_replace(only_find=False)
        )

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
        # self.btn_show_hide_file_manager.clicked.connect(lambda: self.toggleMenu(self.frame_file_manager, 0, 350))
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
        # self.uiLayoutFileManager.addWidget(self.tree_file_browser)
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
        # self.uiLayoutFileManager.addWidget(QPushButton("Outline"))
        # self.uiLayoutFileManager.addWidget(self.uiTreeOutline)
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
        self.app_settings.save_settings_2_disk()

        has_modified_files = any(
            text_edit.is_modified()
            for text_edit, _ in self.tab_manager.iter_text_edits()
        )
        if has_modified_files:
            answer = QMessageBox.question(
                self,
                "R2ScriptEditor",
                "Some opened files have been modified.\n\nDo you want to discard changes?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if answer != QMessageBox.Yes:
                event.ignore()
                return

        if not project_manager.is_project_saved():
            answer = QMessageBox.question(
                self,
                "R2ScriptEditor",
                "Current project is not saved.\n\nDo you want to exit (all changes will be lost)?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if answer != QMessageBox.Yes:
                event.ignore()
                return

        event.accept()





        







########################################################################################################################
# APP CONFIG:
########################################################################################################################



# def _show_tray_message(title, message):
#     system_tray.showMessage(title, message, qta.icon('mdi.information-outline', color='#4863ff', scale_factor=1), 2000)



# def _show_window(reason):
#     if reason != QSystemTrayIcon.Context:
#         pywinstyles.apply_style(window,"dark")
#         window.show()


# def _exit_app():
#     success = _manage_events_before_close()
#     if success:
#         app.quit()



if __name__ == "__main__":

    app = QApplication([])
    
    # app.setFont(font)
    # QFontDatabase.addApplicationFont('ui/fonts/segoeui.ttf')p
    # QFontDatabase.addApplicationFont('ui/fonts/segoeuib.ttf')
    # file = QFile("ui/dark.qss")
    # file.open(QFile.ReadOnly | QFile.Text)
    # stream = QTextStream(file)
    # app.setStyleSheet(stream.readAll())
    app.setStyle('Fusion')
    # app.setStyleSheet(config.app_styles.STYLES)
    

    
    window = MainWindow()

    pywinstyles.apply_style(window,"dark")


    window.show()






    # app.setQuitOnLastWindowClosed(False)

    # system_tray = QSystemTrayIcon(QIcon('R2Editor.ico'), app)
    # system_tray.setToolTip('R2ScriptEditor')
    # system_tray.show()
    # system_tray.activated.connect(_show_window)

    
    # menu = QMenu()
    # action_show_app = menu.addAction('Show')
    # action_exit_app = menu.addAction('Exit')
    # action_show_app.triggered.connect(_show_window)
    # action_exit_app.triggered.connect(_exit_app)
    # system_tray.setContextMenu(menu)


    # # Running the aforementioned command and saving its output
    # output = os.popen('wmic process get description, processid').read()
    
    # if len(re.findall("r2editor.exe", output, re.IGNORECASE)) > 1:
    #     input = QMessageBox.question(window,
    #                                 "R2Editor",
    #                                 "R2Editor is already running in background.\n\nPress OK to close this instance.",
    #                                 QMessageBox.Ok)

    #     if input == QMessageBox.Ok:
            
    #         sys.exit()

    # else:
    #     sys.exit(app.exec_())
    
    sys.exit(app.exec_())

