from pathlib import Path

from PyQt5.QtWidgets import QWidget, QFileSystemModel, QShortcut
from PyQt5.QtCore import Qt, QSize, pyqtSlot, pyqtSignal, QDir, QTimer
from PyQt5.QtGui import QFont, QIcon

from ui.file_system_ui import Ui_Form
from file_browser.context_menu import FileBrowserContextMenu
from file_browser.form_find_replace import FindAndReplace
from file_browser.file_browser_actions import FileBrowserActions
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
        self.actions = FileBrowserActions(self)
        self.context_menu = FileBrowserContextMenu(self)

        self.send_file_path.connect(main_window.document_actions.open_path)

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
        QShortcut('Del', self.tree).activated.connect(self.actions.delete)
        QShortcut('F2', self.tree).activated.connect(self.actions.rename)
        self.tree.setColumnHidden(1, True)
        self.tree.setColumnHidden(2, True)
        self.tree.setColumnHidden(3, True)          
        
        ################## CONTEXT MENU ###########################
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.context_menu.show)





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

        if path.lower().endswith('.con') or path.lower().endswith('.con.xml'):
            data.update({'Conditions Files': [path]})            

        elif path.lower().endswith('.py') and 'dspacemapping' in path.lower():
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


    ########################################################################################################################################################
    ##################################################   FILE / FOLDER MANAGEMENT START  ###################################################################
    ########################################################################################################################################################    


    def refresh_root_path(self):
        path = self.model.rootPath()
        self.model.setRootPath(self.current_path)
        self.model.setRootPath(path)
        self.tree.setRootIndex(self.model.index(self.model.rootPath()))    
        self.model.setRootPath(self.model.rootPath())
        self.tree.setModel(self.model)
        self.tree.sortByColumn(0, Qt.AscendingOrder)



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
