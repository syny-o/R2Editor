import os
import shutil
from pathlib import Path

from PyQt5.QtWidgets import QWidget, QFileSystemModel, QMenu, QInputDialog, QLineEdit, QMessageBox, QShortcut
from PyQt5.QtCore import Qt, QSize, pyqtSlot, pyqtSignal, QDir
from PyQt5.QtGui import QFont, QIcon, QCursor

from ui.file_system_ui import Ui_Form
from file_browser.form_find_replace import FindAndReplace
from dialogs.dialog_message import dialog_message

from components.widgets.widgets_pointing_hand import TreeViewPointingHand
from config.icon_manager import IconManager

class FileSystemView(QWidget, Ui_Form):

    send_data_to_model = pyqtSignal(dict)
    send_file_path = pyqtSignal(Path)

    def __init__(self, main_window, project_manager):
        super().__init__()
        self.setupUi(self)
        self.uiBtnDisconnectProjectFolder.setIcon(IconManager().ICON_DISCONNECT_FOLDER)

        self.tree = TreeViewPointingHand()
        self.tree.setHeaderHidden(True)
        self.uiLayoutTree.addWidget(self.tree)

        self.MAIN = main_window
        self.PROJECT_MANAGER = project_manager

        self.send_file_path.connect(main_window.file_open_from_tree)

        self.is_data_manager_connected = False
        self.uiBtnDisconnectProjectFolder.setVisible(False)
        self.uiBtnDisconnectProjectFolder.clicked.connect(self._user_disconnected_path)
    
        # self._dir_path = QDir.rootPath()
        self._dir_path = r'c:/!!! Projects'
        self.current_path = self._dir_path

        # ################### MODEL #############################
        self.model = QFileSystemModel()
        self.model.setRootPath(self._dir_path)  # directory is just watched for changes
        self.model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot | QDir.Files | QDir.AllEntries)
        self.model.setNameFilters(['*.par','*.a2l', '*.con', '*.py', '*.xml', '*.map', '*.txt'])
        self.model.setNameFilterDisables(False)

        ################## UI TREEVIEW ###########################
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(self._dir_path))
        self.tree.doubleClicked.connect(self._double_click_on_item)
        self.tree.clicked.connect(self._update_current_path)
        QShortcut( 'Del', self.tree ).activated.connect(self._delete_file)
        QShortcut( 'F2', self.tree ).activated.connect(self._rename) 
        self.tree.setColumnHidden(1, True)
        self.tree.setColumnHidden(2, True)
        self.tree.setColumnHidden(3, True)          
        
        ################## CONTEXT MENU ###########################
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._context_menu)




    ########################################################################################################################################################
    # @INTERFACE WITH PROJECT MANAGER
    ########################################################################################################################################################
    def receive_parameters_from_project_manager(self, parameters: dict):
        path = parameters.get("disk_project_path")
        if path is not None:
            self._connect_project_folder(path)
        else:
            self._disconnect_project_folder()


    def _send_project_path_2_project_manager(self, path):
        self.PROJECT_MANAGER.receive_parameters_from_listeners(
            { "disk_project_path": path }
        )


    def _send_project_not_saved_2_project_manager(self):
        self.PROJECT_MANAGER.receive_parameters_from_listeners(
            { "is_project_saved": False }
        )  


    ########################################################################################################################################################
    # @INTERFACE WITH DATA MANAGER
    ########################################################################################################################################################   
    def _send_file_to_model(self, path):
        if not self.is_data_manager_connected:
            self.send_data_to_model.connect(self.MAIN.data_manager.receive_data_from_drop_or_file_manager)
            self.is_data_manager_connected = True

        data = {}

        if path.lower().endswith('.con'):
            data.update({'Conditions Files': [path]})            

        elif path.lower().endswith('dspacemapping.py'):
            data.update({'DSpace Files': [path]})

        elif path.lower().endswith('.a2l'):
            data.update({'A2L Files': [path]})
        
        self.send_data_to_model.emit(data)        

    ########################################################################################################################################################        
    ########################################################################################################################################################   





    def _connect_project_folder(self, path: str):        
        self.uiBtnDisconnectProjectFolder.setVisible(True)
        self.uiLabelProjectFolder.setText(path)
        self.model.setRootPath(path)
        self.tree.setRootIndex(self.model.index(path))
        self.current_path = path



    def _disconnect_project_folder(self):
        self.uiBtnDisconnectProjectFolder.setVisible(False)
        self.uiLabelProjectFolder.setText("No Project Folder")
        self.model.setRootPath(self._dir_path)
        self.tree.setRootIndex(self.model.index(self._dir_path))
        self.current_path = None



    def _user_disconnected_path(self):
        self._disconnect_project_folder()
        self._send_project_path_2_project_manager(path=None)    
        self._send_project_not_saved_2_project_manager()


    def _user_connected_path(self, path):
        self._connect_project_folder(path)
        self._send_project_path_2_project_manager(path)
        self._send_project_not_saved_2_project_manager()


    def _double_click_on_item(self, index):
        file_path = index.model().filePath(index)
        is_directory = index.model().isDir(index)

        if not is_directory:
            self.send_file_path.emit(Path(file_path))



    def _update_current_path(self, index):
        file_path = index.model().filePath(index)
        self.current_path = file_path

        self._double_click_on_item(index)
        self.tree.setExpanded(index, False) if self.tree.isExpanded(index) else self.tree.setExpanded(index, True)


    
    


    ########################################################################################################################################################
    ##################################################   CONTEXT MENU START  ###################################################################
    ########################################################################################################################################################    


    def _context_menu(self, point):
        index = self.tree.indexAt(point)
        if not index.isValid():
            return
        file_path = index.model().filePath(index)
        file_suffix = Path(file_path).suffix
        is_directory = index.model().isDir(index)
        menu = QMenu()
        # # ACTION NEW FILE
        # action_create_file = menu.addAction(QIcon(u"ui/icons/file-new.png"), 'New File')
        # action_create_file.triggered.connect(lambda: self.create_file(index))
        # ACTION NEW FOLDER
        if is_directory:
            action_create_folder = menu.addAction(QIcon(u"ui/icons/folder-new.png"), 'New Folder')
            action_create_folder.triggered.connect(lambda: self._create_folder(index))
            menu.addSeparator()
        # ACTION RENAME
        action_rename = menu.addAction(QIcon(u"ui/icons/16x16/cil-description.png"), 'Rename..')
        action_rename.triggered.connect(self._rename)
        action_rename.setShortcut('F2')

 

        if is_directory:
            menu.addSeparator()
            action_find_replace_in_folder = menu.addAction(QIcon(u"ui/icons/16x16/cil-magnifying-glass.png"), 'Find and Replace in Folder')
            action_find_replace_in_folder.triggered.connect(lambda: self._open_find_replace_dialog(file_path))
            menu.addSeparator()
            # ACTION SET PROJECT LOCATION
            action_set_project_location = menu.addAction(QIcon(u"ui/icons/16x16/cil-layers.png"), 'Set as Project Location')
            action_set_project_location.triggered.connect(lambda: self._user_connected_path(file_path))
        

        # ACTION CREATE COPY OF SCRIPT (DUPLICATE)
        if file_suffix.lower() in ('.par', '.txt'):
            action_duplicate_script = menu.addAction(QIcon(u"ui/icons/20x20/cil-copy.png"), 'Create Copy')                     
            action_duplicate_script.triggered.connect(lambda: self._duplicate_script(file_path)) 

        if (file_suffix.lower() in ('.con','.a2l')) or file_path.lower().endswith('dspacemapping.py'): 
            # ACTION ADD TO MODEL
            menu.addSeparator()
            action_add_to_model = menu.addAction(QIcon(u"ui/icons/16x16/cil-dialpad.png"), 'Add to Model')   
            action_add_to_model.triggered.connect(lambda: self._send_file_to_model(file_path))                        

        if file_suffix.lower() in ('.par', '.txt') or is_directory:
            # ACTION NORMALISE SCRIPT(S)
            menu.addSeparator()
            action_normalise_file = menu.addAction(QIcon(u"ui/icons/16x16/cil-chart-line.png"), 'Normalise Script(s)')                     
            action_normalise_file.triggered.connect(lambda: self._normalise_script(file_path))                

        # ACTION DELETE
        menu.addSeparator()
        action_delete = menu.addAction(QIcon(u"ui/icons/20x20/cil-trash.png"), 'Delete')
        action_delete.triggered.connect(self._delete_file)  
        action_delete.setShortcut('Del')    

        menu.exec_(QCursor().pos())


    ########################################################################################################################################################
    ##################################################   FILE / FOLDER MANAGEMENT START  ###################################################################
    ########################################################################################################################################################    

    
    def _delete_file(self):
        index = self.tree.currentIndex()
        file_path = index.model().filePath(index)
        popup = QMessageBox(self)
        popup.setIcon(QMessageBox.Question)
        popup.setWindowTitle("Delete File")
        popup.setText(f"Do you really want to delete {file_path}?")
        # popup.setInformativeText("Do you want to save your changes?")
        popup.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        popup.setDefaultButton(QMessageBox.Yes)
        answer = popup.exec_()


        opened_files = self.MAIN.get_all_opened_files()  # get dict {Path(str): (QTextEdit, QTabWidget)}
        if (key := Path(file_path)) in opened_files:
            my_text_edit, my_tabs = opened_files[key]
            tab_index = my_tabs.indexOf(my_text_edit)
            my_tabs.removeTab(tab_index)        

        if answer == QMessageBox.Yes:  
            try:      
                self.model.remove(index)
            except Exception as e:
                dialog_message(self, str(e))


    def _create_folder(self, index):
        text, ok = QInputDialog.getText(self, 'Create Folder', 'Name:')
        if ok and text != '':
            try:
                self.model.mkdir(index, text)
            except Exception as e:
                dialog_message(self, str(e))




    def _duplicate_script(self, path): 
        path = Path(path)
        suffix = path.suffix  # e.g. .par
        name = path.name  # file name with suffix e.g. test.par
        parent = path.parent  # all parent folders e.g. C:/temp/
        name_wo_suffix = name.strip(suffix) # just file name e.g. test
        # CREATE DUPLICATED FILE
        new_file_name = name_wo_suffix + " - Copy" + suffix
        new_full_path = parent / new_file_name
        try:
            shutil.copyfile(path, new_full_path)
            # SET TREE POSITION TO THIS NEW FILE
            index = self.model.index(str(new_full_path))  
            self.tree.setCurrentIndex(index)
            # OPEN IT IN EDITOR
            self.send_file_path.emit(new_full_path) 
        except Exception as e:
            dialog_message(self, str(e))        
 

    
    def _rename(self):
        index = self.tree.currentIndex()
        path = Path(index.model().filePath(index))

        new_name, ok = QInputDialog.getText(self, 'Rename', 'New Name:', QLineEdit.Normal, str(path.stem))      

        if ok and new_name.strip() != '':
            new_path = path.with_stem(new_name)
            try:
                os.rename(path, new_path)
                index = self.model.index(str(new_path))  
                self.tree.setCurrentIndex(index)
                # self.model.setReadOnly(False)
                # self.model.setData(index, str(new_name) + path.suffix)
                # self.model.setReadOnly(True)
                opened_files = self.MAIN.get_all_opened_files()  # get dict {Path(str): (QTextEdit, QTabWidget)}
                if (key := Path(path)) in opened_files:
                    my_text_edit, my_tabs = opened_files[key]
                    tab_index = my_tabs.indexOf(my_text_edit)
                    my_text_edit.file_path = Path(new_path)
                    my_tabs.setTabText(tab_index, Path(new_path).name)


            except Exception as e:
                dialog_message(self, str(e))



    # def create_file(self, index):
    #     is_directory = self.model.isDir(index)

    #     if is_directory:
    #         file_path = self.model.filePath(index)
    #         text, ok = QInputDialog.getText(self, 'Create File', 'Name:')
    #     else:
    #         file_path = self.model.filePath(index.parent())
    #         text, ok = QInputDialog.getText(self, 'Create File', 'Name:', QLineEdit.Normal, index.data())   

    #     if ok and text != '':
    #         new_file_path = file_path + '/' + text
    #         if Path(new_file_path).exists():
    #             dialog_message(self, "File exists!")
    #             return
    #         try:
    #             with open(new_file_path, 'w', encoding='utf8') as new_file:
    #                 pass
    #             index = self.model.index(new_file_path)  
    #             self.tree.setCurrentIndex(index)                
    #             self.send_file_path.emit(Path(new_file_path))
    #         except Exception as e:
    #             dialog_message(self, f"Error: {str(e)}")                



    ########################################################################################################################################################
    ##################################################   FILE / FOLDER MANAGEMENT END  #####################################################################
    ########################################################################################################################################################                   



    def _open_find_replace_dialog(self, folder_path):
        self.win = FindAndReplace(folder_path=folder_path)
        self.win.show()


    def _normalise_script(self, file_path):
        import file_browser.form_script_normalisation

        self.form = file_browser.form_script_normalisation.ScriptNormReport(file_path)
        self.form.show()

        
    