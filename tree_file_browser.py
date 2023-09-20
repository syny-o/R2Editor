from PyQt5.QtWidgets import QWidget, QTreeView, QFileSystemModel, QVBoxLayout, QLabel, \
    QFileIconProvider, QToolBar, QAction, QFileDialog, QMenu, QInputDialog, QLineEdit, QToolTip
from PyQt5.QtCore import Qt, QSize, pyqtSlot, pyqtSignal, QSortFilterProxyModel, QDir, QEvent, QPoint
from PyQt5.QtGui import QFont, QIcon, QCursor
from pathlib import Path

from ui.ui_file_system import Ui_Form
import os, stat, re
from dialogs.form_find_replace import FindAndReplace
from vda_normaliser.vda_normaliser import normalise_file




class IconProvider(QFileIconProvider):
    def icon(self, file_info):
        if file_info.isDir():
            return (QIcon(u"ui/icons/16x16/cil-folder.png"))
        return QFileIconProvider.icon(self, file_info)




class FileSystemView(QWidget, Ui_Form):

    send_data_to_model = pyqtSignal(dict)

    send_file_path = pyqtSignal(str)

    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)

        ## HIDE NOT-WORKING UI COMPONENTS
        self.ui_le_filter.setVisible(False)

        self.main_window = main_window

        self.send_file_path.connect(main_window.file_open_from_tree)

        self.is_data_manager_connected = False
        self.ui_btn_disconnect_project_folder.setVisible(False)
        self.ui_btn_disconnect_project_folder.clicked.connect(self.disconnect_project_folder)
        

        # self.installEventFilter(self)


        # self._dir_path = QDir.rootPath()
        self._dir_path = r'j:/!!! Projects'

        self.current_path = self._dir_path



        # ################### MODEL #############################
        self.model = QFileSystemModel()
        # self.model.setIconProvider(IconProvider())
        # self.model.setReadOnly(False)

        self.model.setRootPath(self._dir_path)  # directory is just watched for changes

        self.model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot | QDir.Files | QDir.AllEntries)

        self.model.setNameFilters(['*.par','*.a2l', '*.con', '*.py', '*.xml', '*.map'])
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
        
    @pyqtSlot(str)
    def receive_project_path(self, path):
        self.ui_btn_disconnect_project_folder.setVisible(True)
        self.ui_btn_disconnect_project_folder.setText(path)
        self.model.setRootPath(path)
        self.tree.setRootIndex(self.model.index(path))
        self.main_window.data_manager.disk_project_path = path
        self.current_path = path


    def disconnect_project_folder(self):
        self.ui_btn_disconnect_project_folder.setVisible(False)
        self.model.setRootPath(self._dir_path)
        self.tree.setRootIndex(self.model.index(self._dir_path))
        self.main_window.data_manager.disk_project_path = None



    
    
    
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
        action_rename.triggered.connect(lambda: self.rename_folder(index))
        # ACTION DELETE
        action_delete = menu.addAction(QIcon(u"ui/icons/20x20/cil-trash.png"), 'Delete')
        action_delete.triggered.connect(lambda: self.model.remove(index))   

        if is_directory:
            menu.addSeparator()
            action_find_replace_in_folder = menu.addAction(QIcon(u"ui/icons/16x16/cil-magnifying-glass.png"), 'Find and Replace in Folder')
            action_find_replace_in_folder.triggered.connect(lambda: self.open_find_replace_dialog(file_path))
            menu.addSeparator()
            # ACTION SET PROJECT LOCATION
            action_set_project_location = menu.addAction(QIcon(u"ui/icons/16x16/cil-layers.png"), 'Set as Project Location')
            action_set_project_location.triggered.connect(lambda: self.receive_project_path(file_path))
        elif (file_suffix.lower() in ('.con','.a2l')) or file_path.lower().endswith('dspacemapping.py'): 
            # ACTION ADD TO MODEL
            menu.addSeparator()
            action_add_to_model = menu.addAction(QIcon(u"ui/icons/16x16/cil-dialpad.png"), 'Add to Model')   
            action_add_to_model.triggered.connect(lambda: self.send_file_to_model(file_path))  
        # if file_suffix.lower() in ('.par', '.txt'):
        #     menu.addSeparator()
        #     action_normalise_file = menu.addAction(QIcon(u"ui/icons/16x16/cil-chart-line.png"), 'Normalise Script')                     
        #     action_normalise_file.triggered.connect(lambda: normalise_file(file_path))
                
        menu.exec_(QCursor().pos())



    def send_file_to_model(self, path):
        if not self.is_data_manager_connected:
            self.send_data_to_model.connect(self.main_window.data_manager.receive_data_from_drop_or_file_manager)
            self.is_data_manager_connected = True


        window_position = self.main_window.pos()
        window_height = self.main_window.height()
        window_width = self.main_window.width()

        tooltip_position = window_position

        tooltip_position.setX(tooltip_position.x() + 10)
        tooltip_position.setY(tooltip_position.y() + window_height -200)
        tooltip_width = len(path)*10
        tooltip_content = f"""
                <html>
                <table height="30" width="{tooltip_width}">
                <tr>
                <center><img src="ui/icons/info.png"</center>
                </tr>
                <tr>
                    <td><center>File <font color=lightblue>{path}</font> has been sent to model.</center></td>
                </tr>
                </table>
                </html>
        """    

        # self.main_window.show_tooltip(tooltip_content)
        QToolTip.showText(tooltip_position, tooltip_content)

        data = {}

        if path.lower().endswith('.con'):
            data.update({'Conditions Files': [path]})            

        elif path.lower().endswith('dspacemapping.py'):
            data.update({'DSpace Files': [path]})


        elif path.lower().endswith('.a2l'):
            data.update({'A2L Files': [path]})
        
        self.send_data_to_model.emit(data)

    
    def create_folder(self, index):
        text, ok = QInputDialog.getText(self, 'Create Folder', 'Name:')
        if ok and text != '':
            self.model.mkdir(index, text)

    def create_file(self, index):
        is_directory = self.model.isDir(index)

        if is_directory:
            file_path = self.model.filePath(index)
            text, ok = QInputDialog.getText(self, 'Create File', 'Name:')
            if ok and text != '':
                new_file_path = file_path + '/' + text + '.par'
                if Path(new_file_path).exists():
                    print('File exists')
                    return
                try:
                    with open(new_file_path, 'w', encoding='utf8') as new_file:
                        pass
                    self.send_file_path.emit(new_file_path)
                except Exception as e:
                    print(str(e))

        else:
            file_path = self.model.filePath(index.parent())
            text, ok = QInputDialog.getText(self, 'Create File', 'Name:', QLineEdit.Normal, index.data().strip(".par"))
            if ok and text != '':
                new_file_path = file_path + '/' + text + '.par'
                if Path(new_file_path).exists():
                    print('File exists')
                    return
                try:
                    with open(new_file_path, 'w', encoding='utf8') as new_file:
                        pass
                    self.send_file_path.emit(new_file_path)
                except Exception as e:
                    print(str(e))

    
    def rename_folder(self, index):
        full_path = index.model().filePath(index)
        path_to_folder = '/'.join(full_path.split('/')[:-1])
        original_folder_name = index.data()
        new_folder_name, ok = QInputDialog.getText(self, 'Rename', 'New Name:', QLineEdit.Normal, index.data())        

        if ok and new_folder_name != '':
            try:
                os.rename(full_path, path_to_folder + '/' + new_folder_name)
            except Exception as e:
                print(e)



    def open_find_replace_dialog(self, folder_path):
        self.win = FindAndReplace(folder_path=folder_path)
        self.win.show()




    def double_click_on_item(self, index):
        file_path = index.model().filePath(index)
        is_directory = index.model().isDir(index)

        if not is_directory:
            self.send_file_path.emit(file_path)

    def update_current_path(self, index):
        file_path = index.model().filePath(index)
        self.current_path = file_path


    def normalise_script(self):
        pass

