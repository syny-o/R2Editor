from pathlib import Path
from ui.model_editor_ui import Ui_Form
# from config.font import font
import json, re, os
from PyQt5.QtWidgets import QWidget, QFileDialog, QInputDialog, QMenu, QAction, QLineEdit, QShortcut, QTextEdit, QMessageBox, QStyle, QPushButton, QApplication, QListWidgetItem, QListWidget
from PyQt5.Qt import QStandardItemModel
from PyQt5.QtGui import QIcon, QCursor, QKeySequence, QTextCursor, QTextCharFormat, QColor
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QObject, QRunnable, QThreadPool, QPropertyAnimation, QEasingCurve
from data_manager.condition_nodes import ConditionFileNode, ConditionNode, ValueNode, TestStepNode
from data_manager.dspace_nodes import DspaceFileNode, DspaceDefinitionNode, DspaceVariableNode
from data_manager.a2l_nodes import A2lFileNode, A2lNode
from data_manager import a2l_nodes, condition_nodes, requirement_nodes, dspace_nodes
from data_manager.requirement_nodes import RequirementFileNode, RequirementNode
from data_manager.dlg_add_node import DlgAddNode
# from dialogs.form_add_req_module import AddRequirementsModule
from data_manager.form_add_module import FormAddModule
from data_manager.form_add_requirement_filter import FormAddCoverageFilter
# from dialogs.form_req_filter import RequirementFilter
from progress_bar.widget_modern_progress_bar import ModernProgressBar
from text_editor.completer import Completer
from components.droppable_tree_view import DroppableTreeView
from data_manager.req_text_edit import RequirementTextEdit
from text_editor.tooltips import tooltips
from text_editor.text_editor import TextEdit
from components.template_test_case import TemplateTestCase
from components.reduce_path_string import reduce_path_string
from dialogs.dialog_message import dialog_message
from doors.doors_connection import DoorsConnection
from components.my_list_widget import MyListWidget
from data_manager.widget_baseline import WidgetBaseline

from data_manager import model_manager
from data_manager import view_filter



class DataManager(QWidget, Ui_Form):

    send_file_path = pyqtSignal(Path)

    def __init__(self, main_window, project_manager):
        super().__init__()
        self.setupUi(self)
        self._hide_all_frames()

        self.MAIN = main_window
        self.PROJECT_MANAGER = project_manager
        
        self.MODEL = QStandardItemModel()
        self.ROOT = self.MODEL.invisibleRootItem()        
        self.ROOT.setData(self, Qt.UserRole)  # add pointer to DataManager instance to be accesseble from child nodes (ReqNode, CondNode, ...)

        # TREE:
        self.TREE = DroppableTreeView(self)
        self.ui_layout_tree.addWidget(self.TREE)
        self.TREE.setModel(self.MODEL)
        self.TREE.customContextMenuRequested.connect(self._context_menu) 
        self.TREE.clicked.connect(self._display_values)
        selection_model = self.TREE.selectionModel()
        selection_model.selectionChanged.connect(self._display_values)  # update line edits on Up/Down Arrows        

        QShortcut( 'Ctrl+Down', self.TREE ).activated.connect(lambda: self.move_node(direction='down'))
        QShortcut( 'Ctrl+Up', self.TREE ).activated.connect(lambda: self.move_node(direction='up'))
        QShortcut( 'Del', self.TREE ).activated.connect(self.remove_node)
        QShortcut( 'Ctrl+D', self.TREE ).activated.connect(self.duplicate_node)
        QShortcut( 'Ctrl+C', self.TREE ).activated.connect(self.copy_node)
        QShortcut( 'Ctrl+V', self.TREE ).activated.connect(self.paste_node)
        QShortcut( 'Insert', self.TREE ).activated.connect(self.add_node)
        QShortcut( 'Esc', self.TREE ).activated.connect(self._stop_filtering)
        QShortcut( 'Ctrl+S', self ).activated.connect(self.MAIN.project_save)
     

        self.progress_bar = ModernProgressBar('rgb(0, 179, 0)', 'COVERED')
        self.ui_layout_data_summary.addWidget(self.progress_bar)     

        self.uiLisWidgetModuleColumns = MyListWidget()
        self.uiLisWidgetModuleColumns.setEnabled(False)
        self.uiLayoutModuleColumns.addWidget(self.uiLisWidgetModuleColumns)

        self.uiLisWidgetModuleAttributes = MyListWidget(context_menu=False)
        # self.uiLisWidgetModuleAttributes.setEnabled(False)
        self.uiLayoutModuleAttributes.addWidget(self.uiLisWidgetModuleAttributes)

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
        self.action_update_requirements.triggered.connect(lambda: self._update_requirements(False))

        self.action_remove = QAction(QIcon(u"ui/icons/16x16/cil-x.png"), 'Remove')
        self.action_remove.triggered.connect(self.remove_node)
        self.action_remove.setShortcut('Del')

        self.action_edit = QAction('Edit')
        self.action_edit.setIcon(QIcon(u"ui/icons/16x16/cil-pencil.png"))
        self.action_edit.triggered.connect(self.edit_node)

        self.action_duplicate = QAction('Duplicate')
        self.action_duplicate.setIcon(QIcon(u"ui/icons/16x16/cil-clone.png"))
        self.action_duplicate.triggered.connect(self.duplicate_node)
        self.action_duplicate.setShortcut(QKeySequence("Ctrl+D"))
        
        self.action_add = QAction('Add')
        self.action_add.setIcon(QIcon(u"ui/icons/16x16/cil-plus.png"))
        self.action_add.triggered.connect(self.add_node) 
        self.action_add.setShortcut(QKeySequence("Insert")) 

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

        self.action_show_only_requirements_with_coverage = QAction('Show Not Covered + Covered')
        self.action_show_only_requirements_with_coverage.triggered.connect(self._show_only_items_with_coverage)
        self.action_show_only_requirements_not_covered = QAction('Show Not Covered')
        self.action_show_only_requirements_not_covered.triggered.connect(self._show_only_items_not_covered)        
        self.action_show_all_requirements = QAction('Show All')
        self.action_show_all_requirements.setIcon(QIcon(u"ui/icons/24x24/cil-check-alt.png"))
        self.action_show_all_requirements.triggered.connect(self._show_all_items)        

        self.action_remove_coverage_filter = QAction(QIcon(u"ui/icons/16x16/cil-wifi-signal-off.png"), "Remove Coverage Filter")
        self.action_remove_coverage_filter.triggered.connect(self._remove_coverage_filter)        

        self.action_add_to_ignore_list = QAction(QIcon(u"ui/icons/16x16/cil-task.png"), "Add To Ignore List")
        self.action_add_to_ignore_list.triggered.connect(self._add_to_ignore_list)
        self.action_remove_from_ignore_list = QAction(QIcon(u"ui/icons/16x16/cil-external-link.png"), "Remove From Ignore List")
        self.action_remove_from_ignore_list.triggered.connect(self._remove_from_ignore_list)        
        ################## ACTIONS END ###########################


        # FUNCTIONAL PART:
        # self.MODEL.itemChanged.connect(lambda: self.set_project_saved(False))
        self.MODEL.rowsInserted.connect(lambda: self.set_project_saved(False))
        self.MODEL.rowsRemoved.connect(lambda: self.set_project_saved(False))

        self.ui_remove.clicked.connect(self.remove_node)
        self.ui_add.clicked.connect(self.add_node)
        self.ui_add.setShortcut('Ctrl+n')
        self.ui_duplicate.clicked.connect(self.duplicate_node)
        self.ui_edit.clicked.connect(self.edit_node)
        self.ui_edit.setShortcut('F4')
        self.ui_edit.setToolTip("F4")
        self.ui_export.clicked.connect(self.tree_2_file)
        self.ui_update_requirements.clicked.connect(lambda: self._update_requirements(True))
        self.ui_new_requirements.clicked.connect(self._add_req_node)
        self.ui_check_coverage.clicked.connect(self._create_dict_from_scripts_for_coverage_check)
        self.ui_check_html_report.clicked.connect(self.check_HTML_report)
        self.ui_le_filter.textChanged.connect(self._filter_items)
        self.ui_le_filter.textEdited.connect(self._reset_filter)
        self.ui_btn_goBack.clicked.connect(self._goto_previous_index)

        self.send_data_2_completer()
        self._update_data_summary()


        # node copied into memory by action COPY
        self.node_to_paste = None

        self.send_file_path.connect(main_window.file_open_from_tree)
        self.ui_lw_file_paths_coverage.itemDoubleClicked.connect(self._doubleclick_on_tc_reference)
        self.ui_lw_outlinks.itemDoubleClicked.connect(self._doubleclick_on_outlink)
        self.uiListWidgetModuleIgnoreList.itemDoubleClicked.connect(self._doubleclick_on_ignored_reference)

        # BASELINE LIST WIDGET
        self.widget_baseline = WidgetBaseline()
        self.uiLayoutModuleAllBaselines.addWidget(self.widget_baseline)


        # REQUIREMENT TEXT IMPROVEMENT
        self.ui_requirement_text = RequirementTextEdit(self.MAIN)
        self.ui_layout_req_text.addWidget(self.ui_requirement_text)


        # COPY TO CLIPBOAR FEATURE
        self.ui_btnCopyReqRef.clicked.connect(self._copy_to_clipboard)


        # POINTER TO REQ MODULE WHEN ONLY ONE IS DOWNLOADING
        self._module_which_is_currently_donwnloaded = None

        # FLAG FOR DETERMINING IF DOWNLOADING REQUIREMENTS IS IN PROGRESS
        self.downloading_of_requirements_is_in_progress = False

        # EDITING --> BUTTON EDIT
        self.ui_components_for_editing = [
            self.uiTextEditRequirementNote, 
            self.uiLineEditModulePath, self.uiLisWidgetModuleColumns,
            self.ui_ts_name, self.ui_ts_action, self.ui_ts_comment, self.ui_ts_nominal,
            self.ui_cond_name, self.ui_cond_category,
            self.ui_val_name, self.ui_val_category,
            self.ui_ds_name, self.ui_ds_path, self.ui_ds_value, 
        ] 


        # SPECIAL THREAD FOR COVERAGE CHECK
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(1)        


    @pyqtSlot(bool, str)
    def update_progress_status(self, is_visible, text=''):
        self.ui_frame_progress_status.setMinimumHeight(30) if is_visible else self.ui_frame_progress_status.setMinimumHeight(0)
        self.ui_label_progress_status.setText(text)



    def receive_data_from_drop_or_file_manager(self, data):
        condition_nodes.initialise(data, self.ROOT)
        dspace_nodes.initialise(data, self.ROOT)
        a2l_nodes.initialise(data, self.ROOT)
        self.MAIN.show_notification(f"Model has been updated.")   
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
                    current_node.tree_2_file()        
        return data





    #####################################################################################################################################################
    #   ADDING REQUIREMENT MODULE
    #####################################################################################################################################################

    @pyqtSlot(str, list)
    def receive_data_from_add_req_module_dialog(self, module_path, columns_names):
        r = RequirementFileNode(self.ROOT, module_path, columns_names, attributes=[], baseline={}, coverage_filter=None, coverage_dict=None, update_time=None, ignore_list=None, notes=None, current_baseline=None)
        self.ROOT.appendRow(r)


    def _add_req_node(self):
        self.form_add_req_module = FormAddModule(self)
        self.form_add_req_module.show()
        # from importlib import reload
        # self.ui_layout_req_text.removeWidget(self.ui_requirement_text)
        # reload(data_manager.req_text_edit)
        # self.ui_requirement_text = data_manager.req_text_edit.RequirementTextEdit(self.main_window)
        # self.ui_layout_req_text.addWidget(self.ui_requirement_text)



    #####################################################################################################################################################
    #   CONNECTING AND DOWNLOADING DATA FROM DOORS
    #####################################################################################################################################################


    def _send_request_2_doors(self, password, paths, columns_names, baselines):
        DoorsConnection(self, paths, columns_names, baselines, self, password)
        self.downloading_of_requirements_is_in_progress = True
        self.update_progress_status(True, 'Initialising...')
        


    def _update_requirements(self, is_multiple_modules):
        # 1. Check if at least one req. module is present
        requirements_file_nodes_present = False
        for row in range(self.ROOT.rowCount()):
            node = self.ROOT.child(row)
            if isinstance(node, RequirementFileNode):
                requirements_file_nodes_present = True

        # 2. If some module is present --> get username/password
        if requirements_file_nodes_present:
            passwd_from_input_dlg, ok = QInputDialog.getText(
                None, 
                "Doors Connection", 
                f"Database: {self.MAIN.app_settings.doors_database_path}\nUsername: {self.MAIN.app_settings.doors_user_name}\n\nEnter your password:", QLineEdit.Password)

            if ok and passwd_from_input_dlg:            
                # if Button from Upper Menu was pushed (Update All Requirements)
                if is_multiple_modules:
                    paths = []
                    columns = []
                    baselines = []
                    for row in range(self.ROOT.rowCount()):
                        node = self.ROOT.child(row)
                        if isinstance(node, RequirementFileNode):
                            paths.append(node.path)
                            columns.append(node.columns_names)
                            baselines.append(node.current_baseline)
                    
                    if paths and columns and baselines:
                        self._send_request_2_doors(passwd_from_input_dlg, paths, columns, baselines)
                        
                # if Right Click on Module --> Update Requirements (Update Module)
                else:
                    selected_item_index = self.TREE.currentIndex()
                    selected_item = self.MODEL.itemFromIndex(selected_item_index)
                    if isinstance(selected_item, RequirementFileNode):
                        self._send_request_2_doors(passwd_from_input_dlg, [selected_item.path,], [selected_item.columns_names,], [selected_item.current_baseline,])
                        self._module_which_is_currently_donwnloaded = selected_item
                        




    def receive_data_from_doors(self, doors_output, timestamp):
        self.downloading_of_requirements_is_in_progress = False
        if not doors_output:
            self.MAIN.show_notification(f"Error: No data received.") 
            return

        if self._module_which_is_currently_donwnloaded:
            self._module_which_is_currently_donwnloaded.receive_data_from_doors(doors_output, timestamp)
            self._module_which_is_currently_donwnloaded = None
            return

        for row in range(self.ROOT.rowCount()):
            node = self.ROOT.child(row)
            if isinstance(node, RequirementFileNode):
                node.receive_data_from_doors(doors_output, timestamp)

        
        self.MAIN.show_notification(f"Requirements have been Updated.") 
        self._display_values()
        self._update_data_summary()

        self.set_project_saved(False)


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
            # print("START COVERAGE CHECK")
            self.ui_check_coverage.setEnabled(False)        
            worker = Worker(self)
            self.threadpool.start(worker)


    @pyqtSlot(dict)
    def check_coverage(self, file_content_dict):
        if self.PROJECT_MANAGER.disk_project_path():
            for row in range(self.ROOT.rowCount()):
                current_item = self.ROOT.child(row)
                if isinstance(current_item, RequirementFileNode):
                    change = current_item.check_coverage_with_file_pointers(file_content_dict)
                    if change:
                        self.set_project_saved(False)
            self._update_data_summary()
            self.ui_check_coverage.setEnabled(True)

            


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
                
        self.progress_bar.update_value(calculated_number, covered_number)
        self.ui_lab_req_total.setText(str(calculated_number))
        self.ui_lab_req_covered.setText(str(covered_number))
        self.ui_lab_req_not_covered.setText(str(calculated_number-covered_number))

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
    def receive_data_from_req_filter_dialog(self, filter_string):
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

    def _expand_all_children(self):
        selected_item_index = self.TREE.currentIndex()
        self.TREE.expandRecursively(selected_item_index)

    def _collapse_all_children(self):
        selected_item_index = self.TREE.currentIndex()
        selected_item = self.MODEL.itemFromIndex(selected_item_index)
        
        def _browse_children(node):         
            for row in range(node.rowCount()):
                requirement_node = node.child(row)
                requirement_node_index = requirement_node.index()
                self.TREE.collapse(requirement_node_index)

                _browse_children(requirement_node)        
        
        _browse_children(selected_item)
        self.TREE.collapse(selected_item_index)



    def _copy_to_clipboard(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.ui_requirement_id.text(), mode=cb.Clipboard)
        self.MAIN.show_notification(f"Item {self.ui_requirement_id.text()} copied to Clipboard.")  



    def _make_ui_components_editable(self):
        for c in self.ui_components_for_editing:
            if isinstance(c, (QLineEdit, QTextEdit)): c.setReadOnly(False)
            if isinstance(c, QListWidget): c.setEnabled(True) 
            c.setStyleSheet("background-color: rgb(20, 20, 120);")

    def _make_ui_components_not_editable(self):
        for c in self.ui_components_for_editing:
            if isinstance(c, (QLineEdit, QTextEdit)): c.setReadOnly(True)  
            if isinstance(c, QListWidget): c.setEnabled(False) 
            c.setStyleSheet("background-color: rgb(33, 37, 43);")
            if isinstance(c, QTextEdit):
                c.setStyleSheet("background-color: rgb(33, 37, 43); color: rgb(190, 190, 190); font-style: italic")


    def _hide_all_frames(self):
        # Common Area
        self.ui_frame_file.setVisible(False)
        self.frame_10.setVisible(False)
        # Condition Area
        self.ui_frame_cond.setVisible(False)
        # self.ui_frame_cond.setFont(font)
        self.ui_frame_value.setVisible(False)
        self.ui_frame_ts.setVisible(False)
        # dSpace Area
        self.ui_frame_dspace_definition.setVisible(False)
        self.ui_frame_dspace_variable.setVisible(False)
        # A2L Area
        self.ui_frame_a2l_variable.setVisible(False)
        # Requirement Area
        self.ui_frame_requirement.setVisible(False)
        # RequirementFileNode Area
        self.uiFrameRequirementModule.setVisible(False)

    def _disable_all_buttons(self):
        self.ui_add.setEnabled(False)
        self.ui_edit.setEnabled(False)
        self.ui_remove.setEnabled(False)
        self.ui_duplicate.setEnabled(False)
        self.ui_export.setEnabled(False)
        self.ui_update_requirements.setEnabled(True)


    def _show_filter_input(self, show):
        start_width = self.ui_le_filter.width()
        final_width = 8000 if show else 0
        self.animation = QPropertyAnimation(self.ui_le_filter, b"maximumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(start_width)
        self.animation.setEndValue(final_width)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.start()


    def _display_values(self):
        self._hide_all_frames()
        self._disable_all_buttons()
        # self.ui_le_filter.setEnabled(False)
        # self.ui_le_filter.setVisible(False)
        self._show_filter_input(False)
        self.ui_frame_requirement.setEnabled(True)
        # self.ui_group_box_all_frames.setEnabled(False)


        selected_item_index = self.TREE.currentIndex()
        selected_item = self.MODEL.itemFromIndex(selected_item_index)

        # Recover last filter if there is some
        if selected_item:
            self.ui_le_filter.setText(selected_item.data(Qt.UserRole))
            

        # ConditionFileNode, DspaceFileNode, A2lFileNode
        if isinstance(selected_item, (ConditionFileNode, DspaceFileNode, A2lFileNode)):
            # self.ui_le_filter.setEnabled(True)
            self._show_filter_input(True)
            self.ui_frame_file.setVisible(True)
            self.ui_file_path.setText(selected_item.path)
            if isinstance(selected_item, (ConditionFileNode, DspaceFileNode)):
                # Buttons:
                self.ui_export.setEnabled(True)  
                self.ui_remove.setEnabled(True)          

        # RequirementFileNode
        elif isinstance(selected_item, RequirementFileNode):
            # self.ui_le_filter.setEnabled(True)
            # self.ui_le_filter.setVisible(True)
            self._show_filter_input(True)
            self.uiFrameRequirementModule.setVisible(True)
            self.uiLineEditModulePath.setText(selected_item.path)
            self.uiLineEditUpdateTime.setText(str(selected_item.timestamp))

            self.uiTextEditModuleBaseline.clear()
            # baseline_text = ""
            # for attr, value in selected_item.baseline.items():
            #     self.uiTextEditModuleBaseline.insertHtml(f'<span style="color: rgb(150, 150, 150);">{attr.capitalize()}:</span>  <span> {value}</span><br>')
            # self.uiTextEditModuleBaseline.setPlainText(baseline_text)

            # BASELINES
            self.widget_baseline.update(selected_item)

            # IGNORE LIST
            self.uiListWidgetModuleIgnoreList.clear()
            for item in selected_item.ignore_list:
                ignore_lw_item = QListWidgetItem()    
                ignore_lw_item.setData(Qt.DisplayRole, reduce_path_string(item))
                ignore_lw_item.setData(Qt.UserRole, item)
                # ignore_lw_item.setData(Qt.DecorationRole, QIcon(u"ui/icons/20x20/cil-task.png"))
                ignore_lw_item.setData(Qt.ToolTipRole, self._get_tooltip_from_link(f"{selected_item.path}:{item.split('_')[-1]}"))
                self.uiListWidgetModuleIgnoreList.insertItem(0, ignore_lw_item)


            self.uiLineEditModuleCoverageFilter.setText(str(selected_item.coverage_filter))
            # Buttons:
            self.ui_update_requirements.setEnabled(True)
            self.ui_remove.setEnabled(True)
            self.ui_edit.setEnabled(True)


            self.uiLisWidgetModuleColumns.clear()
            self.uiLisWidgetModuleColumns.insertItems(0, selected_item.columns_names)

            self.uiLisWidgetModuleAttributes.clear()
            self.uiLisWidgetModuleAttributes.insertItems(0, selected_item.attributes)            

        # Condition Area
        elif isinstance(selected_item, ConditionNode):
            self.ui_frame_cond.setVisible(True)
            self.ui_cond_name.setText(selected_item.name)
            self.ui_cond_category.setText(selected_item.category)

            # Buttons:
            self.ui_edit.setEnabled(True)
            self.ui_add.setEnabled(True)
            self.ui_remove.setEnabled(True)
        elif isinstance(selected_item, ValueNode):
            self.ui_frame_value.setVisible(True)
            self.ui_val_name.setText(selected_item.name)
            self.ui_val_category.setText(selected_item.category)

            # Buttons:
            self.ui_edit.setEnabled(True)
            self.ui_add.setEnabled(True)
            self.ui_remove.setEnabled(True)
        elif isinstance(selected_item, TestStepNode):
            self.ui_frame_ts.setVisible(True)
            self.ui_ts_name.setText(selected_item.name)
            self.ui_ts_action.setText(selected_item.action)
            self.ui_ts_comment.setText(selected_item.comment)
            self.ui_ts_nominal.setText(selected_item.nominal)

            # Buttons:
            self.ui_edit.setEnabled(True)
            self.ui_add.setEnabled(True)
            self.ui_remove.setEnabled(True)
            self.ui_duplicate.setEnabled(True)

        # dSpace Area
        elif isinstance(selected_item, DspaceDefinitionNode):
            self.ui_frame_dspace_definition.setVisible(True)
            self.ui_ds_definition.setText(selected_item.name)
        elif isinstance(selected_item, DspaceVariableNode):
            self.ui_frame_dspace_variable.setVisible(True)
            self.ui_ds_name.setText(selected_item.name)
            self.ui_ds_value.setText(selected_item.value)
            self.ui_ds_path.setText(selected_item.path)

            # Buttons:
            self.ui_edit.setEnabled(True)
            self.ui_add.setEnabled(True)
            self.ui_remove.setEnabled(True)
            self.ui_duplicate.setEnabled(True)
        # A2L Area
        elif isinstance(selected_item, A2lNode):
            self.ui_frame_a2l_variable.setVisible(True)
            self.ui_a2l_name.setText(selected_item.name)
            self.ui_a2l_address.setText(selected_item.address)

        ####################################################################
        # REQUIREMENT AREA #################################################
        ####################################################################
        elif isinstance(selected_item, RequirementNode):
            
            self.ui_frame_requirement.setVisible(True)

            self.ui_requirement_id.setText(selected_item.reference)
            self.ui_requirement_covered.setText(str(selected_item.is_covered))
            text_to_display = ''
            columns_data = selected_item.columns_data
            columns_names = selected_item.MODULE.columns_names_backup

            # COLUMNS NAMES + DATA
            for i in range(len(columns_names)):
                text_to_display += f'<{columns_names[i]}>:\n{columns_data[i]} \n\n'
            self.ui_requirement_text.setPlainText(text_to_display)

            # Buttons:
            self.ui_edit.setEnabled(True)
            # Frame
            self.ui_frame_requirement.setEnabled(True)
            # OUTLINKS
            self.ui_lw_outlinks.clear()                        
            for outlink in selected_item.outlinks:
                outlink_lw_item = QListWidgetItem()
                outlink_lw_item.setData(Qt.DisplayRole, reduce_path_string(outlink))
                outlink_lw_item.setData(Qt.UserRole, outlink)
                outlink_lw_item.setData(Qt.DecorationRole, QIcon(u"ui/icons/20x20/cil-arrow-right.png"))
                outlink_lw_item.setData(Qt.ToolTipRole, self._get_tooltip_from_link(outlink))
                self.ui_lw_outlinks.addItem(outlink_lw_item)
            # INLINKS
            for inlink in selected_item.inlinks:
                inlink_lw_item = QListWidgetItem()
                inlink_lw_item.setData(Qt.DisplayRole, reduce_path_string(inlink))
                inlink_lw_item.setData(Qt.UserRole, inlink)
                inlink_lw_item.setData(Qt.ToolTipRole, self._get_tooltip_from_link(inlink))
                inlink_lw_item.setData(Qt.DecorationRole, QIcon(u"ui/icons/20x20/cil-arrow-left.png"))
                self.ui_lw_outlinks.addItem(inlink_lw_item)                   
            # FILE REFERENCES
            self.ui_lw_file_paths_coverage.clear()            
            for file_reference in selected_item.file_references:
                ref_lw_item = QListWidgetItem()
                ref_lw_item.setData(Qt.DisplayRole, reduce_path_string(file_reference))
                ref_lw_item.setData(Qt.UserRole ,file_reference)
                self.ui_lw_file_paths_coverage.addItem(ref_lw_item)  

            # NOTES
            self.uiTextEditRequirementNote.clear()
            self.uiTextEditRequirementNote.setPlainText(selected_item.get_note())

            ## FILTER --> HIGHLIGHT FINDINGS WITH RED COLOR
            filter_text = selected_item.MODULE.data(Qt.UserRole)
            if filter_text:
                text_edit_content = self.ui_requirement_text.toPlainText()
                for match in re.finditer(filter_text, text_edit_content, re.IGNORECASE):
                    # print('%02d-%02d: %s' % (m.start(), m.end(), m.group(0)))
                    tc = self.ui_requirement_text.textCursor()
                    tc.setPosition(match.start())
                    for _ in range(match.end() - match.start()):
                        tc.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor)
                    f = QTextCharFormat()
                    f.setBackground(QColor(255, 0, 0))
                    # f.setForeground(Qt.black)
                    tc.setCharFormat(f)



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
                    if node.get_note():
                        FOUND_LINK_TEXT += f"\n\n<User Note>: {node.get_note()}"
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
                    # print(node)
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
            # self._update_previous_indexes(FOUND_NODE.index())
        else:
            dialog_message(self, "Module is missing.")


    def _goto_previous_index(self):
        self.TREE.goto_previous_index()


    def _doubleclick_on_tc_reference(self, list_item_text):
        file_path_string = list_item_text.data(Qt.UserRole)
        self.send_file_path.emit(Path(file_path_string))
        self.MAIN.manage_right_menu(self.MAIN.tabs_splitter, self.MAIN.ui_btn_text_editor)


    def _create_tc_template_with_req_reference(self, is_testable):
        selected_item_index = self.TREE.currentIndex()
        selected_item = self.MODEL.itemFromIndex(selected_item_index)

        if isinstance(selected_item, RequirementNode):
            template = TemplateTestCase(req_id=selected_item.columns_data[0], req_text=selected_item.columns_data[-1], is_testable=is_testable)
            # print(template.generate_tc_template())
            text = template.generate_tc_template()
            file_path = None
            tab_name = 'Untitled'
            self.MAIN.left_tabs.addTab(TextEdit(self.MAIN, text, file_path), QIcon(u"ui/icons/16x16/cil-description.png"), tab_name)
            self.MAIN.actual_text_edit.setFocus()
            self.MAIN.manage_right_menu(self.MAIN.tabs_splitter, self.MAIN.ui_btn_text_editor)            








    def _context_menu(self, point):
        selected_item_index = self.TREE.indexAt(point)
        # selected_item_index = self.TREE.currentIndex()
        selected_item = self.MODEL.itemFromIndex(selected_item_index)

        if not selected_item_index.isValid():
            return

        menu = QMenu()
        menu.setStyleSheet("QMenu::separator {height: 0.5px; margin: 3px; background-color: rgb(38, 59, 115);}")

        menu.addAction(self.action_expand_all_children)
        menu.addAction(self.action_collapse_all_children)
        menu.addSeparator()
        if isinstance(selected_item, RequirementFileNode) and selected_item.coverage_filter:
            
            if not selected_item.data(Qt.UserRole):
                self._evaluate_view_filter()
                menu.addAction(self.action_show_only_requirements_not_covered)                 
                menu.addAction(self.action_show_only_requirements_with_coverage)                   
                menu.addAction(self.action_show_all_requirements)
                menu.addSeparator()
                menu.addAction(self.action_edit_coverage_filter)
                menu.addAction(self.action_remove_coverage_filter)          

        if isinstance(selected_item, RequirementFileNode):
            if not selected_item.data(Qt.UserRole):
                if not selected_item.coverage_filter:
                    menu.addSeparator()
                    menu.addAction(self.action_open_coverage_filter)
                menu.addSeparator()
                menu.addAction(self.action_update_requirements)

        elif isinstance(selected_item, (ConditionFileNode, DspaceFileNode)):
            menu.addAction(self.action_save)
        elif isinstance(selected_item, (ConditionNode, ValueNode, TestStepNode, DspaceVariableNode)):
            menu.addActions([self.action_add,])
        
       

        if selected_item.parent() and not isinstance(selected_item, (A2lNode, RequirementNode)): 
            menu.addAction(self.action_move_up)
            menu.addAction(self.action_move_down)
            menu.addSeparator()

        if isinstance(selected_item, RequirementNode):
            menu.addAction(self.action_create_testable_tc_template_with_req_reference)
            menu.addAction(self.action_create_not_testable_tc_template_with_req_reference)
            if not selected_item.hasChildren():
                if selected_item.reference in selected_item.MODULE.ignore_list:                
                    menu.addAction(self.action_remove_from_ignore_list)
                elif selected_item.is_covered == False:
                    menu.addAction(self.action_add_to_ignore_list)
            menu.addSeparator()            

        if isinstance(selected_item, (TestStepNode, ValueNode, ConditionNode)):
            menu.addAction(self.action_duplicate)
            menu.addSeparator()      

        if isinstance(selected_item, A2lFileNode):
            menu.addAction(self.action_normalise_a2l_file)                  
        
        if hasattr(selected_item, 'get_node_copy'):
            menu.addSeparator()
            menu.addAction(self.action_copy)

        if self.node_to_paste and type(self.node_to_paste) == type(selected_item):
            menu.addAction(self.action_paste)

        if not isinstance(selected_item, (DspaceDefinitionNode, A2lNode, RequirementNode)):
            menu.addSeparator()
            menu.addAction(self.action_remove)

        menu.exec_(QCursor().pos())
















##############################################################################################################################
# TEXT FILTER (ONLY VIEW AFFECTING
##############################################################################################################################

    def _stop_filtering(self):
        view_filter.stop_filtering(self.TREE, self.MODEL)


    def _reset_filter(self, filtered_text):
        view_filter.reset_filter(self.TREE, self.MODEL, filtered_text)


    def _filter_items(self, filtered_text):
        view_filter.filter_items(self.TREE, self.MODEL, filtered_text)
        
        if filtered_text:            
            self.ui_le_filter.setStyleSheet(""" background-color: rgb(220, 220, 220);
                                                background-image: url(:/16x16/icons/16x16/cil-magnifying-glass.png);
                                                background-position: left center;
                                                background-repeat: no-repeat;
                                                padding-left: 20px;
                                                color: rgb(20, 20, 20);
                                                font-size: 18px;
                                                font-weight: bold;
                                                 """)

        else:
            self.ui_le_filter.setStyleSheet(""" background-color: rgb(35, 35, 25);
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
        index = self.TREE.currentIndex()
        requirement_file_node = self.MODEL.itemFromIndex(index)
        self.action_show_all_requirements.setIcon(QIcon())
        self.action_show_only_requirements_not_covered.setIcon(QIcon())
        self.action_show_only_requirements_with_coverage.setIcon(QIcon())
        view_filter = requirement_file_node.view_filter
        if view_filter == "all":
            self.action_show_all_requirements.setIcon(QIcon(u"ui/icons/24x24/cil-check-alt.png"))
        elif view_filter == "not_covered":
            self.action_show_only_requirements_not_covered.setIcon(QIcon(u"ui/icons/24x24/cil-check-alt.png"))
        else:
            self.action_show_only_requirements_with_coverage.setIcon(QIcon(u"ui/icons/24x24/cil-check-alt.png"))              




        



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
        import data_manager.form_a2l_norm_report
        from importlib import reload
        reload(data_manager.form_a2l_norm_report)
        # from data_manager.form_a2l_norm_report import A2lNormReport
        self.form = data_manager.form_a2l_norm_report.A2lNormReport(data_4_report, missing_signals, duplicated_signals)
        self.form.show()






    ####################################################################################################################
    # ADDING / MODIFYING / REMOVING / EXPORTING NODES DATA:
    ####################################################################################################################


    def tree_2_file(self):
        model_manager.export_file(self.TREE, self.MODEL)

    def remove_node(self):
        result = model_manager.remove_node(self.TREE, self.MODEL)
        message = "Item Removed" if result else "Last Item can not be Removed"
        self.MAIN.show_notification(message)  
        self.send_data_2_completer()
        self._update_data_summary()                    
            
    
    def add_node(self):
        selected_item_index = self.TREE.currentIndex()
        selected_item = self.MODEL.itemFromIndex(selected_item_index)

        if isinstance(selected_item, ConditionNode):
            self.window = DlgAddNode(self, condition_data=[None, None])
            self.window.show()

        elif isinstance(selected_item, ValueNode):
            condition = selected_item.parent().name
            self.window = DlgAddNode(self, condition_data=[condition, None])
            self.window.show()

        elif isinstance(selected_item, TestStepNode):
            condition = selected_item.parent().parent().name
            value = selected_item.parent().name
            self.window = DlgAddNode(self, condition_data=[condition, value])
            self.window.show()

        elif isinstance(selected_item, DspaceVariableNode):
            definition = selected_item.parent().name
            self.window = DlgAddNode(self, dspace_data=definition)
            self.window.show()
        

    def duplicate_node(self):
        model_manager.duplicate_node(self.TREE, self.MODEL)
        self.MAIN.show_notification(f"Item was duplicated.")  

    def copy_node(self):
        self.node_to_paste = model_manager.copy_node(self.TREE, self.MODEL)        
        if self.node_to_paste: 
            self.MAIN.show_notification(f"Item was copied to Clipboard.")  


    def paste_node(self):
        success = model_manager.paste_node(self.TREE, self.MODEL, self.node_to_paste)
        if success:
            self.MAIN.show_notification(f"Item {self.node_to_paste.text()} was inserted.") 
        self.send_data_2_completer


    def edit_node(self, button_is_checked):
        selected_item_index = self.TREE.currentIndex()
        selected_item = self.MODEL.itemFromIndex(selected_item_index)

        if not selected_item:
            return

        if button_is_checked:
            self.TREE.setEnabled(False)
            self._make_ui_components_editable()

        else:            
            self.TREE.setEnabled(True)
            self._make_ui_components_not_editable()
            
            # Save changes:
            if isinstance(selected_item, ConditionNode):
                selected_item.name = self.ui_cond_name.text()
                selected_item.setText(selected_item.name)
            elif isinstance(selected_item, ValueNode):
                selected_item.name = self.ui_val_name.text()
                selected_item.setText(selected_item.name)
            elif isinstance(selected_item, TestStepNode):
                selected_item.name = self.ui_ts_name.text()
                selected_item.action = self.ui_ts_action.text()
                selected_item.setText(selected_item.action)
                selected_item.comment = self.ui_ts_comment.text()
                selected_item.nominal = self.ui_ts_nominal.text()

            elif isinstance(selected_item, DspaceVariableNode):
                selected_item.name = self.ui_ds_name.text()
                selected_item.setText(selected_item.name)
                selected_item.value = self.ui_ds_value.text()
                selected_item.path = self.ui_ds_path.text()

            elif isinstance(selected_item, RequirementFileNode):
                selected_item.path = self.uiLineEditModulePath.text()
                selected_item.setText(reduce_path_string(selected_item.path))
                self.uiLisWidgetModuleColumns.setEnabled(False)
                self.uiListWidgetModuleIgnoreList.setEnabled(True)
                selected_item.columns_names = self.uiLisWidgetModuleColumns.get_all_items()

            elif isinstance(selected_item, RequirementNode):
                note = self.uiTextEditRequirementNote.toPlainText()
                selected_item.update_note(note)
            
            if hasattr(selected_item, 'get_file_node'):
                selected_item.get_file_node().set_modified(True)

            
            self.send_data_2_completer()
            self.MAIN.show_notification(f"Item {selected_item.text()} has been updated.")            
            self.set_project_saved(False)




    def receive_data_from_add_node_dialog(self, data: dict):    
        model_manager.insert_node(self.TREE, self.MODEL, data)
        self.MAIN.show_notification(f"Item has been inserted to Tree.") 
        self.send_data_2_completer()



    def move_node(self, direction):
        model_manager.move_node(self.TREE, self.MODEL, direction)
        self.send_data_2_completer()
        self.set_project_saved(False)




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
            # self._update_previous_indexes(FOUND_NODE.index())
        else:
            dialog_message(self, "Module is missing.")        



        
    




   
####################################################################################################################
# COVERAGE CHECK --> PHYSICAL CHECK OF FILES ON DISK:
####################################################################################################################

PATTERN_REQ_REFERENCE = re.compile(r"""(?:REFERENCE|\$REF:)\s*"(?P<req_reference>[\w\d,/\s\(\)-]+)"\s*""", re.IGNORECASE)

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