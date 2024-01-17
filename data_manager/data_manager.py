from importlib import reload
from pathlib import Path
from ui.model_editor_ui import Ui_Form
import json, re, os
from PyQt5.QtWidgets import QWidget, QFileDialog, QInputDialog, QMenu, QAction, QLineEdit, QShortcut, QMessageBox
from PyQt5.QtGui import QIcon, QCursor, QKeySequence, QStandardItemModel
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QObject, QRunnable, QThreadPool, QPropertyAnimation, QEasingCurve
from data_manager.condition_nodes import ConditionFileNode, ConditionNode, ValueNode, TestStepNode
from data_manager.dspace_nodes import DspaceFileNode, DspaceDefinitionNode, DspaceVariableNode
from data_manager.a2l_nodes import A2lFileNode, A2lNode
from data_manager import a2l_nodes, condition_nodes, requirement_nodes, dspace_nodes
from data_manager.requirement_nodes import RequirementFileNode, RequirementNode
from data_manager.form_add_module import FormAddModule
from data_manager.form_add_requirement_filter import FormAddCoverageFilter
from progress_bar.widget_modern_progress_bar import ModernProgressBar
from components.droppable_tree_view import DroppableTreeView
from text_editor.text_editor import TextEdit
from components.template_test_case import TemplateTestCase
from components.reduce_path_string import reduce_path_string
from dialogs.dialog_message import dialog_message
from doors.doors_connection import DoorsConnection

import data_manager.form_a2l_norm_report        
from data_manager import model_manager
from data_manager import view_filter
from data_manager.ui_control_manager import UIControlManager
from data_manager.display_manager import DisplayManager
from data_manager.form_edit_node import FormEditNode
from components.module_locker import ModuleLocker
from data_manager.form_doors_inputs import FormDoorsInputs


# from my_logging import logger


# logger.debug(f"{__name__} --> Init")


class DataManager(QWidget, Ui_Form):

    send_file_path = pyqtSignal(Path)

    def __init__(self, main_window, project_manager):
        super().__init__()
        self.setupUi(self)

        self.MAIN = main_window
        self.PROJECT_MANAGER = project_manager     
        self.DISPLAY_MANAGER = DisplayManager(self)   
        self.MODEL = QStandardItemModel()
        self.ROOT = self.MODEL.invisibleRootItem()        
        self.ROOT.setData(self, Qt.UserRole)  # add pointer to DataManager instance to be accesseble from child nodes (ReqNode, CondNode, ...)

        self.TREE = DroppableTreeView(self)
        self.ui_layout_tree.addWidget(self.TREE)
        self.TREE.setModel(self.MODEL)
        self.TREE.customContextMenuRequested.connect(self._context_menu) 
        self.TREE.clicked.connect(self._display_values)
        selection_model = self.TREE.selectionModel()
        selection_model.selectionChanged.connect(self._display_values)  # update line edits on Up/Down Arrows  

        self.progress_bar = ModernProgressBar('rgb(0, 179, 0)', 'COVERED')
        self.ui_layout_data_summary.addWidget(self.progress_bar)                

        QShortcut( 'Ctrl+Down', self.TREE ).activated.connect(lambda: self.move_node(direction='down'))
        QShortcut( 'Ctrl+Up', self.TREE ).activated.connect(lambda: self.move_node(direction='up'))
        QShortcut( 'Del', self.TREE ).activated.connect(self.remove_node)
        QShortcut( 'Ctrl+D', self.TREE ).activated.connect(self.duplicate_node)
        QShortcut( 'Ctrl+C', self.TREE ).activated.connect(self.copy_node)
        QShortcut( 'Ctrl+V', self.TREE ).activated.connect(self.paste_node)
        QShortcut( 'Esc', self.TREE ).activated.connect(self._stop_filtering)
        QShortcut( 'Ctrl+S', self ).activated.connect(self.MAIN.project_save)
     


        ################## ACTIONS START ###########################
        self.action_expand_all_children = QAction(QIcon(u"ui/icons/16x16/cil-expand-down.png"), "Expand All Children")
        self.action_expand_all_children.triggered.connect(self._expand_all_children)
        self.action_collapse_all_children = QAction(QIcon(u"ui/icons/16x16/cil-expand-up.png"), "Collapse All Children")
        self.action_collapse_all_children.triggered.connect(self._collapse_all_children)        

        self.action_create_testable_tc_template_with_req_reference = QAction(QIcon(u"ui/icons/16x16/cil-description.png"), "Create Testable Test Script")
        self.action_create_testable_tc_template_with_req_reference.triggered.connect(lambda: self._create_tc_template_with_req_reference(True))
        self.action_create_not_testable_tc_template_with_req_reference = QAction(QIcon(u"ui/icons/16x16/cil-description.png"), "Create NOT Testable Test Script")
        self.action_create_not_testable_tc_template_with_req_reference.triggered.connect(lambda: self._create_tc_template_with_req_reference(False))        

        self.action_update_requirements = QAction('Update Requirements')
        self.action_update_requirements.setIcon(QIcon(u"ui/icons/16x16/cil-cloud-download.png"))
        self.action_update_requirements.triggered.connect(lambda: self._open_form_for_doors_connection_inputs(all_modules=False))

        self.action_remove = QAction(QIcon(u"ui/icons/16x16/cil-x.png"), 'Remove')
        self.action_remove.triggered.connect(self.remove_node)
        self.action_remove.setShortcut('Del')

        self.action_edit = QAction('Edit')
        self.action_edit.setIcon(QIcon(u"ui/icons/16x16/cil-pencil.png"))
        self.action_edit.triggered.connect(self.edit_node_request)

        self.action_duplicate = QAction('Duplicate')
        self.action_duplicate.setIcon(QIcon(u"ui/icons/16x16/cil-clone.png"))
        self.action_duplicate.triggered.connect(self.duplicate_node)
        self.action_duplicate.setShortcut(QKeySequence("Ctrl+D"))

        self.action_copy = QAction('Copy')
        self.action_copy.setIcon(QIcon(u"ui/icons/20x20/cil-copy.png"))
        self.action_copy.triggered.connect(self.copy_node)
        self.action_copy.setShortcut(QKeySequence("Ctrl+C"))

        self.action_paste = QAction('Paste')
        self.action_paste.setIcon(QIcon(u"ui/icons/16x16/cil-share.png"))
        self.action_paste.triggered.connect(self.paste_node)
        self.action_paste.setShortcut(QKeySequence("Ctrl+V"))          

        self.action_save = QAction('Export')
        self.action_save.setIcon(QIcon(u"ui/icons/16x16/cil-save.png"))
        self.action_save.triggered.connect(self.tree_2_file) 

        self.action_move_up = QAction('Move Up')
        self.action_move_up.setIcon(QIcon(u"ui/icons/16x16/cil-level-up.png"))
        self.action_move_up.setShortcut('Ctrl+Up')
        self.action_move_up.triggered.connect(lambda: self.move_node(direction='up')) 

        self.action_move_down = QAction(QIcon(u"ui/icons/16x16/cil-level-down.png"), 'Move Down')
        self.action_move_down.setShortcut(QKeySequence("Ctrl+Down"))
        self.action_move_down.triggered.connect(lambda: self.move_node(direction='down')) 

        self.action_normalise_a2l_file = QAction('Normalise (VDA spec.)')
        self.action_normalise_a2l_file.setIcon(QIcon(u"ui/icons/16x16/cil-chart-line.png"))
        self.action_normalise_a2l_file.triggered.connect(self._normalise_a2l_file)  

        self.action_open_coverage_filter = QAction(QIcon(u"ui/icons/16x16/cil-wifi-signal-2.png"), 'Set Coverage Filter')
        self.action_open_coverage_filter.triggered.connect(self._open_form_for_coverage_filter) 
        self.action_edit_coverage_filter = QAction(QIcon(u"ui/icons/16x16/cil-wifi-signal-2.png"), 'Modify Coverage Filter')
        self.action_edit_coverage_filter.triggered.connect(self._open_form_for_coverage_filter)  
        self.action_remove_coverage_filter = QAction(QIcon(u"ui/icons/16x16/cil-wifi-signal-off.png"), "Remove Coverage Filter")
        self.action_remove_coverage_filter.triggered.connect(self._remove_coverage_filter)                

        self.action_show_only_requirements_with_coverage = QAction('Show Not Covered + Covered')
        self.action_show_only_requirements_with_coverage.triggered.connect(self._show_only_items_with_coverage)
        self.action_show_only_requirements_not_covered = QAction('Show Not Covered')
        self.action_show_only_requirements_not_covered.triggered.connect(self._show_only_items_not_covered)        
        self.action_show_all_requirements = QAction('Show All')
        self.action_show_all_requirements.setIcon(QIcon(u"ui/icons/24x24/cil-check-alt.png"))
        self.action_show_all_requirements.triggered.connect(self._show_all_items)        

        self.action_add_to_ignore_list = QAction(QIcon(u"ui/icons/16x16/cil-task.png"), "Add To Ignore List")
        self.action_add_to_ignore_list.triggered.connect(self._add_to_ignore_list)
        self.action_remove_from_ignore_list = QAction(QIcon(u"ui/icons/16x16/cil-external-link.png"), "Remove From Ignore List")
        self.action_remove_from_ignore_list.triggered.connect(self._remove_from_ignore_list)        
        ################## ACTIONS END ###########################


        self.UI_CONTROL_MANAGER = UIControlManager(
            
            action_expand_all_children=self.action_expand_all_children,
            action_collapse_all_children=self.action_collapse_all_children,
            action_remove_node=self.action_remove,
            action_edit_node=self.action_edit,
            action_duplicate_node=self.action_duplicate,
            action_copy_node=self.action_copy,
            action_paste_node=self.action_paste,
            action_export_node=self.action_save,
            action_move_up_node=self.action_move_up,
            action_move_down_node=self.action_move_down,
            action_normalise_a2l_file=self.action_normalise_a2l_file,
            action_update_module=self.action_update_requirements,
            action_open_coverage_filter=self.action_open_coverage_filter,
            action_edit_coverage_filter=self.action_edit_coverage_filter,
            action_remove_coverage_filter=self.action_remove_coverage_filter,
            action_add_to_ignore_list=self.action_add_to_ignore_list,
            action_remove_from_ignore_list=self.action_remove_from_ignore_list,
            action_show_only_requirements_with_coverage=self.action_show_only_requirements_with_coverage,
            action_show_only_requirements_not_covered=self.action_show_only_requirements_not_covered,
            action_show_all_requirements=self.action_show_all_requirements,

        )


        # MODEL SIGNALS:
        # self.MODEL.itemChanged.connect(lambda: self.set_project_saved(False))
        self.MODEL.rowsInserted.connect(lambda: self.set_project_saved(False))
        self.MODEL.rowsRemoved.connect(lambda: self.set_project_saved(False))

        # ALL BUTTONS
        self.uiBtnEditNode.clicked.connect(self.edit_node_request)
        self.uiBtnEditNode.setShortcut('F4')
        self.uiBtnEditNode.setToolTip("F4")
        self.uiBtnUpdateRequirements.clicked.connect(lambda: self._open_form_for_doors_connection_inputs(all_modules=True))
        self.uiBtnNewModule.clicked.connect(self._open_add_requirement_module_form)
        self.uiBtnCheckCoverage.clicked.connect(self._create_dict_from_scripts_for_coverage_check)
        self.uiBtnCheckHtmlReport.clicked.connect(self.check_HTML_report)
        self.uiLineEditFilter.textChanged.connect(self._filter_items)
        # self.uiLineEditFilter.textEdited.connect(self._reset_filter)
        self.uiBtnPreviousView.clicked.connect(self._goto_previous_index)

        # node copied into memory by action COPY
        self._node_to_paste = None

        # POINTER TO REQ MODULE(S) WHICH ARE DOWNLOADING
        # self._currently_downloaded_modules = []
        self._module_locker = ModuleLocker()

        # SPECIAL THREAD FOR BROWSING HDD AND GETTING DATA FOR COVERAGE CHECK
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(1)  
 
     


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




    ################################################################################################
    #  PROJECT HANDLING
    ################################################################################################

    # @interface --> PROJECT MANAGER
    def set_project_saved(self, is_modified: bool) -> None:
        self.PROJECT_MANAGER.receive_parameters_from_listeners(dict(is_project_saved=is_modified))


    @pyqtSlot(dict)
    def receive_data_from_project_manager(self, data: dict):

        self.ROOT.removeRows(0, self.ROOT.rowCount())

        condition_nodes.initialise(data, self.ROOT)
        dspace_nodes.initialise(data, self.ROOT)
        a2l_nodes.initialise(data, self.ROOT)
        requirement_nodes.initialise(data, self.ROOT)        

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
        r = RequirementFileNode(self.ROOT, module_path, columns_names, attributes=[], baseline={}, coverage_filter=None, coverage_dict=None, update_time=None, ignore_list=None, notes=None, current_baseline=None)
        self.ROOT.appendRow(r)

    #####################################################################################################################################################
    #   CONNECTING AND DOWNLOADING DATA FROM DOORS
    #####################################################################################################################################################        

    # Click on Button Update all Requirements or Update Module from Context Menu
    def _open_form_for_doors_connection_inputs(self, all_modules: bool) -> None:
        if self._module_locker.locked_modules:  # Dialog message when Doors is now connected  
            dialog_message(self, "Requirements are being downloaded from Doors. Please wait...")
            return        
        self.form_doors_inputs = FormDoorsInputs(self, all_modules)


    @pyqtSlot(bool, str, str, str, str)
    def receive_inputs_from_doors_connection_form(self, all_modules, app_path, database_path, user_name, password):
        if all_modules:  # if Button from Upper Menu was pushed (Update All Requirements)
            for row in range(self.ROOT.rowCount()):
                node = self.ROOT.child(row)
                if isinstance(node, RequirementFileNode):
                    self._module_locker.lock_module(node)
        else:  # if Button from Context Menu was pushed (Update Module)
            selected_item_index = self.TREE.currentIndex()
            selected_item = self.MODEL.itemFromIndex(selected_item_index)
            if isinstance(selected_item, RequirementFileNode):
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
        self._display_values()
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
                    if isinstance(current_item, RequirementFileNode) and current_item.coverage_filter:
                        change = current_item.update_script_in_coverage_dict(req_reference, script_path)
                        # print(req_reference)
                        # print(script_path)
                        
                        if change:
                            self._update_data_summary()            
                            self.set_project_saved(False)
                            self.MAIN.show_notification("Coverage Updated.")
                            self._display_values()

        


    #####################################################################################################################################################
    #   PHYSICAL COVERAGE CHECK
    #####################################################################################################################################################
    def _create_dict_from_scripts_for_coverage_check(self):
        if self.PROJECT_MANAGER.disk_project_path():
            self.uiBtnCheckCoverage.setEnabled(False)        
            worker = Worker(self)
            self.threadpool.start(worker)


    @pyqtSlot(dict)
    def check_coverage(self, file_content_dict: dict):
        if self.PROJECT_MANAGER.disk_project_path():
            for row in range(self.ROOT.rowCount()):
                current_item = self.ROOT.child(row)
                if isinstance(current_item, RequirementFileNode):
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
            if isinstance(current_node, RequirementFileNode) and current_node.coverage_filter:                          
                calculated_number += current_node.number_of_calculated_requirements
                covered_number += current_node.number_of_covered_requirements
                
        # VIEW PART
        self.progress_bar.update_value(calculated_number, covered_number)
        self.ui_lab_req_total.setText(str(calculated_number))
        self.ui_lab_req_covered.setText(str(covered_number))
        self.ui_lab_req_not_covered.setText(str(calculated_number - covered_number))
        self._display_values()
        




    ##############################################################################################################################
    # COVERAGE FILTER - OPENING FORM AND RECEIVING BACK COVERAGE FILTER STRING:
    ##############################################################################################################################

    def _open_form_for_coverage_filter(self):
        selected_item_index = self.TREE.currentIndex()
        selected_item = self.MODEL.itemFromIndex(selected_item_index)
        if isinstance(selected_item, RequirementFileNode):
            self.form_req_filter = FormAddCoverageFilter(self, selected_item)
            self.form_req_filter.show()


    @pyqtSlot(str)
    def receive_data_from_req_filter_form(self, filter_string):
        index = self.TREE.currentIndex()
        node = self.MODEL.itemFromIndex(index)
        node.apply_coverage_filter(filter_string) 
        self._update_data_summary()
        # Remove View Filter
        self._show_all_items()       
        self.set_project_saved(False) 


    def _remove_coverage_filter(self):
        index = self.TREE.currentIndex()
        requirement_file_node = self.MODEL.itemFromIndex(index)   
        requirement_file_node.remove_coverage_filter()
        self._update_data_summary()
        #  Remove View Filter
        self._show_all_items()
        self.set_project_saved(False)


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
    # VIEW 
    ####################################################################################################################

    def _display_values(self):
        selected_item_index = self.TREE.currentIndex()
        selected_item = self.MODEL.itemFromIndex(selected_item_index)  
        
        self.DISPLAY_MANAGER.get_layout(selected_item)
        self._show_filter_input(False)

        if selected_item:      
            self.uiLineEditFilter.setText(selected_item.data(Qt.UserRole))
        
            if isinstance(selected_item, (RequirementFileNode, A2lFileNode, ConditionFileNode, DspaceFileNode)):
                self._show_filter_input(True)




    def _context_menu(self, point):
        selected_item_index = self.TREE.indexAt(point)
        selected_item = self.MODEL.itemFromIndex(selected_item_index)

        if not selected_item_index.isValid():
            return

        if isinstance(selected_item, RequirementFileNode) and selected_item in self._module_locker.locked_modules:
            return

        if isinstance(selected_item, RequirementFileNode):
            self._evaluate_view_filter()
        
        menu = self.UI_CONTROL_MANAGER.get_context_menu(selected_item)
        
        if menu:
            if self._node_to_paste and type(self._node_to_paste) == type(selected_item):
                menu.addAction(self.action_paste)        
            menu.exec_(QCursor().pos())



    def _goto_previous_index(self):
        self.TREE.goto_previous_index()

    def _expand_all_children(self):
        self.TREE.expand_all_children()

    def _collapse_all_children(self):
        self.TREE.collapse_all_children()



    def _show_filter_input(self, show: bool) -> None:
        start_width = self.uiLineEditFilter.width()
        final_width = 8000 if show else 0
        self.animation = QPropertyAnimation(self.uiLineEditFilter, b"maximumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(start_width)
        self.animation.setEndValue(final_width)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.start()



    ####################################################################################################################
    # LIST WIDGETS CLICKS/HOVER MANAGEMENT  
    ####################################################################################################################

    def _get_tooltip_from_link(self, link):
        FOUND_LINK_TEXT = ""

        def find_node_by_reference(parent_node, reference):
            nonlocal FOUND_LINK_TEXT
            for row in range(parent_node.rowCount()):
                node = parent_node.child(row)
                if node.reference == reference:
                    # print(node)
                    # print("FOUND: ", node.reference)
                    FOUND_LINK_TEXT = "\n".join(node.columns_data)
                    if node.note:
                        FOUND_LINK_TEXT += f"\n\n<User Note>: {node.note}"
                    break
                else:
                    find_node_by_reference(node, reference)

        module_path = link.split(":")[0]
        reference = link.split(":")[1]

        for row in range(self.ROOT.rowCount()):
            node = self.ROOT.child(row)
            if node.path == module_path:
                if node.hasChildren():
                    first_child_reference = node.child(0).reference
                    prefix = first_child_reference.split("_")[:-1]
                    full_reference = "_".join(prefix) + "_" + reference
                    # print(full_reference)
                    find_node_by_reference(node, full_reference)


        return FOUND_LINK_TEXT                      
                


              

    def _doubleclick_on_ignored_reference(self, reference_item):
        selected_item_index = self.TREE.currentIndex()
        selected_item = self.MODEL.itemFromIndex(selected_item_index)
        reference = reference_item.text()

        FOUND_NODE = None
        def find_node_by_reference(parent_node, reference):
            nonlocal FOUND_NODE
            for row in range(parent_node.rowCount()):
                node = parent_node.child(row)
                if node.reference == reference:
                    print(reference)
                    FOUND_NODE = node
                    break
                else:
                    find_node_by_reference(node, reference)
        
        find_node_by_reference(selected_item, reference)     

        if FOUND_NODE:
            self.TREE.setCurrentIndex(FOUND_NODE.index())
            self.TREE.scrollTo(FOUND_NODE.index())   



    def _doubleclick_on_outlink(self, outlink_item):
        FOUND_NODE = None

        def find_node_by_reference(parent_node, reference):
            nonlocal FOUND_NODE
            for row in range(parent_node.rowCount()):
                node = parent_node.child(row)
                if node.reference == reference:
                    # print("FOUND: ", node.reference)
                    FOUND_NODE = node
                    return node
                else:
                    find_node_by_reference(node, reference)

        module_path = outlink_item.data(Qt.UserRole).split(":")[0]
        reference = outlink_item.data(Qt.UserRole).split(":")[1]

        for row in range(self.ROOT.rowCount()):
            node = self.ROOT.child(row)
            if node.path == module_path:
                if node.hasChildren():
                    first_child_reference = node.child(0).reference
                    prefix = first_child_reference.split("_")[:-1]
                    full_reference = "_".join(prefix) + "_" + reference
                    # print(full_reference)
                    find_node_by_reference(node, full_reference)


        if FOUND_NODE:
            self.TREE.setCurrentIndex(FOUND_NODE.index())
            self.TREE.scrollTo(FOUND_NODE.index())
        else:
            dialog_message(self, "Module is missing.")



    def _doubleclick_on_tc_reference(self, list_item_text):
        file_path_string = list_item_text.data(Qt.UserRole)
        self.send_file_path.emit(Path(file_path_string))
        self.MAIN.manage_right_menu(self.MAIN.tabs_splitter, self.MAIN.ui_btn_text_editor)




    def _create_tc_template_with_req_reference(self, is_testable):
        selected_item_index = self.TREE.currentIndex()
        selected_item = self.MODEL.itemFromIndex(selected_item_index)

        if isinstance(selected_item, RequirementNode):
            template = TemplateTestCase(req_id=selected_item.reference, req_text=selected_item.columns_data[-1], is_testable=is_testable)
            text = template.generate_tc_template()
            file_path = None
            tab_name = 'Untitled'
            self.MAIN.left_tabs.addTab(TextEdit(self.MAIN, text, file_path), QIcon(u"ui/icons/16x16/cil-description.png"), tab_name)
            self.MAIN.actual_text_edit.setFocus()
            self.MAIN.manage_right_menu(self.MAIN.tabs_splitter, self.MAIN.ui_btn_text_editor)            








##############################################################################################################################
# TEXT FILTER (ONLY VIEW AFFECTING
##############################################################################################################################

    def _stop_filtering(self):
        view_filter.stop_filtering(self.TREE, self.MODEL)


    # def _reset_filter(self, filtered_text):
    #     view_filter.reset_filter(self.TREE, self.MODEL, filtered_text)


    def _filter_items(self, filtered_text):
        view_filter.filter_items(self.TREE, self.MODEL, filtered_text)
        
        if filtered_text:            
            self.uiLineEditFilter.setStyleSheet(""" background-color: rgb(220, 220, 220);
                                                background-image: url(:/16x16/icons/16x16/cil-magnifying-glass.png);
                                                background-position: left center;
                                                background-repeat: no-repeat;
                                                padding-left: 20px;
                                                color: rgb(20, 20, 20);
                                                font-size: 18px;
                                                font-weight: bold;
                                                 """)

        else:
            self.uiLineEditFilter.setStyleSheet(""" background-color: rgb(35, 35, 25);
                                                background-image: url(:/16x16/icons/16x16/cil-magnifying-glass.png);
                                                background-position: left center;
                                                background-repeat: no-repeat;
                                                padding-left: 20px; """)



       
##############################################################################################################################
# COVERAGE FILTER (ONLY VIEW AFFECTING)
##############################################################################################################################

    def _show_only_items_with_coverage(self):
        view_filter.show_only_items_with_coverage(self.TREE, self.MODEL)

    def _show_only_items_not_covered(self):
        view_filter.show_only_items_not_covered(self.TREE, self.MODEL)

    def _show_all_items(self):
        view_filter.show_all_items(self.TREE, self.MODEL)

    def _evaluate_view_filter(self):
        view_filter.evaluate_view_filter(self.TREE, self.MODEL, 
                                         self.action_show_all_requirements, 
                                         self.action_show_only_requirements_with_coverage, 
                                         self.action_show_only_requirements_not_covered)
            


    ####################################################################################################################
    # A2L NORMALISATIION:
    ####################################################################################################################
    def _normalise_a2l_file(self):
        selected_item_index = self.TREE.currentIndex()
        selected_item = self.MODEL.itemFromIndex(selected_item_index)
        if isinstance(selected_item, A2lFileNode):
            selected_item.normalise_file()  
            self.send_data_2_completer()    


    @pyqtSlot(dict, list, list)
    def a2l_normalisation_finished(self, data_4_report, missing_signals, duplicated_signals):
        # reload(data_manager.form_a2l_norm_report)
        self.form = data_manager.form_a2l_norm_report.A2lNormReport(data_4_report, missing_signals, duplicated_signals)
        self.form.show()



    ####################################################################################################################
    # ADDING / MODIFYING / REMOVING / EXPORTING NODES DATA:
    ####################################################################################################################


    def tree_2_file(self):
        selected_item_index = self.TREE.currentIndex()
        selected_item = self.MODEL.itemFromIndex(selected_item_index)
        success, message = model_manager.export_file(selected_item)
        if success:
            self.MAIN.show_notification("File has been exported.")
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
        self._node_to_paste = model_manager.copy_node(self.TREE, self.MODEL)        
        if self._node_to_paste: 
            self.MAIN.show_notification(f"Item was copied to Clipboard.")  
            self.TREE.setFocus()


    def paste_node(self):
        success = model_manager.paste_node(self.TREE, self.MODEL, self._node_to_paste)
        if success:
            self.MAIN.show_notification(f"Item {self._node_to_paste.text()} was inserted.") 
            self._node_to_paste = None
            self.send_data_2_completer
            self.TREE.setFocus()


    def edit_node_request(self):
        selected_item_index = self.TREE.currentIndex()
        selected_item = self.MODEL.itemFromIndex(selected_item_index)

        if not selected_item or isinstance(selected_item, (ConditionFileNode, A2lFileNode, A2lNode, DspaceFileNode, DspaceDefinitionNode)):
            self.MAIN.show_notification("Item is not Editable!")
            return
        
        if isinstance(selected_item, RequirementFileNode) and selected_item in self._module_locker.locked_modules:
            self.MAIN.show_notification("Module is being downloaded from Doors. Please wait...")
            return
        
        self.form_edit_node = FormEditNode(selected_item, self)
    
    
    @pyqtSlot()
    def edit_node_response(self):
        self.MAIN.show_notification("Data Updated")
        self._display_values()
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
        import data_manager.form_validate_html_report
        from importlib import reload
        reload(data_manager.form_validate_html_report)
        
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
            if isinstance(file_node, RequirementFileNode) and file_node.coverage_filter:
                for k in file_node.coverage_dict.keys():
                    if k.lower() in html_report_string.lower():
                        covered_requirements.append(k)
                    else:
                        missing_requirements.append(k)

        # print("MISSING: ", "\n".join(missing_requirements))
        # print("COVERED: ", covered_requirements)

        self.form = data_manager.form_validate_html_report.FormValidatedHTMLReport(self, missing_requirements)

    @pyqtSlot(str)
    def doubleclicked_on_requirement_in_HTML_report_form(self, req_identifier: str):
        FOUND_NODE = None

        def find_node_by_reference(parent_node, reference):
            nonlocal FOUND_NODE
            for row in range(parent_node.rowCount()):
                node = parent_node.child(row)
                if node.reference.lower() == reference.lower():
                    # print(node)
                    # print("FOUND: ", node.reference)
                    FOUND_NODE = node
                    return node
                else:
                    find_node_by_reference(node, reference)


        for row in range(self.ROOT.rowCount()):
            node = self.ROOT.child(row)
            if isinstance(node, RequirementFileNode) and node.coverage_filter:
                find_node_by_reference(node, req_identifier)


        if FOUND_NODE:
            self.TREE.setCurrentIndex(FOUND_NODE.index())
            self.TREE.scrollTo(FOUND_NODE.index())
        else:
            dialog_message(self, "Module is missing.")        



        
    




   
####################################################################################################################
# COVERAGE CHECK --> PHYSICAL CHECK OF FILES ON DISK:
####################################################################################################################

# PATTERN_REQ_REFERENCE = re.compile(r"""(?:REFERENCE|\$REF:)\s*"(?P<req_reference>[\w\d,/\s\(\)-]+)"\s*""", re.IGNORECASE)
PATTERN_REQ_REFERENCE = re.compile(r'(?:REFERENCE|\$REF:)\s*"(?P<req_reference>.+)"\s*\$', re.IGNORECASE)

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
                    reference_list = PATTERN_REQ_REFERENCE.findall(text)

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