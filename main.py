import os, re
import stat
import sys
import functools
from pathlib import Path
from importlib import reload
import qtawesome as qta
import pywinstyles

from PyQt5.QtCore import QEasingCurve, QPropertyAnimation, QSettings, Qt, QTimer, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor, QFontDatabase, QIcon, QKeySequence
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox, QShortcut, QSplitter, QTreeWidgetItem, QVBoxLayout, QLabel, QFrame, QSystemTrayIcon, QMenu

from app_settings import AppSettings
from components.notification_widget import NotificationWidget
from components.pyqt_find_text_widget.findReplaceTextWidget import FindReplaceTextWidget
from components.template_test_case import TemplateTestCase
from config.font import font
from dashboard.dashboard import Dashboard
from data_manager import project_manager
from data_manager.data_manager import DataManager
from dialogs.dialog_message import dialog_message
from file_browser.tree_file_browser import FileSystemView
from tabs import Tabs
from text_editor import text_management
from text_editor.text_editor import TextEdit
from ui.main_ui import Ui_MainWindow
from config import constants
import config.app_styles
from components.syntax_highlighter import python_highlighter, rapit_two_highlighter
from config.icon_manager import IconManager
from components.widgets.widgets_pointing_hand import TreeWidgetPointingHand
from components.smooth_scrolling import SmoothScrolling



_FILE_FILTER = 'RapitTwo Editor Project (*.json)'

# pyinstaller -w --icon=R2Editor.ico --name=R2Editor main.py


class MainWindow(QMainWindow, Ui_MainWindow):

    open_project = pyqtSignal(str)
    save_project = pyqtSignal(str)
    script_requirement_reference_changed = pyqtSignal(set, str)

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.ICON_MANAGER = IconManager()
        

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


        # self.timer = QTimer()
        # self.timer.start(3000)
        # self.timer.timeout.connect(lambda: self.change_theme(self.app_settings.theme))

        self.timer_4_updating_outline = QTimer()
        self.timer_4_updating_outline.start(500)
        self.timer_4_updating_outline.timeout.connect(self.update_outline)

        self.resize(1920, 1080)

        self.setWindowIcon(QIcon('R2Editor.ico'))
        self.setWindowTitle("Editor")
        self.frame_top.setVisible(False)
          
        ## CONNECT BUTTONS        
        self.btn_app_exit.clicked.connect(self.close)

        self.btn_project_open.clicked.connect(self.project_open)
        self.btn_project_new.clicked.connect(self.project_new)
        self.btn_project_save.clicked.connect(self.project_save)
        self.btn_project_save_as.clicked.connect(self.project_save_as)

        self.btn_script_new.clicked.connect(self.file_new)
        self.btn_script_new.setShortcut('Ctrl+n')
        self.btn_script_save.clicked.connect(self.file_save)
        self.btn_script_save.setShortcut('Ctrl+s')
        self.btn_script_save_as.clicked.connect(self.file_save_as)
        self.btn_script_open.clicked.connect(self.file_open_from_dialog)
        self.btn_insert_chapter.clicked.connect(self.insert_chapter)
        self.btn_insert_chapter.setShortcut('Ctrl+Shift+a')
        self.btn_insert_chapter.setToolTip('Chapter (Ctrl+Shift+A)')
        self.btn_insert_testcase.clicked.connect(self.insert_testcase)
        self.btn_insert_testcase.setShortcut('Ctrl+Shift+t')
        self.btn_insert_testcase.setToolTip('Testcase (Ctrl+Shift+T)')
        self.btn_insert_command.clicked.connect(self.insert_command)
        self.btn_insert_command.setShortcut('Ctrl+Shift+c')
        self.btn_insert_command.setToolTip('Command (Ctrl+Shift+C)')
        self.btn_comment_uncomment.clicked.connect(self.comment_uncomment)
        self.btn_comment_uncomment.setShortcut('Ctrl+/')
        self.btn_comment_uncomment.setToolTip('(Un)Comment (Ctrl+"/")')
        self.btn_format_code.clicked.connect(self.format_code)
        self.btn_format_code.setShortcut(('Ctrl+Shift+f'))
        self.btn_format_code.setToolTip(('Format Code (Ctrl+Shift+F)'))
        self.btn_lock_unlock.clicked.connect(self.file_lock_unlock)
        # self.btn_find_replace.clicked.connect(lambda is_pressed: self.find_replace(is_pressed, only_find=False))
        # self.btn_find_replace.setShortcut('Ctrl+h')
        # self.btn_find_replace.setToolTip('Ctrl + "H"')
        # self.btn_undo.clicked.connect(self.perform_undo)
        # self.btn_redo.clicked.connect(self.perform_redo)
        self.btn_zoom_in.clicked.connect(self.font_increase)
        self.btn_zoom_in.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Plus))
        self.btn_zoom_in.setToolTip("Zoom In (Ctrl+Plus)")
        self.btn_zoom_out.clicked.connect(self.font_decrease)
        self.btn_zoom_out.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Minus))        
        self.btn_zoom_out.setToolTip("Zoom Out (Ctrl+Minus)")
        self.btn_zoom_default.clicked.connect(self.font_reset)
        self.btn_zoom_default.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_0))
        self.btn_zoom_default.setToolTip("Reset Zoom (Ctrl+0)")

        QShortcut( 'Ctrl+f', self ).activated.connect((lambda: self.find_replace(only_find=True)))            
        QShortcut( 'Ctrl+h', self ).activated.connect((lambda: self.find_replace(only_find=False)))              

        self.uiFrameFileManager.setVisible(False)
        self.frame_2.setVisible(False)
        self.actual_find_box = None


        ## TOGGLE/BURGUER MENU
        ########################################################################
        self.btn_toggle_menu.clicked.connect(lambda: self.toggle_menu(self.uiFrameLeftMenu, 70, 210))
        # self.btn_show_hide_file_manager.clicked.connect(lambda: self.toggleMenu(self.frame_file_manager, 0, 350))
        self.btn_close.clicked.connect(self.close)

        self.VERSION = '2021-03-04'
        # FILTER FOR OPENING/SAVING SCRIPTS AND PROJECTS
        self.filter_script = 'RapitTwo Script (*.par)'

        ################################################################################################################
        # POINTER TO ACTUAL TEXTEDIT, ACTUAL TABS
        ################################################################################################################
        self._actual_text_edit = None
        self.actual_tabs = None

        ################################################################################################################
        # APP SETTINGS CONFIGURATION
        ################################################################################################################
        self.app_settings = AppSettings(self)   
        self.change_theme(self.app_settings.theme)     

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
        self.uiTreeOutline.itemClicked.connect(self.click_on_outline)
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

        ################################################################################################################
        # STACKEDWIDGET CONFIGURATION
        ################################################################################################################
        
        self.stackedWidget.addWidget(self.tabs_splitter)
        self.stackedWidget.addWidget(self.data_manager)
        self.stackedWidget.addWidget(self.app_settings)
        self.stackedWidget.addWidget(self.dashboard)
        self.stackedWidget.setCurrentWidget(self.dashboard)

        self.ui_btn_text_editor.clicked.connect(lambda: self.manage_right_menu(self.tabs_splitter, self.ui_btn_text_editor))
        self.ui_btn_data_manager.clicked.connect(lambda: self.manage_right_menu(self.data_manager, self.ui_btn_data_manager))
        self.ui_btn_home.clicked.connect(lambda: self.manage_right_menu(self.dashboard, self.ui_btn_home))
        self.btn_app_settings.clicked.connect(lambda: self.manage_right_menu(self.app_settings, self.btn_app_settings))

        ################################################################################################################
        # NOTIFICATION WIDGET CONFIGURATION
        ################################################################################################################
        self.notification_widget = NotificationWidget(self)

        self.last_text_4_outline = ""
        self.update_actual_information()

    # @pyqtSlot(list)
    # def get_outline(self, sections: list[str, int]):
    #     # print(sections)
    #     self.uiTreeOutline.clear()
    #     for section in sections:
    #         item = QTreeWidgetItem(self.uiTreeOutline)
    #         item.setData(0, Qt.DisplayRole, section[0])
    #         item.setData(0, Qt.UserRole, section[1])

    #     current_position = self.actual_text_edit.textCursor().position()
    #     for item in self.uiTreeOutline.findItems("*", Qt.MatchWildcard):
    #         if item.data(0, Qt.UserRole) > current_position:
    #             item_above = self.uiTreeOutline.itemAbove(item)
    #             self.uiTreeOutline.setCurrentItem(item_above if item_above else item)
    #             break
    #         else:
    #             item_below = self.uiTreeOutline.itemBelow(item)
    #             self.uiTreeOutline.setCurrentItem(item_below if item_below else item)
    
    
    # def update_outline(self):
    #     self.uiTreeOutline.clear()
    #     if not self.actual_text_edit:
    #         return
        
    #     # EXTRACT CHAPTERS AND TESTCASES FROM TEXT
    #     text = self.actual_text_edit.toPlainText()
    #     # results = re.finditer(r'(?:CHAPTER|TESTCASE)\s*"(.+)"', text)
    #     results = re.finditer(r".*(?:END CHAPTER|CHAPTER|TESTCASE).*", text)
    #     if results:
    #         results = list(results)                        
    #         sections = [(result.group().strip(), result.start()) for result in results if not result.group().strip().startswith("'")]

    #     for section in sections:
    #         item = QTreeWidgetItem(self.uiTreeOutline)
    #         item.setData(0, Qt.DisplayRole, section[0])
    #         item.setData(0, Qt.UserRole, section[1])

    #     current_position = self.actual_text_edit.textCursor().position()
    #     for item in self.uiTreeOutline.findItems("*", Qt.MatchWildcard):
    #         if item.data(0, Qt.UserRole) > current_position:
    #             item_above = self.uiTreeOutline.itemAbove(item)
    #             self.uiTreeOutline.setCurrentItem(item_above if item_above else item)
    #             break
    #         else:
    #             item_below = self.uiTreeOutline.itemBelow(item)
    #             self.uiTreeOutline.setCurrentItem(item_below if item_below else item)


    def line_number_from_position(self, position):
        return self.actual_text_edit.toPlainText()[:position].count("\n") + 1


    def update_outline(self):

        if not self.actual_text_edit:
            self.uiTreeOutline.clear()
            self.last_text_4_outline = ""
            return
        
        if self.actual_text_edit.file_path and Path(self.actual_text_edit.file_path).suffix.lower() != '.par':
            self.uiTreeOutline.clear()
            self.last_text_4_outline = ""
            return
        
        text = self.actual_text_edit.toPlainText()
        
        if text != self.last_text_4_outline:
            self.last_text_4_outline = text
            self.uiTreeOutline.clear()
            chapters_testcases = self.extract_chapters_testcases_from_text(text)
            parent = self.uiTreeOutline
            for section in chapters_testcases:
                text = section[0]
                if re.search(r'^\s*CHAPTER\s+".*"', text, re.IGNORECASE):
                    parent = QTreeWidgetItem(self.uiTreeOutline)
                    parent.setData(0, Qt.DisplayRole, section[0].split('"')[1])
                    parent.setData(0, Qt.UserRole, section[1])
                    parent.setData(0, Qt.DecorationRole, qta.icon('fa5s.book-open', color='#E5A031', scale_factor=1.5))
                    continue
                elif re.search(r'^\s*END CHAPTER\s+', text, re.IGNORECASE):
                    parent = self.uiTreeOutline
                    continue

                elif re.search(r'^\s*TESTCASE\s+".*".*EXPECTEDRESULT', text, re.IGNORECASE):                    
                    item = QTreeWidgetItem(parent)
                    item.setData(0, Qt.DisplayRole, section[0].split('"')[1])
                    item.setData(0, Qt.UserRole, section[1])
                    item.setData(0, Qt.DecorationRole, qta.icon('ph.test-tube-fill', color='#9B59B6', scale_factor=1.5))

            self.update_selected_item_in_outline()
            self.uiTreeOutline.expandAll()


    def update_selected_item_in_outline_by_scrollbar(self, scrollbar_value):
        
        if not self.actual_text_edit: return

        current_position = scrollbar_value + int(self.number_of_visible_lines()/2)
        temp_item = self.uiTreeOutline.topLevelItem(0)
        for item in self.uiTreeOutline.findItems("*", Qt.MatchWildcard | Qt.MatchRecursive):
            if self.line_number_from_position(item.data(0, Qt.UserRole)) > current_position:
                self.uiTreeOutline.setCurrentItem(temp_item)
                break
            
            temp_item = item
            self.uiTreeOutline.setCurrentItem(item)     


    def number_of_visible_lines(self):
        return self.actual_text_edit.height() / self.actual_text_edit.fontMetrics().lineSpacing()

        # doc = popup.document()
        # margin = doc.documentMargin()
        # num_lines = (doc.size().height() - 2*margin)/popup.fontMetrics().height()               



    def update_selected_item_in_outline(self):
        if not self.actual_text_edit: return

        current_position = self.actual_text_edit.textCursor().position()
        temp_item = self.uiTreeOutline.topLevelItem(0)
        for item in self.uiTreeOutline.findItems("*", Qt.MatchWildcard | Qt.MatchRecursive):
            if item.data(0, Qt.UserRole) > current_position:
                self.uiTreeOutline.setCurrentItem(temp_item)
                break
            
            temp_item = item
            self.uiTreeOutline.setCurrentItem(item)
    

    @functools.cache
    def extract_chapters_testcases_from_text(self, text):
        results = re.finditer(r".*(?:END CHAPTER|CHAPTER|TESTCASE).*", text, re.IGNORECASE)
        if results:
            sections = self.extract_sections_from_matches(results)
            return sections
        return []
    

    @functools.cache
    def extract_sections_from_matches(self, matches: list):
        return [(result.group().strip(), result.start()) for result in matches if not result.group().strip().startswith("'")]


    def click_on_outline(self, item):
        self.uiTreeOutline.expandItem(item) if not item.isExpanded() else self.uiTreeOutline.collapseItem(item)
        cursor = self.actual_text_edit.textCursor()
        line =self.line_number_from_position(item.data(0, Qt.UserRole))
        self.smooth_scrolling = SmoothScrolling(self.actual_text_edit)
        self.smooth_scrolling.move_2_line(line-1)
        # cursor.setPosition(len(self.actual_text_edit.toPlainText())-1)
        # self.actual_text_edit.setTextCursor(cursor)
        cursor.setPosition(item.data(0, Qt.UserRole))
        self.actual_text_edit.setTextCursor(cursor)
        self.actual_text_edit.setFocus()





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
            self.uiFrameFileManager.setVisible(False)
            self.frame_2.setVisible(False)
        else:
            self.uiFrameFileManager.setVisible(True)
            self.frame_2.setVisible(True)
            if self.actual_text_edit:
                self.actual_text_edit.setFocus()


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
            self.btn_toggle_menu.setIcon(IconManager().ICON_MENU_CLOSE)
        else:
            self.btn_toggle_menu.setIcon(IconManager().ICON_MENU)




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
            self.actual_text_edit.setFocus()
        self.update_actual_information()



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
            self.actual_text_edit.setFocus()
        self.update_actual_information()


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

                    if file_suffix.lower() == '.py':
                        syntax_highlighter = python_highlighter.PythonHighlighter
                    else:
                        syntax_highlighter = rapit_two_highlighter.RapitTwoHighlighter

                    tab_name = file_path.name
                    self.left_tabs.addTab(TextEdit(self, text, file_path, syntax_highlighter), QIcon(u"ui/icons/16x16/cil-file.png"), tab_name)

                else:
                    opened_files[file_path][1].setCurrentWidget(opened_files[file_path][0])
                    self.actual_tabs = opened_files[file_path][1]
                    self.actual_text_edit = opened_files[file_path][0]
                    self.update_actual_information()
        except Exception as e:
            dialog_message(self, str(e))


    
    def find_reference_in_string(self, string):
        match_list = constants.PATTERN_REQ_REFERENCE.findall(string)
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
                        # file_to_save.close()

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
                    # file_to_save.close()

                    self.update_coverage(self.actual_text_edit.toPlainText(), self.actual_text_edit.original_file_content, path)

                    self.actual_text_edit.original_file_content = text_to_save
                    self.actual_text_edit.file_was_modified = False
                    self.set_actual_tab_icon(False)
                    self.actual_text_edit.file_path = Path(path)
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
        self.left_tabs.addTab(TextEdit(self, "", file_path, rapit_two_highlighter.RapitTwoHighlighter), QIcon(u"ui/icons/16x16/cil-description.png"), tab_name)
        self.actual_text_edit.setFocus()
        tc = self.actual_text_edit.textCursor()
        tc.insertText(text)
        self.actual_text_edit.selectAll()


    def file_lock_unlock(self):
        if self.actual_text_edit:
            try:
                if self.actual_text_edit.is_read_only:
                    os.chmod(self.actual_text_edit.file_path, stat.S_IWRITE)
                    self.actual_text_edit.is_read_only = False
                    self.btn_lock_unlock.setIcon(IconManager().ICON_FILE_UNLOCKED)
                else: 
                    os.chmod(self.actual_text_edit.file_path, stat.S_IREAD)
                    self.actual_text_edit.is_read_only = True
                    self.btn_lock_unlock.setIcon(IconManager().ICON_FILE_LOCKED)
            except TypeError as e:
                dialog_message(self, f"File is not saved! Save the file first. {str(e)}.")
                self.actual_text_edit.setFocus()
                

########################################################################################################################
# FILE MANAGEMENT METHODS:  END
########################################################################################################################



########################################################################################################################
# UPDATES:  START
########################################################################################################################
    def receive_parameters_from_project_manager(self, parameters: dict):
        self.update_project_title(parameters)


    def update_project_title(self, project_params:dict):
        json_project_path = project_params.get("json_project_path")
        is_project_saved = project_params.get("is_project_saved")
        str_modified_status = "" if is_project_saved else "[*Modified]"
        str_project_path = str(json_project_path) if json_project_path else "No Project Loaded"  
        
        # self.setWindowTitle(f"{str_project_path} {str_modified_status} - R2 Script Editor")

        self.label_opened_project.setText(f"{str_project_path} {str_modified_status}") 
        if is_project_saved:
            self.label_opened_project.setStyleSheet("color: rgb(200, 200, 200)")
        else:
            self.label_opened_project.setStyleSheet("color: rgb(250, 50, 50);")
        

    def update_actual_information(self):
        if self.left_tabs.count() == 0 and self.right_tabs.count() == 0:
            self.actual_text_edit = None

        self._update_btn_lock_unlock()
        self._update_tabs_color()
        self._update_script_label()
        # self.update_outline()
        self.update_selected_item_in_outline()


    def _update_btn_lock_unlock(self):
        if self.actual_text_edit is None:
            self.btn_lock_unlock.setVisible(False)
            return
        self.btn_lock_unlock.setVisible(True)
        if self.actual_text_edit.is_read_only:
            self.btn_lock_unlock.setIcon(IconManager().ICON_FILE_LOCKED)
        else:
            self.btn_lock_unlock.setIcon(IconManager().ICON_FILE_UNLOCKED)



    def _update_tabs_color(self):
        # UNDERLINE ACTUAL TAB WITH COLOR
        if self.actual_tabs:
            self.left_tabs.setStyleSheet('QTabBar::tab {border-bottom: 3px solid #31363b}')
            self.right_tabs.setStyleSheet('QTabBar::tab {border-bottom: 3px solid #31363b}')
            self.actual_tabs.setStyleSheet('QTabBar::tab:selected {border-bottom: 3px solid rgb(0, 128, 255)}')        


    def _update_script_label(self):
        self.setWindowTitle(f"Editor - {self.actual_text_edit.file_path}" if self.actual_text_edit else "Editor")
   
    
    def show_notification(self, notification_text):
        self.notification_widget.show_text(notification_text)



########################################################################################################################
# UPDATES:  END
########################################################################################################################

########################################################################################################################
# PROJECT MANAGEMENT METHODS:  START
########################################################################################################################


    def project_new(self):
        # self.window = ProjectConfig(self, is_new_project=True)
        # self.window.show()
        if not project_manager.is_project_saved():
            proceed = QMessageBox.question(self,
                            "R2ScriptEditor",
                            "Current project is not saved.\n\nDo you want to proceed (all changes will be lost)?",
                            QMessageBox.Yes | QMessageBox.No)
            if proceed == QMessageBox.No:
                return        
        project_manager.new_project()

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
        # _show_tray_message("R2ScriptEditor", "R2ScriptEditor is running in background.")

        self.app_settings.save_settings_2_disk()
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



    def change_theme(self, theme):
        reload(config.app_styles)
        styles = config.app_styles.switch_theme(theme.upper())
        app.setStyleSheet(styles)

        







########################################################################################################################
# APP CONFIG:
########################################################################################################################



# def _manage_events_before_close():
#     window.app_settings.save_settings_2_disk()
#     opened_files = window.get_all_opened_files()
#     for path, val in opened_files.items():
#         text_edit = val[0]
#         if text_edit.file_was_modified:
#             close = QMessageBox.question(window,
#                                        "R2ScriptEditor",
#                                        "Some of opened files have been modified.\n\nDo you want to discard changes?",
#                                        QMessageBox.Yes | QMessageBox.No)
#             if close != QMessageBox.Yes:
#                 return False


#     if not project_manager.is_project_saved():
#         close = QMessageBox.question(window,
#                                     "R2ScriptEditor",
#                                     "Current project is not saved.\n\nDo you want to exit (all changes will be lost)?",
#                                     QMessageBox.Yes | QMessageBox.No)
#         if close != QMessageBox.Yes:
#             return False
        
#     return True





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

