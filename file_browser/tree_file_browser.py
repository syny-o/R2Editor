import os
import shutil
from pathlib import Path

from PyQt5.QtWidgets import QWidget, QTreeView, QFileSystemModel, QVBoxLayout, QLabel, \
    QFileIconProvider, QToolBar, QAction, QFileDialog, QMenu, QInputDialog, QLineEdit, QToolTip, QMessageBox
from PyQt5.QtCore import Qt, QSize, pyqtSlot, pyqtSignal, QSortFilterProxyModel, QDir, QEvent, QPoint
from PyQt5.QtGui import QFont, QIcon, QCursor

from ui.ui_file_system import Ui_Form
from dialogs.form_find_replace import FindAndReplace
from file_browser.pbc_patterns_scripts import patterns
from dialogs.dialog_message import dialog_message




# class IconProvider(QFileIconProvider):
#     def icon(self, file_info):
#         if file_info.isDir():
#             return (QIcon(u"ui/icons/16x16/cil-folder.png"))
#         return QFileIconProvider.icon(self, file_info)




class FileSystemView(QWidget, Ui_Form):

    send_data_to_model = pyqtSignal(dict)

    send_file_path = pyqtSignal(Path)

    def __init__(self, main_window, project_manager):
        super().__init__()
        self.setupUi(self)

        ## HIDE NOT-WORKING UI COMPONENTS
        self.ui_le_filter.setVisible(False)

        self.main_window = main_window
        self.PROJECT_MANAGER = project_manager

        self.send_file_path.connect(main_window.file_open_from_tree)

        self.is_data_manager_connected = False
        self.ui_btn_disconnect_project_folder.setVisible(False)
        self.ui_btn_disconnect_project_folder.clicked.connect(self.disconnect_project_folder)
        

        # self.installEventFilter(self)


        # self._dir_path = QDir.rootPath()
        self._dir_path = r'c:/!!! Projects'

        self.current_path = self._dir_path



        # ################### MODEL #############################
        self.model = QFileSystemModel()
        # self.model.setIconProvider(IconProvider())
        # self.model.setReadOnly(False)

        self.model.setRootPath(self._dir_path)  # directory is just watched for changes

        self.model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot | QDir.Files | QDir.AllEntries)

        self.model.setNameFilters(['*.par','*.a2l', '*.con', '*.py', '*.xml', '*.map', '*.txt'])
        self.model.setNameFilterDisables(False)

        ################## UI TREEVIEW ###########################

        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(self._dir_path))


        # self.tree.clicked.connect(self.update_index)
        self.tree.doubleClicked.connect(self.double_click_on_item)
        self.tree.clicked.connect(self.update_current_path)

        # hide header and all columns except file name
        self.tree.setColumnHidden(1, True)
        self.tree.setColumnHidden(2, True)
        self.tree.setColumnHidden(3, True)

        
        ################## CONTEXT MENU ###########################
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.context_menu)

        ################## FILTER LINE EDIT ###########################

    
    # INTERFACE TO PROJECT MANAGER
    def receive_parameters_from_project_manager(self, parameters: dict):
        if parameters["disk_project_path"]:
            self.receive_project_path(parameters)
        else:
            self.disconnect_project_folder()



    def receive_project_path(self, project_params: dict):
        path = project_params.get("disk_project_path")
        self.ui_btn_disconnect_project_folder.setVisible(True)
        self.ui_btn_disconnect_project_folder.setText(path)
        self.model.setRootPath(path)
        self.tree.setRootIndex(self.model.index(path))
        # self.main_window.data_manager.disk_project_path = path
        self.current_path = path


    def disconnect_project_folder(self):
        self.ui_btn_disconnect_project_folder.setVisible(False)
        self.model.setRootPath(self._dir_path)
        self.tree.setRootIndex(self.model.index(self._dir_path))




    
    
    
    def context_menu(self, point):
        index = self.tree.indexAt(point)
        if not index.isValid():
            return
        file_path = index.model().filePath(index)
        file_suffix = Path(file_path).suffix
        is_directory = index.model().isDir(index)
        menu = QMenu()
        # ACTION OPEN
        if not is_directory:
            action_open = menu.addAction(QIcon(u"ui/icons/16x16/cil-exit-to-app.png"), 'Open')
            action_open.triggered.connect(lambda: self.double_click_on_item(index))
            menu.addSeparator()
        # ACTION NEW FILE
        action_create_file = menu.addAction(QIcon(u"ui/icons/file-new.png"), 'New File')
        action_create_file.triggered.connect(lambda: self.create_file(index))
        # ACTION NEW FOLDER
        action_create_folder = menu.addAction(QIcon(u"ui/icons/folder-new.png"), 'New Folder')
        action_create_folder.triggered.connect(lambda: self.create_folder(index))
        menu.addSeparator()
        # ACTION RENAME
        action_rename = menu.addAction(QIcon(u"ui/icons/16x16/cil-description.png"), 'Rename..')
        action_rename.triggered.connect(lambda: self.rename(index))
        # ACTION DELETE
        action_delete = menu.addAction(QIcon(u"ui/icons/20x20/cil-trash.png"), 'Delete')
        action_delete.triggered.connect(lambda: self.delete_file(index))  
 

        if is_directory:
            menu.addSeparator()
            action_find_replace_in_folder = menu.addAction(QIcon(u"ui/icons/16x16/cil-magnifying-glass.png"), 'Find and Replace in Folder')
            action_find_replace_in_folder.triggered.connect(lambda: self.open_find_replace_dialog(file_path))
            menu.addSeparator()
            # ACTION SET PROJECT LOCATION
            action_set_project_location = menu.addAction(QIcon(u"ui/icons/16x16/cil-layers.png"), 'Set as Project Location')
            action_set_project_location.triggered.connect(lambda: self.disk_project_path_was_changed(file_path))
        elif (file_suffix.lower() in ('.con','.a2l')) or file_path.lower().endswith('dspacemapping.py'): 
            # ACTION ADD TO MODEL
            menu.addSeparator()
            action_add_to_model = menu.addAction(QIcon(u"ui/icons/16x16/cil-dialpad.png"), 'Add to Model')   
            action_add_to_model.triggered.connect(lambda: self.send_file_to_model(file_path))  
        if file_suffix.lower() in ('.par', '.txt') or is_directory:
            # ACTION NORMALISE SCRIPT(S)
            menu.addSeparator()
            action_normalise_file = menu.addAction(QIcon(u"ui/icons/16x16/cil-chart-line.png"), 'Normalise Script(s)')                     
            action_normalise_file.triggered.connect(lambda: self.normalise_script(file_path))

        # ACTION CREATE COPY OF SCRIPT (DUPLICATE)
        if file_suffix.lower() in ('.par', '.txt'):
            action_duplicate_script = menu.addAction(QIcon(u"ui/icons/20x20/cil-copy.png"), 'Create Copy')                     
            action_duplicate_script.triggered.connect(lambda: self.duplicate_script(file_path))            

                
        menu.exec_(QCursor().pos())


    def disk_project_path_was_changed(self, path):
        self.PROJECT_MANAGER.receive_parameters_from_listeners(
            { "disk_project_path": path }
        )



    def send_file_to_model(self, path):
        if not self.is_data_manager_connected:
            self.send_data_to_model.connect(self.main_window.data_manager.receive_data_from_drop_or_file_manager)
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
    ##################################################   FILE / FOLDER MANAGEMENT START  ###################################################################
    ########################################################################################################################################################    

    
    def delete_file(self, index):
        file_path = index.model().filePath(index)
        popup = QMessageBox(self)
        popup.setIcon(QMessageBox.Question)
        popup.setWindowTitle("Delete File")
        popup.setText(f"Do you really want to delete {file_path}?")
        # popup.setInformativeText("Do you want to save your changes?")
        popup.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        popup.setDefaultButton(QMessageBox.Yes)
        answer = popup.exec_()

        if answer == QMessageBox.Yes:        
            self.model.remove(index)


    def create_folder(self, index):
        text, ok = QInputDialog.getText(self, 'Create Folder', 'Name:')
        if ok and text != '':
            self.model.mkdir(index, text)



    def create_file(self, index):
        is_directory = self.model.isDir(index)

        if is_directory:
            file_path = self.model.filePath(index)
            text, ok = QInputDialog.getText(self, 'Create File', 'Name:')
        else:
            file_path = self.model.filePath(index.parent())
            text, ok = QInputDialog.getText(self, 'Create File', 'Name:', QLineEdit.Normal, index.data())   

        if ok and text != '':
            new_file_path = file_path + '/' + text
            if Path(new_file_path).exists():
                dialog_message(self, "File exists!")
                return
            try:
                with open(new_file_path, 'w', encoding='utf8') as new_file:
                    pass
                index = self.model.index(new_file_path)  
                self.tree.setCurrentIndex(index)                
                self.send_file_path.emit(Path(new_file_path))
            except Exception as e:
                dialog_message(self, f"Error: {str(e)}")



    def duplicate_script(self, path): 
        path = Path(path)
        suffix = path.suffix  # e.g. .par
        name = path.name  # file name with suffix e.g. test.par
        parent = path.parent  # all parent folders e.g. C:/temp/
        name_wo_suffix = name.strip(suffix) # just file name e.g. test
        # CREATE DUPLICATED FILE
        new_file_name = name_wo_suffix + " - Copy" + suffix
        new_full_path = parent / new_file_name
        shutil.copyfile(path, new_full_path)
        # SET TREE POSITION TO THIS NEW FILE
        index = self.model.index(str(new_full_path))  
        self.tree.setCurrentIndex(index)
        # OPEN IT IN EDITOR
        self.send_file_path.emit(new_full_path)         
 

    
    def rename(self, index):
        full_path = index.model().filePath(index)
        path_to_folder = '/'.join(full_path.split('/')[:-1])
        # original_folder_name = index.data()
        new_folder_name, ok = QInputDialog.getText(self, 'Rename', 'New Name:', QLineEdit.Normal, index.data())        

        if ok and new_folder_name != '':
            new_path = path_to_folder + '/' + new_folder_name
            try:
                os.rename(full_path, new_path)
                index = self.model.index(str(new_path))  
                self.tree.setCurrentIndex(index)                
            except Exception as e:
                dialog_message(self, str(e))



    ########################################################################################################################################################
    ##################################################   FILE / FOLDER MANAGEMENT END  #####################################################################
    ########################################################################################################################################################                   



    def open_find_replace_dialog(self, folder_path):
        self.win = FindAndReplace(folder_path=folder_path)
        self.win.show()



    def double_click_on_item(self, index):
        file_path = index.model().filePath(index)
        is_directory = index.model().isDir(index)

        if not is_directory:
            self.send_file_path.emit(Path(file_path))



    def update_current_path(self, index):
        file_path = index.model().filePath(index)
        self.current_path = file_path


    def normalise_script(self, file_path):
        import file_browser.form_script_normalisation

        self.form = file_browser.form_script_normalisation.ScriptNormReport(file_path)
        self.form.show()

        
    

