from PyQt5.QtWidgets import QWidget, QFileDialog, QListWidget, QInputDialog
from PyQt5.QtCore import Qt, pyqtSignal
from ui.ui_project_config import Ui_Form
from data_manager.condition_nodes import ConditionFileNode
from data_manager.dspace_nodes import DspaceFileNode
from data_manager.a2l_nodes import A2lFileNode
from data_manager.requirement_nodes import RequirementFileNode
import os


def find_files(project_path, target_file):
    """
    Function for browsing specific folder (project_path) and finding cond/dspace/a2l file path
    :param: project_path, target_file
    :return: dictionary {'cond': j:/Projects/.../cond_file.con, 'dspace': ...}
    """
    cond_files = []
    a2l_files = []
    dspace_file = None

    for root, dirs, files in os.walk(project_path):
        for filename in files:
            if target_file == 'cond_file' and filename.lower().endswith(".con"):
                cond_files.append(root + '\\' + filename)

            elif target_file == 'dspace_file' and filename.lower() == 'dspacemapping.py':
                dspace_file = root + '\\' + filename
            elif target_file == 'a2l_file' and filename.lower().endswith(".a2l"):
                a2l_files.append(root + '\\' + filename)


    if target_file == 'cond_file':
        return cond_files
    elif target_file == 'a2l_file':
        return a2l_files
    elif target_file == 'dspace_file':
        return dspace_file



class ProjectConfig(QWidget, Ui_Form):
    """
    This "window" will appear after NEW PROJECT or EDIT PROJECT CONFIGURATION
    """
    # SIGNAL DEFINITION
    send_project_data = pyqtSignal(object)

    def __init__(self, main_window, is_new_project=False):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # POINTER TO MAIN WINDOW AND DATA_CONTROLLER
        # self.main_window = main_window
        self.data_manager = main_window.data_manager
        self.is_new_project = is_new_project

        self.data = {}

        # SIGNAL CONNECTION
        self.send_project_data.connect(self.data_manager.new_project)

        # WINDOW PARAMETERS
        # self.setMinimumSize(600, 280)
        if is_new_project:
            self.label_window_name.setText('Create Project')
        else:
            self.label_window_name.setText('Project Configuration')

        self.stackedWidget.setCurrentWidget(self.page_1)
        
        # CONNECT BUTTONS
        self.btn_project.clicked.connect(lambda x: self.get_folder_path_from_dialog(self.le_project))
        self.btn_cond_file.clicked.connect(lambda x: self.get_file_path_from_dialog(self.lw_cond_file, 'Cond file (*.con)'))
        self.btn_dspace_file.clicked.connect(lambda x: self.get_file_path_from_dialog(self.le_dspace_file, 'Python file (*.py)'))
        self.btn_a2l_file.clicked.connect(lambda x: self.get_file_path_from_dialog(self.lw_a2l_file, 'A2L file (*.a2l)'))

        self.btn_cancel.clicked.connect(self.close_window)
        self.btn_ok.clicked.connect(self.ok_clicked)
        self.btn_next.clicked.connect(self.next_page)
        self.btn_back.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_1))

        self.btn_req_file.clicked.connect(self.add_req_item)

        # FILL LINE EDITS WITH DATA FROM OPENED PROJECT
        if not is_new_project:
            self.fill_line_edits_with_current_project()
            self.stackedWidget.setCurrentWidget(self.page_2)
            self.btn_back.setText('Cancel')
            self.btn_back.clicked.connect(self.close_window)

    def add_req_item(self):
        text, ok = QInputDialog.getText(self, 'Add Location', 'Path::')
        if ok and text != '':
            self.lw_req_file.addItem(text)


    def next_page(self):
        self.stackedWidget.setCurrentWidget(self.page_2)
        project_path = self.le_project.text()
        if project_path != '' and self.is_new_project:
            self.lw_cond_file.addItems(find_files(project_path, 'cond_file'))
            self.le_dspace_file.setText(find_files(project_path, 'dspace_file'))
            self.lw_a2l_file.addItems(find_files(project_path, 'a2l_file'))


    def fill_line_edits_with_current_project(self):
        #  1. iterate through model and get each node object
        for row in range(self.data_manager.ROOT.rowCount()):
            current_item = self.data_manager.ROOT.child(row)
            #  2. get node path and add it to list widget
            if isinstance(current_item, ConditionFileNode):
                self.lw_cond_file.addItem(current_item.path)
            elif isinstance(current_item, A2lFileNode):
                self.lw_a2l_file.addItem(current_item.path)
            elif isinstance(current_item, RequirementFileNode):
                self.lw_req_file.addItem(current_item.path)
            elif isinstance(current_item, DspaceFileNode):
                self.le_dspace_file.setText(current_item.path)



    def get_file_path_from_dialog(self, widget, f):
        path, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select File',
            directory=self.le_project.text(),
            filter=f
        )
        if not path:
            return
        else:
            if isinstance(widget, QListWidget):
                widget.addItem(path)
            else:
                widget.setText(path)

    def get_folder_path_from_dialog(self, widget):
        path = QFileDialog.getExistingDirectory(
            parent=self,
            caption='Select File',
            directory=None
        )
        if not path:
            return
        else:
            widget.setText(path)


    def ok_clicked(self):
        self.send_data_to_controller()
        self.close_window()

    def close_window(self):
        self.close()
        self = None


    def get_data_from_form(self):
        """
        METHOD for reading texts from all line_edits and creating self variables with these values
        :return: None
        """
        disk_project_path = self.le_project.text()

        cond_files = []
        for row in range(self.lw_cond_file.count()):
            cond_files.append(self.lw_cond_file.item(row).text())

        dspace_files = [self.le_dspace_file.text()]

        a2l_files = []
        for row in range(self.lw_a2l_file.count()):
            a2l_files.append(self.lw_a2l_file.item(row).text())

        req = []
        for row in range(self.lw_req_file.count()):
            req.append(self.lw_req_file.item(row).text())

        requirements = [{path: []} for path in req]

        data = {
            'disk_project_path': disk_project_path,
            'Conditions Files': cond_files,
            'DSpace Files': dspace_files,
            'A2L Files': a2l_files,
            'Requirements': requirements
        }

        return data


    def send_data_to_controller(self):
        """
        1. METHOD is triggered after pressing Apply/OK
        2. METHOD emits signal to DATA_CONTROLLER with all gathered data from line_edits in LIST form
        3. as a second parameter sends information if its new or current project
        :return: None
        """
        data = self.get_data_from_form()
        self.send_project_data.emit(data)
        print(data)














