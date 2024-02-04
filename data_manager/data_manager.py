from importlib import reload
from pathlib import Path
from data_manager.nodes import a2l_nodes, dspace_nodes, requirement_module
from ui.model_editor_ui import Ui_Form
import json, re, os
from PyQt5.QtWidgets import QWidget, QFileDialog, QInputDialog, QLabel, QAction, QLineEdit, QShortcut, QMessageBox, QListWidgetItem
from PyQt5.QtGui import QIcon, QCursor, QKeySequence, QStandardItemModel, QColor, QPainter
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QObject, QRunnable, QThreadPool, QPropertyAnimation, QEasingCurve
from data_manager.nodes.condition_nodes import ConditionFileNode, ConditionNode, ValueNode, TestStepNode
from data_manager.nodes.dspace_nodes import DspaceFileNode, DspaceDefinitionNode, DspaceVariableNode
from data_manager.nodes.a2l_nodes import A2lFileNode, A2lNode
from data_manager.nodes import condition_nodes
from data_manager.nodes.requirement_module import RequirementModule, RequirementNode
from data_manager.forms.form_add_module import FormAddModule
from components.progress_bar.widget_modern_progress_bar import ModernProgressBar
from components.template_test_case import TemplateTestCase
from dialogs.dialog_message import dialog_message
from doors.doors_connection import DoorsConnection
import data_manager.forms.form_a2l_norm_report   
import data_manager.forms.form_validate_html_report
from data_manager import model_manager
from data_manager.forms.form_edit_node import FormEditNode
from components.module_locker import ModuleLocker
from data_manager.forms.form_doors_inputs import FormDoorsInputs
from data_manager.view.widget_view import View
import data_manager.tree_walker as tree_walker
from config import constants
from components.chart.chart_bar import ChartBar


# from my_logging import logger
# logger.debug(f"{__name__} --> Init")

style = """
QWidget, QFrame{
    font-size: 16px;
    border: none;
}

QFrame, QLineEdit{
	background-color: rgb(33, 37, 43);

	font-family: "Arial Narrow", Arial, "Helvetica Condensed", Helvetica, sans-serif;	

	letter-spacing: 1.3px;
}



QLabel{
    color: rgb(95, 180, 255);
    color: rgb(150, 150, 150);
    font-weight: bold;
    min-width: 20px;
}

QListWidget, QTextEdit{
	border: 1px solid rgb(50,50,50);
}


QListWidget::item{
    padding:1px;
    font-size: 14px;
    } 

QListWidget::item:hover {
    background-color: rgb(58, 89, 245);
}


QToolTip{
    font-size: 16px;
    padding: 15px;
    }

QLineEdit, QPushButton{
	padding: 5;
	border: 1px solid rgb(39, 44, 54);
}

QPushButton:hover{
	background-color:rgb(39, 44, 54);
}


QMenu::separator {
     height: 2px;
     margin: 2px 5px 2px 4px;
	background-color: red;
	color: red;
 }





QPushButton {	
	border: none;
	padding: 10;
	border-right: 5px solid rgb(44, 49, 60);
	background-color: rgb(39, 44, 54);
	text-align: left;

}
QPushButton:hover {
	background-color: rgb(33, 37, 43);

}
QPushButton:pressed {	
	background-color: rgb(85, 170, 255);

}

QPushButton:checked {	
	background-color: rgb(85, 170, 255);
}

QPushButton:disabled {	
	color: rgb(80, 80, 80);

}


#uiLayoutTitleBar, #uiFrameTitleBar{
    background-color: rgb(39, 44, 54);
}

#uiFrameTitleBar QPushButton{
    font-size: 12px;
}



"""


class DataManager(QWidget, Ui_Form):

    send_file_path = pyqtSignal(Path)

    def __init__(self, main_window, project_manager):
        super().__init__()
        self.setupUi(self)
        # self.setStyleSheet(style)
        # node copied into memory by action COPY
        self.node_2_paste = None        

        self.MAIN = main_window
        self.PROJECT_MANAGER = project_manager     
        self.MODEL = QStandardItemModel()
        self.ROOT = self.MODEL.invisibleRootItem()        
        self.ROOT.setData(self, Qt.UserRole)  # add pointer to DataManager instance to be accesseble from child nodes (ReqNode, CondNode, ...)

        self.send_file_path.connect(self.MAIN.file_open_from_tree)

        self.VIEW = View(self, self.MODEL)
        self.ui_layout_tree.addWidget(self.VIEW)
        self.TREE = self.VIEW.uiDataTreeView  # TODO: REFACTOR

        self.progress_bar = ModernProgressBar('rgb(0, 179, 0)', 'COVERED')
        # self.ui_layout_data_summary.addWidget(self.progress_bar)   
        self.widget_chart = ChartBar()
        self.ui_layout_data_summary.addWidget(self.widget_chart)

        # self.MODEL.itemChanged.connect(lambda: self.set_project_saved(False))
        self.MODEL.rowsInserted.connect(lambda: self.set_project_saved(False))
        self.MODEL.rowsRemoved.connect(lambda: self.set_project_saved(False))

        # ALL BUTTONS
        self.uiBtnUpdateRequirements.clicked.connect(lambda: self._open_form_for_doors_connection_inputs(all_modules=True))
        self.uiBtnNewModule.clicked.connect(self._open_add_requirement_module_form)
        self.uiBtnCheckCoverage.clicked.connect(self._create_dict_from_scripts_for_coverage_check)
        self.uiBtnCheckHtmlReport.clicked.connect(self.check_HTML_report)
        self.uiBtnSetProjectPath.clicked.connect(self._set_project_path)

        # POINTER TO REQ MODULE(S) WHICH ARE DOWNLOADING
        # self._currently_downloaded_modules = []
        self._module_locker = ModuleLocker()

        # SPECIAL THREAD FOR BROWSING HDD AND GETTING DATA FOR COVERAGE CHECK
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(1)  

        QShortcut( 'Ctrl+S', self ).activated.connect(self.MAIN.project_save)
        QShortcut( 'Backspace', self ).activated.connect(self.TREE.goto_previous_index)
 
     

    @pyqtSlot(bool, str)
    def update_progress_status(self, is_visible, text=''):
        self.MAIN.uiLabelProgressStatus.setText(text) if is_visible else self.MAIN.uiLabelProgressStatus.setText("Ready")
        self.MAIN.uiLabelProgressStatus.setStyleSheet("color: rgb(50, 250, 50);") if is_visible else self.MAIN.uiLabelProgressStatus.setStyleSheet("color: rgb(200, 200, 200);")


    def receive_data_from_drop_or_file_manager(self, data):
        condition_nodes.initialise(data, self.ROOT)
        dspace_nodes.initialise(data, self.ROOT)
        a2l_nodes.initialise(data, self.ROOT)
        self.MAIN.show_notification(f"Data Updated")   
        self.send_data_2_completer() 
        self.TREE.setCurrentIndex(self.MODEL.indexFromItem(self.ROOT.child(0)))


    ################################################################################################
    #  PROJECT HANDLING
    ################################################################################################

    def _set_project_path(self):
        folder = QFileDialog.getExistingDirectory(self, "Set Project Path", "", QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if folder:
            self.PROJECT_MANAGER.receive_parameters_from_listeners(dict(disk_project_path=folder))
            return True
        return False
    

    # @interface --> PROJECT MANAGER
    def set_project_saved(self, is_modified: bool) -> None:
        self.PROJECT_MANAGER.receive_parameters_from_listeners(dict(is_project_saved=is_modified))


    @pyqtSlot(dict)
    def receive_data_from_project_manager(self, data: dict):

        self.ROOT.removeRows(0, self.ROOT.rowCount())

        condition_nodes.initialise(data, self.ROOT)
        dspace_nodes.initialise(data, self.ROOT)
        a2l_nodes.initialise(data, self.ROOT)
        requirement_module.initialise(data, self.ROOT)   
        self.TREE.setCurrentIndex(self.MODEL.indexFromItem(self.ROOT.child(0)))     

        self._update_data_summary()
        self.send_data_2_completer()  
        self.set_project_saved(True)


    @pyqtSlot(dict)
    def receive_parameters_from_project_manager(self, parameters: dict):
        self.ui_lab_project_path.setText(parameters["disk_project_path"])


    @pyqtSlot(dict)
    def provide_data_4_project_manager(self):
        data = {
            'Conditions Files': [],
            'DSpace Files': [],
            'A2L Files': [],
            'REQUIREMENT MODULES': [],
        }
        for row in range(self.ROOT.rowCount()):
            current_node = self.ROOT.child(row)  # get node object
            received_data = current_node.data_4_project(data)
            data.update(received_data)
            # if con/dspace file is modified, save it
            if isinstance(current_node, (ConditionFileNode, DspaceFileNode)):
                if current_node.is_modified:
                    success, message = model_manager.export_file(current_node)
                    if not success:
                        dialog_message(self, message)

        return data


    #####################################################################################################################################################
    #   ADDING REQUIREMENT MODULE
    #####################################################################################################################################################

    def _open_add_requirement_module_form(self):
        self.form_add_req_module = FormAddModule(self)
        self.form_add_req_module.show()

    @pyqtSlot(str, list)
    def receive_data_from_add_req_module_dialog(self, module_path, columns_names):
        r = RequirementModule(self.ROOT, module_path, columns_names, attributes=[], baseline={}, coverage_filter=None, coverage_dict=None, update_time=None, ignore_list=None, notes=None, current_baseline=None)
        self.ROOT.appendRow(r)

    #####################################################################################################################################################
    #   CONNECTING AND DOWNLOADING DATA FROM DOORS
    #####################################################################################################################################################        

    def _open_form_for_doors_connection_inputs(self, all_modules: bool) -> None:  # Button Update All Requirements or Update Module Context Menu
        if self._module_locker.locked_modules:  # Dialog message when Doors is now connected  
            dialog_message(self, "Requirements are being downloaded from Doors. Please wait...")
            return   
    
        if not tree_walker.at_least_one_module_is_present(self.ROOT):
            # dialog_message(self, "There are no Requirement Modules. Add at least one.")
            self._open_add_requirement_module_form()
            return
        
        self.form_doors_inputs = FormDoorsInputs(self, all_modules)


    @pyqtSlot(bool, str, str, str, str)
    def receive_inputs_from_doors_connection_form(self, all_modules, app_path, database_path, user_name, password):
        if all_modules:  # if Button from Upper Menu was pushed (Update All Requirements)
            for row in range(self.ROOT.rowCount()):
                node = self.ROOT.child(row)
                if isinstance(node, RequirementModule):
                    self._module_locker.lock_module(node)
        else:  # if Button from Context Menu was pushed (Update Module)
            selected_item_index = self.TREE.currentIndex()
            selected_item = self.MODEL.itemFromIndex(selected_item_index)
            if isinstance(selected_item, RequirementModule):
                self._module_locker.lock_module(selected_item)
           
        module_paths = []
        module_columns = []
        module_baselines = []
        for node in self._module_locker.locked_modules:
            module_paths.append(node.path)
            module_columns.append(node.columns_names)
            module_baselines.append(node.current_baseline)                
        if module_paths and module_columns and module_baselines:
            self._send_request_2_doors(app_path, database_path, user_name, password, module_paths, module_columns, module_baselines)



    def _send_request_2_doors(self, app_path, database_path, user_name, password, module_paths, columns_names, baselines):
        DoorsConnection(self, app_path, database_path, user_name, password, module_paths, columns_names, baselines)
        self.update_progress_status(True, 'Initialising...')
        self.uiBtnCheckCoverage.setEnabled(False)


    #####################################################################################################################################################
    #   RECEIVING DATA FROM DOORS
    ##################################################################################################################################################### 

    @pyqtSlot(str, str)
    def receive_data_from_doors(self, doors_output: str, timestamp: str):
        global_success = True
        if doors_output == "Connection Failed":
            global_success = False
            dialog_message(self, "Connecting to Doors Failed.\n\nPossible reasons:\n1. Invalid username/password\n2. Doors client is N/A\n3. Network issues.")
  
        else:
            for module in self._module_locker.locked_modules:
                success, message = module.receive_data_from_doors(doors_output, timestamp)
                if not success:                     
                    global_success = False
                    dialog_message(self, message)
                    break
                self.set_project_saved(False)
        
        self._module_locker.unlock_all_modules()
        self._update_data_summary()
        self.uiBtnCheckCoverage.setEnabled(True)
        if global_success: 
            dialog_message(self, "Requirements have been updated successfully.", "Downloading from Doors finished")


    #####################################################################################################################################################
    #   UPDATING COVERAGE BY EDITING SCRIPT IN EDITOR
    #####################################################################################################################################################

    @pyqtSlot(set, str)
    def script_requirement_reference_changed(self, req_references: set[str], script_path: str):
        if self.PROJECT_MANAGER.disk_project_path():
            for req_reference in req_references:            
                for row in range(self.ROOT.rowCount()):
                    current_item = self.ROOT.child(row)
                    if isinstance(current_item, RequirementModule) and current_item.coverage_filter:
                        change = current_item.update_script_in_coverage_dict(req_reference, script_path)
                        # print(req_reference, script_path, change)
                        
                        if change:
                            self._update_data_summary()            
                            self.set_project_saved(False)
                            self.MAIN.show_notification("Coverage Updated.")
                            # self._display_values()


    #####################################################################################################################################################
    #   PHYSICAL COVERAGE CHECK
    #####################################################################################################################################################
    def _create_dict_from_scripts_for_coverage_check(self): # PushButton Check Coverage clicked
        if not tree_walker.at_least_one_module_with_coverage_is_present(self.ROOT):
            dialog_message(self, "There are no Requirement Modules with Coverage Filter. Add at least one.")
            return
        
        if self.PROJECT_MANAGER.disk_project_path() is None:
            succes = self._set_project_path()
            if not succes: return
        
        self.uiBtnCheckCoverage.setEnabled(False)        
        worker = Worker(self)
        self.threadpool.start(worker)


    @pyqtSlot(dict)
    def check_coverage(self, file_content_dict: dict):
        if self.PROJECT_MANAGER.disk_project_path():
            for row in range(self.ROOT.rowCount()):
                current_item = self.ROOT.child(row)
                if isinstance(current_item, RequirementModule):
                    change = current_item.check_coverage_with_file_pointers(file_content_dict)
                    if change:
                        self.set_project_saved(False)
            self._update_data_summary()
            self.uiBtnCheckCoverage.setEnabled(True)



    #####################################################################################################################################################
    #   UPDATE DATA SUMMARY
    #####################################################################################################################################################
    def _update_data_summary(self):        
        calculated_number, covered_number = 0, 0
        for row in range(self.ROOT.rowCount()):
            current_node = self.ROOT.child(row)
            if isinstance(current_node, RequirementModule) and current_node.coverage_filter:                          
                calculated_number += current_node.number_of_calculated_requirements
                covered_number += current_node.number_of_covered_requirements
                
        # VIEW PART
        self.progress_bar.update_value(calculated_number, covered_number)
        self.ui_lab_req_total.setText(str(calculated_number))
        self.ui_lab_req_covered.setText(str(covered_number))
        self.ui_lab_req_not_covered.setText(str(calculated_number - covered_number))
        # self._display_values()
        self.VIEW._update_view()
        self.widget_chart.set_value(covered_number, calculated_number)
    


    ##############################################################################################################################
    # IGNORE LIST:
    ##############################################################################################################################

    def _add_to_ignore_list(self):
        selected_item_index = self.TREE.currentIndex()
        selected_item = self.MODEL.itemFromIndex(selected_item_index)
        if isinstance(selected_item, RequirementNode):
            selected_item.add_to_ignore_list()    
            self._update_data_summary()              
            self.set_project_saved(False) 

    def _remove_from_ignore_list(self):
        selected_item_index = self.TREE.currentIndex()
        selected_item = self.MODEL.itemFromIndex(selected_item_index)
        if isinstance(selected_item, RequirementNode):
            selected_item.remove_from_ignore_list()    
            self._update_data_summary()   
            self.set_project_saved(False)      


    ####################################################################################################################
    # LIST WIDGETS CLICKS/HOVER MANAGEMENT  
    ####################################################################################################################

    def _get_tooltip_from_link(self, link):
        module_path = link.split(":")[0]
        identifier = link.split(":")[1]

        for row in range(self.ROOT.rowCount()):
            node = self.ROOT.child(row)
            if node.path == module_path:
                if node.hasChildren():
                    first_child_reference = node.child(0).reference
                    prefix = first_child_reference.split("_")[:-1]
                    full_reference = "_".join(prefix) + "_" + identifier
                    found_node = tree_walker.find_node_by_identifier(node, full_reference)
                    return "\n".join(found_node.columns_data) if found_node else ""



    def set_tooltip_2_list_widget_item(self, item):
        identifier = item.data(Qt.UserRole)
        module = self.MODEL.itemFromIndex(self.TREE.currentIndex())
        found_node = tree_walker.find_node_by_identifier(module, identifier)
        item.setToolTip("\n".join(found_node.columns_data) if found_node else "")
              

              

    def _doubleclick_on_identifier(self, item: QListWidgetItem):
        module = self.MODEL.itemFromIndex(self.TREE.currentIndex())
        identifier = item.data(Qt.UserRole)                
        found_node = tree_walker.find_node_by_identifier(module, identifier)
        if found_node:
            self.TREE.setCurrentIndex(found_node.index())
            self.TREE.scrollTo(found_node.index())   


    def _doubleclick_on_outlink(self, outlink_item):
        module_path = outlink_item.data(Qt.UserRole).split(":")[0]
        reference = outlink_item.data(Qt.UserRole).split(":")[1]
        found_node = None

        if not tree_walker.is_module_present(self.ROOT, module_path):
            add_module = QMessageBox.question(self,
                                        f"Module is missing.",
                                        f"Module {module_path} is N/A.\n\nDo you want to add it?",
                                        QMessageBox.Yes | QMessageBox.No)
            if add_module == QMessageBox.Yes:            
                self.receive_data_from_add_req_module_dialog(module_path, [])        
        
            return

        for row in range(self.ROOT.rowCount()):
            node = self.ROOT.child(row)
            if node.path == module_path:
                if node.hasChildren():
                    first_child_reference = node.child(0).reference
                    if "_" in first_child_reference:  # LP3 has identifier just plain number
                        prefix = first_child_reference.split("_")[:-1]
                        full_reference = "_".join(prefix) + "_" + reference
                    else:
                        full_reference = reference
                    found_node = tree_walker.find_node_by_identifier(node, full_reference)

        if found_node:
            self.TREE.setCurrentIndex(found_node.index())
            self.TREE.scrollTo(found_node.index())
        else:
            self.MAIN.show_notification(f"{reference} is not present in {module_path}.")




    def _doubleclick_on_tc_reference(self, list_item_text):
        file_path_string = list_item_text.data(Qt.UserRole)
        self.send_file_path.emit(Path(file_path_string))
        self.MAIN.manage_right_menu(self.MAIN.tabs_splitter, self.MAIN.ui_btn_text_editor)




    

    ####################################################################################################################
    # A2L NORMALISATIION:
    ####################################################################################################################
    def _normalise_a2l_file(self):
        selected_item_index = self.TREE.currentIndex()
        selected_item = self.MODEL.itemFromIndex(selected_item_index)
        if isinstance(selected_item, A2lFileNode):
            selected_item.normalise_file()  
            self.send_data_2_completer()  
            self.set_project_saved(True)  


    @pyqtSlot(dict, list, list)
    def a2l_normalisation_finished(self, data_4_report, missing_signals, duplicated_signals):
        # reload(data_manager.form_a2l_norm_report)
        self.form = data_manager.forms.form_a2l_norm_report.A2lNormReport(data_4_report, missing_signals, duplicated_signals)
        self.form.show()



    ####################################################################################################################
    # ADDING / MODIFYING / REMOVING / EXPORTING NODES DATA:
    ####################################################################################################################


    def tree_2_file(self):
        selected_item_index = self.TREE.currentIndex()
        selected_item = self.MODEL.itemFromIndex(selected_item_index)
        success, message = model_manager.export_file(selected_item)
        if success:
            self.MAIN.show_notification("File Exported.")
        else:
            dialog_message(self, message)
        

    def remove_node(self):
        remove = QMessageBox.question(self,
                    "Remove Item",
                    "Do you want to remove selected item?",
                    QMessageBox.Yes | QMessageBox.No)
        if remove == QMessageBox.Yes:        
            result = model_manager.remove_node(self.TREE, self.MODEL)
            message = "Item Removed" if result else "Item can not be Removed"
            self.MAIN.show_notification(message)  
            self.send_data_2_completer()
            self._update_data_summary()  
            self.TREE.setFocus()                  
        

    def duplicate_node(self):
        success = model_manager.duplicate_node(self.TREE, self.MODEL)
        if success:
            self.MAIN.show_notification(f"Item was duplicated.")  
            self.TREE.setFocus()

    def copy_node(self):
        self.node_2_paste = model_manager.copy_node(self.TREE, self.MODEL)        
        if self.node_2_paste: 
            self.MAIN.show_notification(f"Item was copied to Clipboard.")  
            self.TREE.setFocus()

            # TODO: REFACTOR COUPLING
            self.VIEW.action_paste.setEnabled(True)


    def paste_node(self):
        success = model_manager.paste_node(self.TREE, self.MODEL, self.node_2_paste)
        if success:
            self.MAIN.show_notification(f"Item {self.node_2_paste.text()} was inserted.") 
            self.node_2_paste = None
            self.send_data_2_completer
            self.TREE.setFocus()
            # TODO: REFACTOR COUPLING
            self.VIEW.action_paste.setEnabled(False)


    def edit_node_request(self):
        selected_item_index = self.TREE.currentIndex()
        selected_item = self.MODEL.itemFromIndex(selected_item_index)

        if not selected_item or isinstance(selected_item, (ConditionFileNode, A2lFileNode, A2lNode, DspaceFileNode, DspaceDefinitionNode)):
            self.MAIN.show_notification("Item is not Editable!")
            return
        
        if isinstance(selected_item, RequirementModule) and selected_item in self._module_locker.locked_modules:
            self.MAIN.show_notification("Module is being downloaded from Doors. Please wait...")
            return
        
        self.form_edit_node = FormEditNode(selected_item, self)
    
    
    @pyqtSlot()
    def edit_node_response(self):
        self.MAIN.show_notification("Data Updated")
        self._update_data_summary()
        self.set_project_saved(False)
        self.send_data_2_completer()
        self.TREE.setFocus()


    def move_node(self, direction):
        model_manager.move_node(self.TREE, self.MODEL, direction)
        self.send_data_2_completer()
        self.set_project_saved(False)
        self.TREE.setFocus()




    ####################################################################################################################
    # COMPLETER:
    ####################################################################################################################

    def send_data_2_completer(self):
        model_manager.send_data_2_completer(self.ROOT)
        self._update_data_summary()


    ####################################################################################################################
    # HTML REPORT CHECK:
    ####################################################################################################################
    
    def check_HTML_report(self):
        # reload(data_manager.form_validate_html_report)
        
        path, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption='Open HTML Report',
            directory=self.PROJECT_MANAGER.disk_project_path(),
            filter="*.html"
        )

        if not path: return

        try:
            with Path(path).open() as f:
                html_report_string = f.read()

        except Exception as my_exception:
            dialog_message(self, str(my_exception))                      
                
        missing_requirements, covered_requirements = [], []

        for row in range(self.ROOT.rowCount()):
            file_node = self.ROOT.child(row)
            if isinstance(file_node, RequirementModule) and file_node.coverage_filter:
                for k in file_node.coverage_dict.keys():
                    if k.lower() in html_report_string.lower():
                        covered_requirements.append(k)
                    else:
                        missing_requirements.append(k)

        self.form = data_manager.forms.form_validate_html_report.FormValidatedHTMLReport(self, missing_requirements)

    @pyqtSlot(str)
    def doubleclicked_on_requirement_in_HTML_report_form(self, req_identifier: str):
        for row in range(self.ROOT.rowCount()):
            node = self.ROOT.child(row)
            if isinstance(node, RequirementModule) and node.coverage_filter:
                FOUND_NODE = tree_walker.find_node_by_identifier(node, req_identifier)
                if FOUND_NODE:
                    self.TREE.setCurrentIndex(FOUND_NODE.index())
                    self.TREE.scrollTo(FOUND_NODE.index())


    





   
####################################################################################################################
# COVERAGE CHECK --> PHYSICAL CHECK OF FILES ON DISK:
####################################################################################################################

class Worker(QRunnable):
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.signals = WorkerSignals()
        self.signals.status.connect(data_manager.update_progress_status)
        self.signals.finished.connect(data_manager.check_coverage)        


    @pyqtSlot()
    def run(self):
        reference_dict = {}       
        for root, dirs, files in os.walk(self.data_manager.PROJECT_MANAGER.disk_project_path()):
            for filename in files:
                if filename.endswith((".par", ".txt")):
                    full_path = Path(root) / Path(filename)
                    full_path = str(full_path)

                    self.signals.status.emit(True, f"Checking: <{full_path}>")

                    with open(full_path, 'r') as f:
                        text = f.read()
                    reference_list = constants.PATTERN_REQ_REFERENCE.findall(text)

                    for ref_string in reference_list:
                        references = ref_string.split(",")
                        for ref in references:
                            ref = ref.lower().strip()

                            if ref in reference_dict:
                                reference_dict[ref].add(full_path)
                            else:
                                reference_dict.update({ref: set([full_path,])})   
        
        self.signals.status.emit(False, "Updating coverage, please wait...")
        self.signals.finished.emit(reference_dict)




class WorkerSignals(QObject):
    finished = pyqtSignal(dict)
    status = pyqtSignal(bool, str)