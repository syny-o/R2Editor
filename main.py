import sys, os, stat
from pathlib import Path
from PyQt5.QtWidgets import QSizeGrip
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QTimer, QEvent
from config.font import font
from ui.main_ui import Ui_MainWindow

from dialogs.dialog_message import dialog_message

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QMessageBox, QTabWidget, \
     QAction, QFileDialog, QSplitter, QToolTip, QMenu, QShortcut, QPushButton

from PyQt5.QtCore import Qt, QSize, QFile, QTextStream, pyqtSignal, pyqtSlot, QSettings, QPoint, QRect
from PyQt5.QtGui import QTextCursor, QKeySequence, QIcon, QFontDatabase

from text_editor.text_editor import TextEdit
from text_editor import text_management
from tree_file_browser import FileSystemView
from tabs import Tabs
from data_manager.data_manager import DataManager
from dashboard.dashboard import Dashboard

from dialogs.window_project_config import ProjectConfig
from dialogs.window_settings import AppSettings
from dialogs.form_find_replace import FindAndReplace
from dialogs.dialog_recent_projects import RecentProjects

from components.pyqt_find_text_widget.findTextWidget import FindTextWidget
from components.pyqt_find_text_widget.findReplaceTextWidget import FindReplaceTextWidget

# pyinstaller -w --icon=R2Editor.ico main.py

class MainWindow(QMainWindow, Ui_MainWindow):

    open_project = pyqtSignal(str)
    save_project = pyqtSignal(str)

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.resize(1600, 800)

        self.setWindowIcon(QIcon('R2Editor.ico'))
        self.setWindowTitle("R2Editor")

        self.splitter.setStyleSheet("QSplitterHandle:hover {}  QSplitter::handle:horizontal:hover {background-color:rgb(58,89,245);}")
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        QSizeGrip(self.frame_size_grip)

        ## HIDE NOT-WORKING UI COMPONENTS
        self.btn_project_recent.setVisible(False)
        # self.btn_undo.setVisible(False)
        # self.btn_redo.setVisible(False) 
        self.frame_11.setVisible(False)       
        
        ## CONNECT BUTTONS
        
        self.btn_app_exit.clicked.connect(self.close)

        self.btn_project_open.clicked.connect(self.project_open)
        self.btn_project_new.clicked.connect(self.project_new)
        self.btn_project_save.clicked.connect(self.project_save)
        self.btn_project_save_as.clicked.connect(self.project_save_as)
        self.btn_project_recent.clicked.connect(self.show_recent_projects)


        self.btn_script_new.clicked.connect(self.file_new)
        self.btn_script_new.setShortcut('Ctrl+n')
        self.btn_script_save.clicked.connect(self.file_save)
        self.btn_script_save.setShortcut('Ctrl+s')
        self.btn_script_save_as.clicked.connect(self.file_save_as)
        self.btn_insert_chapter.clicked.connect(self.insert_chapter)
        self.btn_insert_chapter.setShortcut('Ctrl+Shift+c')
        self.btn_insert_testcase.clicked.connect(self.insert_testcase)
        self.btn_insert_testcase.setShortcut('Ctrl+Shift+t')
        self.btn_insert_command.clicked.connect(self.insert_command)
        self.btn_insert_command.setShortcut('Ctrl+Shift+o')
        self.btn_comment_uncomment.clicked.connect(self.comment_uncomment)
        self.btn_comment_uncomment.setShortcut('Ctrl+/')
        self.btn_format_code.clicked.connect(self.format_code)
        self.btn_format_code.setShortcut(('Ctrl+Shift+f'))
        self.btn_lock_unlock.clicked.connect(self.file_lock_unlock)
        self.btn_find_replace.clicked.connect(self.find_replace)
        self.btn_find_replace.setShortcut('Ctrl+f')
        self.btn_undo.clicked.connect(self.perform_undo)
        self.btn_redo.clicked.connect(self.perform_redo)
        self.btn_zoom_in.clicked.connect(self.font_increase)
        self.btn_zoom_in.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Plus))
        self.btn_zoom_out.clicked.connect(self.font_decrease)
        self.btn_zoom_out.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Minus))        
        self.btn_zoom_default.clicked.connect(self.font_reset)
        self.btn_zoom_default.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_0))                

        self.frame_file_manager.setVisible(False)
        self.frame_2.setVisible(False)
        self.actual_find_box = None


        

        def maximize_restore():
            if self.isMaximized():
                self.showNormal()
                self.btn_maximize_restore.setIcon(QIcon(u"ui/icons/16x16/cil-window-maximize.png"))
            else:
                self.showMaximized()
                self.btn_maximize_restore.setIcon(QIcon(u"ui/icons/16x16/cil-window-restore.png"))

        def doubleClickMaximizeRestore(event):
            # IF DOUBLE CLICK CHANGE STATUS
            if event.type() == QEvent.MouseButtonDblClick:
                QTimer.singleShot(50, maximize_restore)                

        def moveWindow(e):
            # Detect if the window is  normal size
            # ###############################################
            if self.isMaximized() == False: #Not maximized
                # Move window only when window is normal size
                # ###############################################
                #if left mouse button is clicked (Only accept left mouse button clicks)
                if e.buttons() == Qt.LeftButton:
                    #Move window
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()

        #######################################################################
        # Add click event/Mouse move event/drag event to the top header to move the window
        #######################################################################
        self.frame_top_btns.mouseMoveEvent = moveWindow
        self.frame_top_btns.mouseDoubleClickEvent = doubleClickMaximizeRestore
        #######################################################################                

        ## TOGGLE/BURGUER MENU
        ########################################################################
        self.btn_toggle_menu.clicked.connect(lambda: self.toggle_menu(self.frame_left_menu, 70, 210))
        # self.btn_show_hide_file_manager.clicked.connect(lambda: self.toggleMenu(self.frame_file_manager, 0, 350))
        self.btn_close.clicked.connect(self.close)
        self.btn_maximize_restore.clicked.connect(maximize_restore)
        self.btn_minimize.clicked.connect(lambda: self.showMinimized())








        self.VERSION = '2021-03-04'
        # FILTER FOR OPENING/SAVING SCRIPTS AND PROJECTS
        self.filter_script = 'RapitTwo Script (*.par)'
        self.filter_project = 'RapitTwo Editor Project (*.json)'

        ################################################################################################################
        # POINTER TO ACTUAL TEXTEDIT, ACTUAL TABS
        ################################################################################################################
        self.actual_text_edit = None
        self.actual_tabs = None

        self.opened_project_path = None

        ################################################################################################################
        # TREE FILE BROWSER CONFIGURATION
        ################################################################################################################
        self.tree_file_browser = FileSystemView(self)
        self.verticalLayout_7.addWidget(self.tree_file_browser)


        ################################################################################################################
        # DATA MANAGER CONFIGURATION
        ################################################################################################################
        self.data_manager = DataManager(self)
        self.open_project.connect(self.data_manager.open_project)
        self.save_project.connect(self.data_manager.save_project)


        ################################################################################################################
        # DASHBOARD CONFIGURATION
        ################################################################################################################
        self.dashboard = Dashboard(self)

        ################################################################################################################
        # TABS CONFIGURATION
        ################################################################################################################
        self.left_tabs = Tabs(self, True, 'LEFT_TABS')
        self.left_tabs.tabCloseRequested.connect(self.left_tab_close_request)
        self.left_tabs.currentChanged.connect(self.left_tab_was_changed)
        self.left_tabs.tabBarClicked.connect(self.left_tab_was_changed)

        self.right_tabs = Tabs(self, False, 'RIGHT_TABS')
        self.right_tabs.tabCloseRequested.connect(self.right_tab_close_request)
        self.right_tabs.currentChanged.connect(self.right_tab_was_changed)
        self.right_tabs.tabBarClicked.connect(self.right_tab_was_changed)

        self.tabs_splitter = QSplitter()
        self.tabs_splitter.addWidget(self.left_tabs)
        self.tabs_splitter.addWidget(self.right_tabs)
        self.tabs_splitter.setStretchFactor(2, 1)
        self.tabs_splitter.setStyleSheet('background-color: rgb(33, 37, 43); border:None;')

        ################################################################################################################
        # APP SETTINGS CONFIGURATION
        ################################################################################################################
        self.app_settings = AppSettings(self)

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


    def keyPressEvent(self, e) -> None:
        if e.key() == Qt.Key_Escape:
            self.find_replace(False)
            self.btn_find_replace.setChecked(False)
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
    def mousePressEvent(self, event):
        # ###############################################
        # Get the current position of the mouse
        self.clickPosition = event.globalPos()
        # For moving window
    #######################################################################
    #######################################################################

    def toggle_menu(self, toggled_frame, min_width, max_width):
        # GET ACTUAL WIDTH
        width = toggled_frame.width()
        # SET DESIRED WIDTH
        extended_width = max_width if width == min_width else min_width
        # ANIMATION
        self.animation = QPropertyAnimation(toggled_frame, b"minimumWidth")
        self.animation.setDuration(400)
        self.animation.setStartValue(width)
        self.animation.setEndValue(extended_width)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()


    def update_actual_information(self):
        self.update_title()
        if self.actual_text_edit:
            self.btn_lock_unlock.setChecked(self.actual_text_edit.is_read_only)
        else:
           self.btn_lock_unlock.setChecked(False) 


    def update_title(self):
        # SET WINDOW TITLE SAME AS ACTUAL FILE PATH
        self.setWindowTitle(
            '{0} - R2 Script Editor'.format(self.opened_project_path) if self.opened_project_path else 'Unsaved Project')
        self.label_opened_project.setText(str(self.opened_project_path) if self.opened_project_path else 'No Project')

        # SET STATUS BAR LABEL SAME AS ACTUAL FILE PATH
        self.label_actual_script_path.setText(self.actual_text_edit.file_path if self.actual_text_edit else '')

        # UNDERLINE ACTUAL TAB WITH COLOR
        if self.actual_tabs:
            self.left_tabs.setStyleSheet('QTabBar::tab {border-bottom: 3px solid #31363b}')
            self.right_tabs.setStyleSheet('QTabBar::tab {border-bottom: 3px solid #31363b}')
            self.actual_tabs.setStyleSheet(' QTabBar::tab:selected {border-bottom: 3px solid rgb(0, 128, 255)}')
   
    
    def show_tooltip(self, tooltip_text):
        # tooltip_text = tooltip_text.replace(" ","&nbsp;")
        # formated_tooltip_text = f'<html><center><img src="ui/icons/info.png"><br><div style="color: white;">{tooltip_text}</div></center></html>'
        # pos_x, pos_y = self.pos().x(), self.pos().y()
        QToolTip.showText(QPoint(self.width()-len(tooltip_text), self.height()-50), tooltip_text)






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



    def file_open_from_tree(self, file_path):
        file_suffix = Path(file_path).suffix
        opened_files = self.get_all_opened_files()
        if file_suffix.lower() in ('.par', '.py', '.con', '.xml', '.a2l', '.map'):
            if file_path not in opened_files:
                with open(file_path, 'r') as file_to_open:
                    text = file_to_open.read()
                    file_to_open.close()

                tab_name = file_path.split('/')[-1]
                self.left_tabs.addTab(TextEdit(self, text, file_path), QIcon(u"ui/icons/16x16/cil-file.png"), tab_name)

            else:
                opened_files[file_path][1].setCurrentWidget(opened_files[file_path][0])
                self.actual_tabs = opened_files[file_path][1]
                self.actual_text_edit = opened_files[file_path][0]
                self.update_actual_information()




    def file_save(self):
        if self.actual_text_edit:
            self.format_code()
            if self.actual_text_edit.file_path == None:
                self.file_save_as()
            else:
                try:
                    text_to_save = self.actual_text_edit.toPlainText()
                    with open(self.actual_text_edit.file_path, 'w') as file_to_save:
                        file_to_save.write(text_to_save)
                        file_to_save.close()
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
        text = ''
        file_path = None
        tab_name = 'Untitled'
        self.left_tabs.addTab(TextEdit(self, text, file_path), QIcon(u"ui/icons/16x16/cil-file.png"), tab_name)
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
    def project_new(self):
        self.opened_project_path = None
        self.window = ProjectConfig(self, is_new_project=True)
        self.window.show()

    def project_save(self):        
        path = self.opened_project_path
        if not path:
            self.project_save_as()
        else:
            try:
                # REQUEST FOR DATA_CONTROLLER
                self.save_project.emit(path)
            except Exception as exception_to_show:
                dialog_message(self, str(exception_to_show))

    def project_save_as(self):        
        path, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption='Save Project',
            directory='.//Projects',
            filter=self.filter_project
        )
        if not path:
            return
        else:
            try:
                # REQUEST FOR DATA_CONTROLLER
                self.save_project.emit(path)
                self.opened_project_path = path
                self.update_title()
            except Exception as exception_to_show:
                dialog_message(self, str(exception_to_show))


    def project_open(self):
        path, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption='Open Project',
            directory='.//Projects',
            filter=self.filter_project
        )

        if not path:
            return
        else:
            try:
                # REQUEST FOR DATA_CONTROLLER
                self.open_project.emit(path)
                self.opened_project_path = path
                self.update_title()
            except Exception as my_exception:
                dialog_message(self, str(my_exception))




    def show_recent_projects(self):
        self.window = RecentProjects(self)
        self.window.show()                


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

    def find_replace(self, is_checked):
        if not self.actual_text_edit:
            self.btn_find_replace.setChecked(False)
            return
        


        if self.actual_find_box:
                self.ui_hLayout_findReplace.removeWidget(self.actual_find_box) 

        if is_checked:   
            # new_find_box = FindTextWidget(self.actual_text_edit)
            new_find_box = FindReplaceTextWidget(self.actual_text_edit)
            self.ui_hLayout_findReplace.addWidget(new_find_box)
            new_find_box.setFocus()
            self.actual_find_box = new_find_box
            # self.actual_text_edit.setStyleSheet("selection-background-color: red;")
        




    def find_text(self, text_to_find):
        if self.actual_text_edit:
            tc = self.actual_text_edit.textCursor()
            self.find_from_index = tc.position()
            text = self.actual_text_edit.toPlainText()
            index = text.lower().find(text_to_find.lower(), self.find_from_index)

            if index == -1:
                self.find_from_index = 0
                index = text.lower().find(text_to_find.lower(), self.find_from_index)


            if index != -1:                
                tc.setPosition(index)
                tc.setPosition(index + len(text_to_find), QTextCursor.KeepAnchor)
                self.actual_text_edit.setTextCursor(tc)
                # self.find_from_index = index
            else:
                dialog_message(self, '\nYou have reached end of Document!', 'Find Text')


                


    def format_code(self):
        from importlib import reload
        reload(text_management)
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

        if not self.data_manager.is_project_saved:
            close = QMessageBox.question(self,
                                        "R2ScriptEditor",
                                        "Current project is not saved.\n\nDo you want to discard changes?",
                                        QMessageBox.Yes | QMessageBox.No)
            if close == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()





if __name__ == "__main__":
    app = QApplication(sys.argv)

    # app.setFont(font)

    QFontDatabase.addApplicationFont('ui/fonts/segoeui.ttf')
    QFontDatabase.addApplicationFont('ui/fonts/segoeuib.ttf')
    file = QFile("ui/dark.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())


    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

