import os
import re
import stat
import sys
from pathlib import Path

import pywinstyles
from PyQt5.QtCore import (QEasingCurve, QEvent, QFile, QPoint,
                          QPropertyAnimation, QRect, QSettings, QSize, Qt,
                          QTextStream, QTimer, pyqtSignal, pyqtSlot)
from PyQt5.QtGui import (QColor, QFontDatabase, QIcon, QKeySequence, QPalette,
                         QTextCursor)
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QHBoxLayout,
                             QMainWindow, QMenu, QMessageBox, QPushButton,
                             QShortcut, QSizeGrip, QSplitter, QTabWidget,
                             QToolTip, QVBoxLayout, QWidget)

from app_settings import AppSettings
from components.notification_widget import NotificationWidget
from components.pyqt_find_text_widget.findReplaceTextWidget import \
    FindReplaceTextWidget
from components.pyqt_find_text_widget.findTextWidget import FindTextWidget
from components.template_test_case import TemplateTestCase
from config.font import font
from dashboard.dashboard import Dashboard
from data_manager import project_manager
from data_manager.data_manager import DataManager
from data_manager.requirement_nodes import RequirementFileNode
from dialogs.dialog_message import dialog_message
from dialogs.form_find_replace import FindAndReplace
from dialogs.window_project_config import ProjectConfig
from file_browser.tree_file_browser import FileSystemView
from tabs import Tabs
from text_editor import text_management
from text_editor.text_editor import TextEdit
from ui.main_ui import Ui_MainWindow

# from dialogs.dialog_recent_projects import RecentProjects





_FILE_FILTER = 'RapitTwo Editor Project (*.json)'

# pyinstaller -w --icon=R2Editor.ico main.py
# pyinstaller -w --icon=R2Editor.ico --name=R2Editor main.py

class MainWindow(QMainWindow, Ui_MainWindow):

    open_project = pyqtSignal(str)
    save_project = pyqtSignal(str)
    script_requirement_reference_changed = pyqtSignal(set, str)

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.resize(1920, 1080)

        self.setWindowIcon(QIcon('R2Editor.ico'))
        self.setWindowTitle("R2Editor")

        self.splitter.setStyleSheet("QSplitterHandle:hover {}  QSplitter::handle:horizontal:hover {background-color:rgb(58,89,245);}")
        
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.frame_top.setVisible(False)

        self.palette = QPalette()
        self.palette.setColor(QPalette.Window, QColor(58,89,245))
        self.palette.setColor(QPalette.Text, QColor(200, 200, 200))
        self.palette.setColor(QPalette.WindowText, QColor(200, 200, 200))
        self.setPalette(self.palette)
        
        # QSizeGrip(self.frame_size_grip)

        ## HIDE NOT-WORKING UI COMPONENTS
        # self.btn_project_recent.setVisible(False)
        # self.btn_undo.setVisible(False)
        # self.btn_redo.setVisible(False) 
        # self.frame_11.setVisible(False)       
        
        ## CONNECT BUTTONS
        
        self.btn_app_exit.clicked.connect(self.close)

        self.btn_project_open.clicked.connect(self.project_open)
        self.btn_project_new.clicked.connect(self.project_new)
        self.btn_project_save.clicked.connect(self.project_save)
        self.btn_project_save_as.clicked.connect(self.project_save_as)
        # self.btn_project_recent.clicked.connect(self.show_recent_projects)


        self.btn_script_new.clicked.connect(self.file_new)
        self.btn_script_new.setShortcut('Ctrl+n')
        self.btn_script_save.clicked.connect(self.file_save)
        self.btn_script_save.setShortcut('Ctrl+s')
        self.btn_script_save_as.clicked.connect(self.file_save_as)
        self.btn_script_open.clicked.connect(self.file_open_from_dialog)
        self.btn_insert_chapter.clicked.connect(self.insert_chapter)
        self.btn_insert_chapter.setShortcut('Ctrl+Shift+a')
        self.btn_insert_chapter.setToolTip('Ctrl + Shift + "A"')
        self.btn_insert_testcase.clicked.connect(self.insert_testcase)
        self.btn_insert_testcase.setShortcut('Ctrl+Shift+t')
        self.btn_insert_testcase.setToolTip('Ctrl + Shift + "T"')
        self.btn_insert_command.clicked.connect(self.insert_command)
        self.btn_insert_command.setShortcut('Ctrl+Shift+c')
        self.btn_insert_command.setToolTip('Ctrl + Shift + "C"')
        self.btn_comment_uncomment.clicked.connect(self.comment_uncomment)
        self.btn_comment_uncomment.setShortcut('Ctrl+/')
        self.btn_comment_uncomment.setToolTip('Ctrl + "/"')
        self.btn_format_code.clicked.connect(self.format_code)
        self.btn_format_code.setShortcut(('Ctrl+Shift+f'))
        self.btn_lock_unlock.clicked.connect(self.file_lock_unlock)
        # self.btn_find_replace.clicked.connect(lambda is_pressed: self.find_replace(is_pressed, only_find=False))
        # self.btn_find_replace.setShortcut('Ctrl+h')
        # self.btn_find_replace.setToolTip('Ctrl + "H"')
        self.btn_undo.clicked.connect(self.perform_undo)
        self.btn_redo.clicked.connect(self.perform_redo)
        self.btn_zoom_in.clicked.connect(self.font_increase)
        self.btn_zoom_in.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Plus))
        self.btn_zoom_out.clicked.connect(self.font_decrease)
        self.btn_zoom_out.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Minus))        
        self.btn_zoom_default.clicked.connect(self.font_reset)
        self.btn_zoom_default.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_0))    

        QShortcut( 'Ctrl+f', self ).activated.connect((lambda: self.find_replace(only_find=True)))            
        QShortcut( 'Ctrl+h', self ).activated.connect((lambda: self.find_replace(only_find=False)))   
               

        self.frame_file_manager.setVisible(False)
        self.frame_2.setVisible(False)
        self.actual_find_box = None





        

        # def maximize_restore():
        #     if self.isMaximized():
        #         self.showNormal()
        #         self.btn_maximize_restore.setIcon(QIcon(u"ui/icons/16x16/cil-window-maximize.png"))
        #     else:
        #         self.showMaximized()
        #         self.btn_maximize_restore.setIcon(QIcon(u"ui/icons/16x16/cil-window-restore.png"))

        # def doubleClickMaximizeRestore(event):
        #     # IF DOUBLE CLICK CHANGE STATUS
        #     if event.type() == QEvent.MouseButtonDblClick:
        #         QTimer.singleShot(50, maximize_restore)                

        # def moveWindow(e):
        #     # Detect if the window is  normal size
        #     # ###############################################
        #     if self.isMaximized() == False: #Not maximized
        #         # Move window only when window is normal size
        #         # ###############################################
        #         #if left mouse button is clicked (Only accept left mouse button clicks)
        #         if e.buttons() == Qt.LeftButton:
        #             #Move window
        #             self.move(self.pos() + e.globalPos() - self.clickPosition)
        #             self.clickPosition = e.globalPos()
        #             e.accept()

        # #######################################################################
        # # Add click event/Mouse move event/drag event to the top header to move the window
        # #######################################################################
        # self.frame_top_btns.mouseMoveEvent = moveWindow
        # self.frame_top_btns.mouseDoubleClickEvent = doubleClickMaximizeRestore
        # #######################################################################                

        ## TOGGLE/BURGUER MENU
        ########################################################################
        self.btn_toggle_menu.clicked.connect(lambda: self.toggle_menu(self.frame_left_menu, 70, 210))
        # self.btn_show_hide_file_manager.clicked.connect(lambda: self.toggleMenu(self.frame_file_manager, 0, 350))
        self.btn_close.clicked.connect(self.close)
        # self.btn_maximize_restore.clicked.connect(maximize_restore)
        # self.btn_minimize.clicked.connect(lambda: self.showMinimized())








        self.VERSION = '2021-03-04'
        # FILTER FOR OPENING/SAVING SCRIPTS AND PROJECTS
        self.filter_script = 'RapitTwo Script (*.par)'


        ################################################################################################################
        # APP SETTINGS CONFIGURATION
        ################################################################################################################
        self.app_settings = AppSettings(self)        

        ################################################################################################################
        # POINTER TO ACTUAL TEXTEDIT, ACTUAL TABS
        ################################################################################################################
        self._actual_text_edit = None
        self.actual_tabs = None

        self.opened_project_path = None

        ################################################################################################################
        # TREE FILE BROWSER CONFIGURATION
        ################################################################################################################
        self.tree_file_browser = FileSystemView(self, project_manager)
        self.verticalLayout_7.addWidget(self.tree_file_browser)


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
        self.left_tabs.tabCloseRequested.connect(self.left_tab_close_request)
        self.left_tabs.currentChanged.connect(self.left_tab_was_changed)
        self.left_tabs.tabBarClicked.connect(self.left_tab_was_changed)
        self.left_tabs.currentChanged.connect(self.update_find_replace)

        self.right_tabs = Tabs(self, False, 'RIGHT_TABS')
        self.right_tabs.tabCloseRequested.connect(self.right_tab_close_request)
        self.right_tabs.currentChanged.connect(self.right_tab_was_changed)
        self.right_tabs.tabBarClicked.connect(self.right_tab_was_changed)
        self.right_tabs.currentChanged.connect(self.update_find_replace)

        self.tabs_splitter = QSplitter()
        self.tabs_splitter.addWidget(self.left_tabs)
        self.tabs_splitter.addWidget(self.right_tabs)
        self.tabs_splitter.setStretchFactor(2, 1)
        self.tabs_splitter.setStyleSheet('background-color: rgb(33, 37, 43); border:None;')


        ################################################################################################################
        # STACKEDWIDGET CONFIGURATION
        # ########################################################################
        
        self.stackedWidget.addWidget(self.tabs_splitter)
        self.stackedWidget.addWidget(self.data_manager)
        self.stackedWidget.addWidget(self.app_settings)
        self.stackedWidget.addWidget(self.dashboard)
        self.stackedWidget.setCurrentWidget(self.dashboard)


        self.ui_btn_text_editor.clicked.connect(lambda: self.manage_right_menu(self.tabs_splitter, self.ui_btn_text_editor))
        self.ui_btn_data_manager.clicked.connect(lambda: self.manage_right_menu(self.data_manager, self.ui_btn_data_manager))
        self.ui_btn_home.clicked.connect(lambda: self.manage_right_menu(self.dashboard, self.ui_btn_home))
        self.btn_app_settings.clicked.connect(lambda: self.manage_right_menu(self.app_settings, self.btn_app_settings))

    #     QShortcut( 'Esc', self.tabs_splitter).activated.connect(self.press_esc)


    # def press_esc(self):
    #     # Close FindNReplace Widget if it is Visible
    #     self.find_replace(False)
    #     self.btn_find_replace.setChecked(False)

        self.notification_widget = NotificationWidget(self)

    @property
    def actual_text_edit(self):
        return self._actual_text_edit


    @actual_text_edit.setter
    def actual_text_edit(self, text_edit):
        self._actual_text_edit = text_edit
     


    def keyPressEvent(self, e) -> None:
        if e.key() == Qt.Key_Escape:
            # self.find_replace(False)
            # self.btn_find_replace.setChecked(False)
            if self.actual_find_box:
                self.ui_hLayout_findReplace.removeWidget(self.actual_find_box) 
            if self.actual_text_edit:
                self.actual_text_edit.setFocus()
        return super().keyPressEvent(e)

    def manage_right_menu(self, widget, button):

        self.ui_btn_home.setChecked(False)
        self.ui_btn_text_editor.setChecked(False)
        self.ui_btn_data_manager.setChecked(False)
        self.btn_app_settings.setChecked(False)
        self.stackedWidget.setCurrentWidget(widget)
        button.setChecked(True)
        if button is not self.ui_btn_text_editor:
            self.frame_file_manager.setVisible(False)
            self.frame_2.setVisible(False)
        else:
            self.frame_file_manager.setVisible(True)
            self.frame_2.setVisible(True)



    #######################################################################
    # Add mouse events to the window
    #######################################################################
    # def mousePressEvent(self, event):
    #     # ###############################################
    #     # Get the current position of the mouse
    #     self.clickPosition = event.globalPos()
    #     # For moving window
    #######################################################################
    #######################################################################

    def toggle_menu(self, toggled_frame, min_width, max_width):
        # GET ACTUAL WIDTH
        width = toggled_frame.width()
        # SET DESIRED WIDTH
        extended_width = max_width if width == min_width else min_width
        # ANIMATION
        self.animation = QPropertyAnimation(toggled_frame, b"minimumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(width)
        self.animation.setEndValue(extended_width)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()
        if self.btn_toggle_menu.isChecked():
            self.btn_toggle_menu.setStyleSheet("background-image: url(:/20x20/icons/20x20/cil-x.png);")
        else:
            self.btn_toggle_menu.setStyleSheet("background-image: url(:/20x20/icons/20x20/cil-menu.png);")











########################################################################################################################
# TABS MANAGEMENT METHODS:  START
########################################################################################################################


    def clicked_on_text_edit(self, edit_text):
        self.actual_text_edit = edit_text

        if self.left_tabs.indexOf(edit_text) == -1:
            self.actual_tabs = self.right_tabs
        else:
            self.actual_tabs = self.left_tabs

        self.update_actual_information()


    def left_tab_was_changed(self, tab_index):
        if self.left_tabs.count() > 0:
            self.actual_tabs = self.left_tabs
            self.actual_text_edit = self.actual_tabs.widget(tab_index)
            self.update_actual_information()
            self.actual_text_edit.setFocus()



    def left_tab_close_without_saving(self, tab_index):
        self.left_tabs.removeTab(tab_index)
        if self.left_tabs.count() == 0 and not self.right_tabs.isVisible():
            self.actual_tabs = None
            self.actual_text_edit = None
        elif self.left_tabs.count() == 0 and self.right_tabs.isVisible():
            self.actual_tabs = self.right_tabs
            self.actual_text_edit = self.right_tabs.currentWidget()
        self.update_actual_information()


    def left_tab_close_request(self, tab_index):
        if not self.left_tabs.widget(tab_index).file_was_modified:
            self.left_tab_close_without_saving(tab_index)
        else:
            popup = QMessageBox(self)
            popup.setIcon(QMessageBox.Question)
            popup.setWindowTitle("R2 Editor")
            popup.setText("The file has been modified")
            popup.setInformativeText("Do you want to save your changes?")
            popup.setStandardButtons(QMessageBox.Save |
                                     QMessageBox.Cancel |
                                     QMessageBox.Discard)
            popup.setDefaultButton(QMessageBox.Save)
            answer = popup.exec_()

            if answer == QMessageBox.Save:
                backup_text_edit = self.actual_text_edit
                self.actual_text_edit = self.left_tabs.widget(tab_index)
                self.file_save()
                self.actual_text_edit = backup_text_edit
                self.left_tab_close_without_saving(tab_index)

            elif answer == QMessageBox.Discard:
                self.left_tab_close_without_saving(tab_index)

        self.update_actual_information()


    def right_tab_was_changed(self, tab_index):
        if self.right_tabs.count() > 0:
            self.actual_tabs = self.right_tabs
            self.actual_text_edit = self.actual_tabs.widget(tab_index)
            self.update_actual_information()
            self.actual_text_edit.setFocus()


    def right_tab_close_without_saving(self, tab_index):
        self.right_tabs.removeTab(tab_index)
        if self.right_tabs.count() == 0:
            self.right_tabs.setVisible(False)
            if self.left_tabs.count() > 0:
                self.actual_text_edit = self.left_tabs.currentWidget()
                self.actual_tabs = self.left_tabs
            else:
                self.actual_tabs = None
                self.actual_text_edit = None

    def right_tab_close_request(self, tab_index):
        if not self.right_tabs.widget(tab_index).file_was_modified:
            self.right_tab_close_without_saving(tab_index)
        else:
            popup = QMessageBox(self)
            popup.setIcon(QMessageBox.Question)
            popup.setWindowTitle("R2 Editor")
            popup.setText("The file has been modified")
            popup.setInformativeText("Do you want to save your changes?")
            popup.setStandardButtons(QMessageBox.Save |
                                     QMessageBox.Cancel |
                                     QMessageBox.Discard)
            popup.setDefaultButton(QMessageBox.Save)
            answer = popup.exec_()

            if answer == QMessageBox.Save:
                backup_text_edit = self.actual_text_edit
                self.actual_text_edit = self.right_tabs.widget(tab_index)
                self.file_save()
                self.actual_text_edit = backup_text_edit
                self.right_tab_close_without_saving(tab_index)

            elif answer == QMessageBox.Discard:
                self.right_tab_close_without_saving(tab_index)

        self.update_actual_information()


    def set_actual_tab_icon(self, file_was_modified):
        tab_index = self.actual_tabs.indexOf(self.actual_text_edit)
        if file_was_modified:
            self.actual_tabs.setTabIcon(tab_index, QIcon(u"ui/icons/16x16/cil-description.png"))
        else:
            self.actual_tabs.setTabIcon(tab_index, QIcon(u"ui/icons/16x16/cil-file.png"))


########################################################################################################################
# TABS MANAGEMENT METHODS:  END
########################################################################################################################





########################################################################################################################
# FILE MANAGEMENT METHODS:  START
########################################################################################################################



    def get_all_opened_files(self):
        opened_files = {}
        for tab_index in range(self.left_tabs.count()):
            text_edit = self.left_tabs.widget(tab_index)
            opened_files.update({text_edit.file_path: [text_edit, self.left_tabs]})
        for tab_index in range(self.right_tabs.count()):
            text_edit = self.right_tabs.widget(tab_index)
            opened_files.update({text_edit.file_path: [text_edit, self.right_tabs]})
        return opened_files


    def file_open_from_dialog(self):
        path, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption='Open Script',
            directory=self.tree_file_browser.current_path,
            filter=self.filter_script
        )

        if not path:
            return
        else:
            try:
                self.file_open_from_tree(Path(path))
                # self.update_title()
            except Exception as my_exception:
                dialog_message(self, str(my_exception))        



    @pyqtSlot(Path)
    def file_open_from_tree(self, file_path: Path):
        try:
            file_suffix = file_path.suffix
            opened_files = self.get_all_opened_files()
            if file_suffix.lower() in ('.par', '.py', '.con', '.xml', '.txt', '.map'):
                if file_path not in opened_files:
                    with open(file_path, 'r') as file_to_open:
                        text = file_to_open.read()
                        # file_to_open.close()

                    # tab_name = file_path.split('/')[-1]
                    tab_name = file_path.name
                    self.left_tabs.addTab(TextEdit(self, text, file_path), QIcon(u"ui/icons/16x16/cil-file.png"), tab_name)

                else:
                    opened_files[file_path][1].setCurrentWidget(opened_files[file_path][0])
                    self.actual_tabs = opened_files[file_path][1]
                    self.actual_text_edit = opened_files[file_path][0]
                    self.update_actual_information()
        except Exception as e:
            dialog_message(self, str(e))


    
    def find_reference_in_string(self, string):
        PATTERN_REQ_REFERENCE = re.compile(r'(?:REFERENCE|\$REF:)\s*"(?P<req_reference>[\w\d,/\s\(\)-]+)"\s*', re.IGNORECASE)
        match_list = PATTERN_REQ_REFERENCE.findall(string)
        # print(match_list)
        references = set()
        for match_string in match_list:
            matches = match_string.split(",")
            matches = [match.strip().lower() for match in matches]
            references.update(set(matches))

        return references




    def update_coverage(self, text_to_save, original_text, file_path):
        ################ TEST CHECK COVERAGE IN DATAMANAGER TREE:
        references_original_text = self.find_reference_in_string(original_text)
        references_text_to_save = self.find_reference_in_string(text_to_save)

        missing_references = references_original_text.difference(references_text_to_save)
        new_references = references_text_to_save.difference(references_original_text)

        references = missing_references.union(new_references)

        # print("MISSING: ", missing_references)
        # print("NEW: ", new_references)

        self.script_requirement_reference_changed.emit(references, str(Path(file_path)))




    def file_save(self):
        if self.actual_text_edit:
            if self.app_settings.format_code_when_save:
                if self.actual_text_edit.file_path is not None:
                    if Path(self.actual_text_edit.file_path).suffix.lower() in ('.par','.txt'):
                        self.format_code()
            if self.actual_text_edit.file_path == None:
                self.file_save_as()
            else:
                try:
                    text_to_save = self.actual_text_edit.toPlainText()
                    with open(self.actual_text_edit.file_path, 'w') as file_to_save:
                        file_to_save.write(text_to_save)
                        file_to_save.close()

                        self.update_coverage(self.actual_text_edit.toPlainText(), self.actual_text_edit.original_file_content, self.actual_text_edit.file_path)

                        self.actual_text_edit.original_file_content = text_to_save
                        self.actual_text_edit.file_was_modified = False
                        self.set_actual_tab_icon(False)





                except Exception as exception_to_show:
                    dialog_message(self, str(exception_to_show))

        self.update_actual_information()




    def file_save_as(self):
        path, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption='Save Script',
            directory=self.tree_file_browser.current_path,
            filter=self.filter_script
        )

        if not path:
            return
        else:
            try:
                text_to_save = self.actual_text_edit.toPlainText()
                with open(path, 'w') as file_to_save:
                    file_to_save.write(text_to_save)
                    file_to_save.close()

                    self.update_coverage(self.actual_text_edit.toPlainText(), self.actual_text_edit.original_file_content, path)

                    self.actual_text_edit.original_file_content = text_to_save
                    self.actual_text_edit.file_was_modified = False
                    self.set_actual_tab_icon(False)
                    self.actual_text_edit.file_path = path
                    current_tab_index = self.actual_tabs.indexOf(self.actual_text_edit)
                    self.actual_tabs.setTabText(current_tab_index, path.split('/')[-1])                    

            except Exception as exception_to_show:
                dialog_message(self, str(exception_to_show))

        self.update_actual_information()



    def file_new(self):
        template = TemplateTestCase()
        text = template.generate_tc_template()
        file_path = None
        tab_name = 'Untitled'
        self.left_tabs.addTab(TextEdit(self, text, file_path), QIcon(u"ui/icons/16x16/cil-description.png"), tab_name)
        self.actual_text_edit.setFocus()


    def file_lock_unlock(self):
        if self.actual_text_edit:
            try:
                if self.actual_text_edit.is_read_only:
                    os.chmod(self.actual_text_edit.file_path, stat.S_IWRITE)
                    self.actual_text_edit.is_read_only = False
                else: 
                    os.chmod(self.actual_text_edit.file_path, stat.S_IREAD)
                    self.actual_text_edit.is_read_only = True
            except TypeError as e:
                dialog_message(self, f"File is not saved! Save the file first. {str(e)}.")
                self.actual_text_edit.setFocus()
                

########################################################################################################################
# FILE MANAGEMENT METHODS:  END
########################################################################################################################

########################################################################################################################
# PROJECT MANAGEMENT METHODS:  START
########################################################################################################################
    def receive_parameters_from_project_manager(self, parameters: dict):
        self.update_project_title(parameters)


    def update_project_title(self, project_params:dict):
        json_project_path = project_params.get("json_project_path")
        is_project_saved = project_params.get("is_project_saved")
        str_modified_status = "" if is_project_saved else "[*Modified]"
        str_project_path = str(json_project_path) if json_project_path else "New Project"  
        
        # self.setWindowTitle(f"{str_project_path} {str_modified_status} - R2 Script Editor")

        self.label_opened_project.setText(f"{str_project_path} {str_modified_status}") 
        if is_project_saved:
            self.label_opened_project.setStyleSheet("color: rgb(200, 200, 200)")
        else:
            self.label_opened_project.setStyleSheet("color: rgb(250, 100, 100); font-weight: bold")
        

    def update_actual_information(self):
        self._update_btn_lock_unlock()
        self._update_tabs_color()
        self._update_script_label()


    def _update_btn_lock_unlock(self):
        if self.actual_text_edit:
            self.btn_lock_unlock.setChecked(self.actual_text_edit.is_read_only)
        else:
           self.btn_lock_unlock.setChecked(False)  


    def _update_tabs_color(self):
        # UNDERLINE ACTUAL TAB WITH COLOR
        if self.actual_tabs:
            self.left_tabs.setStyleSheet('QTabBar::tab {border-bottom: 3px solid #31363b}')
            self.right_tabs.setStyleSheet('QTabBar::tab {border-bottom: 3px solid #31363b}')
            self.actual_tabs.setStyleSheet('QTabBar::tab:selected {border-bottom: 3px solid rgb(0, 128, 255)}')        


    def _update_script_label(self):
        self.setWindowTitle(f"R2 Editor - {self.actual_text_edit.file_path}" if self.actual_text_edit else "R2 Editor")


   
    
    def show_notification(self, notification_text):
        self.notification_widget.show_text(notification_text)




    def project_new(self):
        self.opened_project_path = None
        self.window = ProjectConfig(self, is_new_project=True)
        self.window.show()

    def project_save(self):        
        success, message = project_manager.save_project()
        if success:
            self.show_notification(message)
        elif message == "NO JSON PATH":
            self.project_save_as()
        else:
            dialog_message(message)


    def project_save_as(self):        
        path, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption='Save Project',
            directory='.//Projects',
            filter=_FILE_FILTER
        )
        if not path:
            return
        success, message = project_manager.save_project_as(path)
        if success:
            self.show_notification(message)
        else:
            dialog_message(message)            


    def project_open(self):
        if not project_manager.is_project_saved():
            proceed = QMessageBox.question(self,
                            "R2ScriptEditor",
                            "Current project is not saved.\n\nDo you want to proceed (all changes will be lost)?",
                            QMessageBox.Yes | QMessageBox.No)
            if proceed == QMessageBox.No:
                return

        path, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption='Open Project',
            directory='.//Projects',
            filter=_FILE_FILTER
        )

        if not path:
            return
        else:
            success, error_message = project_manager.open_project(path)
            if not success:
                dialog_message(self, f"Failed to Open Project!\n{error_message}")





########################################################################################################################
# PROJECT MANAGEMENT METHODS:  END
########################################################################################################################



########################################################################################################################
# REST OF ACTION METHODS:  START
########################################################################################################################




    def insert_command(self):
        if self.actual_text_edit:
            text_management.insert_command(self.actual_text_edit)
            self.actual_text_edit.setFocus()

    def insert_testcase(self):
        if self.actual_text_edit:
            text_management.insert_testcase(self.actual_text_edit)
            self.actual_text_edit.setFocus()

    def insert_chapter(self):
        if self.actual_text_edit:
            text_management.insert_chapter(self.actual_text_edit)
            self.actual_text_edit.setFocus()

    def comment_uncomment(self):
        if self.actual_text_edit:
            text_management.indent_dedent_comment(self.actual_text_edit, variant='comment')
            self.actual_text_edit.setFocus()

    
    def update_find_replace(self):
        if self.ui_hLayout_findReplace.count():
            self.find_replace(self.actual_find_box.only_find_widget)
        


    
    def find_replace(self, only_find):
        if not self.actual_text_edit:
            return
        


        if self.actual_find_box:
                self.ui_hLayout_findReplace.removeWidget(self.actual_find_box) 


        # new_find_box = FindTextWidget(self.actual_text_edit)
        self.new_find_box = FindReplaceTextWidget(self.actual_text_edit)
        self.ui_hLayout_findReplace.addWidget(self.new_find_box)
        self.new_find_box.setFocus()
        self.actual_find_box = self.new_find_box
        TextEdit.update_ctrl_pressed(False)
        # self.actual_text_edit.setStyleSheet("selection-background-color: red;")


        self.actual_find_box.setOnlyFindTextWidget(only_find)
        


    def format_code(self):
        # from importlib import reload
        # reload(text_management)
        if self.actual_text_edit:
            try:
                # text_management.format_text(self.actual_text_edit)
                text_management.TextFormatter(self.actual_text_edit).run()
                self.actual_text_edit.setFocus()
            except Exception as exc:
                print(str(exc))
                

    def perform_undo(self):
        if self.actual_text_edit:
            self.actual_text_edit.undo()
            self.actual_text_edit.setFocus()

    def perform_redo(self):
        if self.actual_text_edit:
            self.actual_text_edit.redo()
            self.actual_text_edit.setFocus()

    def font_increase(self):
        if self.actual_text_edit: self.actual_text_edit.font_increase()

    def font_decrease(self):
        if self.actual_text_edit: self.actual_text_edit.font_decrease()

    def font_reset(self):
        if self.actual_text_edit: self.actual_text_edit.font_reset()                




########################################################################################################################
# REST OF ACTION METHODS:  END
########################################################################################################################

    # SAVE WINDOW SIZE, POSITION BEFORE CLOSE APP AND CHECK IF ALL SCRIPTS ARE SAVED
    def closeEvent(self, event):
        # self.settings.setValue('size', self.size())
        # self.settings.setValue('position', self.pos())
        # self.settings.setValue('last_opened_project', self.opened_project_path)

        self.app_settings.save_settings()
        opened_files = self.get_all_opened_files()
        for path, val in opened_files.items():
            text_edit = val[0]
            if text_edit.file_was_modified:
                close = QMessageBox.question(self,
                                           "R2ScriptEditor",
                                           "Some of opened files have been modified.\n\nDo you want to discard changes?",
                                           QMessageBox.Yes | QMessageBox.No)
                if close == QMessageBox.Yes:
                    event.accept()
                else:
                    event.ignore()

        if not project_manager.is_project_saved():
            close = QMessageBox.question(self,
                                        "R2ScriptEditor",
                                        "Current project is not saved.\n\nDo you want to exit (all changes will be lost)?",
                                        QMessageBox.Yes | QMessageBox.No)
            if close == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()





if __name__ == "__main__":

    app = QApplication([])
    

    
    

    # app.setFont(font)

    QFontDatabase.addApplicationFont('ui/fonts/segoeui.ttf')
    QFontDatabase.addApplicationFont('ui/fonts/segoeuib.ttf')
    file = QFile("ui/dark.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())
    app.setStyle('Fusion')
    

    
    window = MainWindow()

    pywinstyles.apply_style(window,"dark")


    window.show()

    sys.exit(app.exec_())

