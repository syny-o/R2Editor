from pathlib import Path
from ui.model_editor_ui import Ui_Form
from config.font import font
import json, re, os
from PyQt5.QtWidgets import QWidget, QLabel, QInputDialog, QMenu, QAction, QLineEdit, QShortcut, QTextEdit, QMessageBox, QStyle, QPushButton, QApplication, QListWidgetItem, QListWidget
from PyQt5.Qt import QStandardItemModel
from PyQt5.QtGui import QIcon, QCursor, QKeySequence, QTextCursor, QTextCharFormat, QColor
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QObject, QRunnable, QThreadPool
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

import data_manager.req_text_edit


class DataManager(QWidget, Ui_Form):

    send_project_path = pyqtSignal(str)

    send_file_path = pyqtSignal(str)

    

    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)

        self.main_window = main_window

        self.lab_project_files.setVisible(False)
        self.lab_requirements.setVisible(False)

        # SETTINGS FROM DISK
        # self.settings = QSettings(r'.\config\configuration.ini', QSettings.IniFormat)
        self.settings = main_window.app_settings

        # MODEL PART:
        self.model = QStandardItemModel()
        # self.model.rowsInserted.connect(self.send_data_2_completer)
        # self.model.rowsRemoved.connect(self.send_data_2_completer)
        # self.model.itemChanged.connect(self.send_data_2_completer)  # finally cancelled because of Requirement Coverage (changing Icon triggeres this signal)
        self.ROOT = self.model.invisibleRootItem()
        
        self.ROOT.setData(self, Qt.UserRole)  # add pointer to DataManager instance to be accesseble from child nodes (ReqNode, CondNode, ...)
        # print(self.ROOT.data(Qt.UserRole))
        self._disk_project_path = None
        self.is_project_saved = True


        # VIEW PART:
        self.ui_tree_view = DroppableTreeView(self)
        self.ui_layout_tree.addWidget(self.ui_tree_view)
        self.ui_tree_view.setHeaderHidden(True)
        self.ui_tree_view.setFont(font)
        self.ui_group_box_all_frames.setEnabled(True)
        self.ui_tree_view.setModel(self.model)
        self.ui_tree_view.setExpandsOnDoubleClick(True)
        self.ui_tree_view.setAnimated(True)
        self._hide_all_frames()

        self.uiLisWidgetModuleColumns = MyListWidget()
        self.uiLisWidgetModuleColumns.setEnabled(False)
        self.uiLayoutModuleColumns.addWidget(self.uiLisWidgetModuleColumns)

        self.uiLisWidgetModuleAttributes = MyListWidget()
        # self.uiLisWidgetModuleAttributes.setEnabled(False)
        self.uiLayoutModuleAttributes.addWidget(self.uiLisWidgetModuleAttributes)





        ################## CONTEXT MENU START ###########################
        self.ui_tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui_tree_view.customContextMenuRequested.connect(self._context_menu)  
        # CONTEXT MENU ACTIONS:  

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
        self.action_update_requirements.triggered.connect(lambda: self.update_requirements(False))

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
        self.action_normalise_a2l_file.triggered.connect(self.normalise_a2l_file)  

        self.action_open_coverage_filter = QAction(QIcon(u"ui/icons/16x16/cil-wifi-signal-2.png"), 'Set Coverage Filter')
        self.action_open_coverage_filter.triggered.connect(self._open_form_for_coverage_filter) 

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
        ################## CONTEXT MENU END ###########################

        ################## TreeView Shortcuts START ##########################
        QShortcut( 'Ctrl+Down', self.ui_tree_view ).activated.connect(lambda: self.move_node(direction='down'))
        QShortcut( 'Ctrl+Up', self.ui_tree_view ).activated.connect(lambda: self.move_node(direction='up'))
        QShortcut( 'Del', self.ui_tree_view ).activated.connect(self.remove_node)
        QShortcut( 'Ctrl+D', self.ui_tree_view ).activated.connect(self.duplicate_node)
        QShortcut( 'Ctrl+C', self.ui_tree_view ).activated.connect(self.copy_node)
        QShortcut( 'Ctrl+V', self.ui_tree_view ).activated.connect(self.paste_node)
        QShortcut( 'Insert', self.ui_tree_view ).activated.connect(self.add_node)
        QShortcut( 'Esc', self.ui_tree_view ).activated.connect(self.stop_filtering)
        QShortcut( 'Ctrl+S', self ).activated.connect(self.main_window.project_save)
        

        ################## TreeView Shortcuts END ##########################




        # modern progress bar
        self.progress_bars = [
            ModernProgressBar('rgb(0, 179, 0)', 'COVERED')
        ]

        for progress_bar in self.progress_bars:
            self.ui_layout_data_summary.addWidget(progress_bar)
            


        # FUNCTIONAL PART:
        self.send_project_path.connect(main_window.tree_file_browser.receive_project_path)

        self.ui_tree_view.clicked.connect(self._display_values)  # update line edits on mouse click

        selection_model = self.ui_tree_view.selectionModel()
        selection_model.selectionChanged.connect(self._display_values)  # update line edits on Up/Down Arrows

        self.ui_remove.clicked.connect(self.remove_node)
        self.ui_add.clicked.connect(self.add_node)
        self.ui_add.setShortcut('Ctrl+n')
        self.ui_duplicate.clicked.connect(self.duplicate_node)
        self.ui_edit.clicked.connect(self.edit_node)
        self.ui_edit.setShortcut('F4')
        self.ui_edit.setToolTip("F4")
        self.ui_export.clicked.connect(self.tree_2_file)
        self.ui_update_requirements.clicked.connect(lambda: self.update_requirements(True))
        self.ui_new_requirements.clicked.connect(self.add_req_node)
        self.ui_check_coverage.clicked.connect(self.create_dict_from_scripts_for_coverage_check)
        self.ui_le_filter.textChanged.connect(self._filter_items)
        self.ui_le_filter.textEdited.connect(self._reset_filter)
        # self.ui_btn_filter.clicked.connect(self.open_wildcard_filter)
        self.ui_btn_goBack.clicked.connect(self._goto_previous_index)


        self.send_data_2_completer()

        self.update_data_summary()


        # node copied into memory by action COPY
        self.node_to_paste = None

        # SENDING REQUIREMENT LIST WIDGET ITEM TO MAIN WINDOW
        # signal for sending file path from requirement listwidget
        self.send_file_path.connect(main_window.file_open_from_tree)
        self.ui_lw_file_paths_coverage.itemDoubleClicked.connect(self._doubleclick_on_tc_reference)
        self.ui_lw_outlinks.itemDoubleClicked.connect(self._doubleclick_on_outlink)
        self.uiListWidgetModuleIgnoreList.itemDoubleClicked.connect(self._doubleclick_on_ignored_reference)




        # REQUIREMENT TEXT IMPROVEMENT
        self.ui_requirement_text = RequirementTextEdit(self.main_window)
        self.ui_layout_req_text.addWidget(self.ui_requirement_text)


        # COPY TO CLIPBOAR FEATURE
        self.ui_btnCopyReqRef.clicked.connect(self.copy_to_clipboard)


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



        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(1)        


    def _expand_all_children(self):
        selected_item_index = self.ui_tree_view.currentIndex()
        self.ui_tree_view.expandRecursively(selected_item_index)

    def _collapse_all_children(self):
        selected_item_index = self.ui_tree_view.currentIndex()
        selected_item = self.model.itemFromIndex(selected_item_index)
        
        def _browse_children(node):         
            for row in range(node.rowCount()):
                requirement_node = node.child(row)
                requirement_node_index = requirement_node.index()
                self.ui_tree_view.collapse(requirement_node_index)

                _browse_children(requirement_node)        
        
        _browse_children(selected_item)
        self.ui_tree_view.collapse(selected_item_index)



    def copy_to_clipboard(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.ui_requirement_id.text(), mode=cb.Clipboard)
        self.main_window.show_notification(f"Item {self.ui_requirement_id.text()} copied to Clipboard.")  



    def make_ui_components_editable(self):
        for c in self.ui_components_for_editing:
            if isinstance(c, (QLineEdit, QTextEdit)): c.setReadOnly(False)
            if isinstance(c, QListWidget): c.setEnabled(True) 
            c.setStyleSheet("background-color: rgb(20, 20, 120);")

    def make_ui_components_not_editable(self):
        for c in self.ui_components_for_editing:
            if isinstance(c, (QLineEdit, QTextEdit)): c.setReadOnly(True)  
            if isinstance(c, QListWidget): c.setEnabled(False) 
            c.setStyleSheet("background-color: rgb(33, 37, 43);")
            if isinstance(c, QTextEdit):
                c.setStyleSheet("background-color: rgb(33, 37, 43); color: rgb(190, 190, 190); font-style: italic")
    
    @property
    def disk_project_path(self):
        return self._disk_project_path            

    @disk_project_path.setter
    def disk_project_path(self, path):
        self._disk_project_path = path
        self.ui_lab_project_path.setText(path)



    def _add_to_ignore_list(self):
        selected_item_index = self.ui_tree_view.currentIndex()
        selected_item = self.model.itemFromIndex(selected_item_index)
        if isinstance(selected_item, RequirementNode):
            selected_item.add_to_ignore_list()    
            self.update_data_summary()   


    def _remove_from_ignore_list(self):
        selected_item_index = self.ui_tree_view.currentIndex()
        selected_item = self.model.itemFromIndex(selected_item_index)
        if isinstance(selected_item, RequirementNode):
            selected_item.remove_from_ignore_list()    
            self.update_data_summary()   

      




    ####################################################################################################################
    # INTERFACE INPUT (INPUT DATA = LIST OF FILE PATHS):
    ####################################################################################################################


    @pyqtSlot(dict)
    def receive_data_from_drop_or_file_manager(self, data):
        condition_nodes.initialise(data, self.ROOT)
        dspace_nodes.initialise(data, self.ROOT)
        a2l_nodes.initialise(data, self.ROOT)
        self.is_project_saved = False
        self.main_window.show_notification(f"Model has been updated.")   
        self.send_data_2_completer() 


    @pyqtSlot(str, list)
    def receive_data_from_add_req_module_dialog(self, module_path, columns_names):
        r = RequirementFileNode(self.ROOT, module_path, columns_names, attributes=[], baseline={}, coverage_filter=None, coverage_dict=None, update_time=None, ignore_list=None, notes=None)
        r.file_2_tree()
        self.is_project_saved = False


    def add_req_node(self):
        self.form_add_req_module = FormAddModule(self)
        self.form_add_req_module.show()
        # from importlib import reload
        # self.ui_layout_req_text.removeWidget(self.ui_requirement_text)
        # reload(data_manager.req_text_edit)
        # self.ui_requirement_text = data_manager.req_text_edit.RequirementTextEdit(self.main_window)
        # self.ui_layout_req_text.addWidget(self.ui_requirement_text)
        


    @pyqtSlot(bool, str)
    def update_progress_status(self, is_visible, text=''):
        self.ui_frame_progress_status.setMinimumHeight(30) if is_visible else self.ui_frame_progress_status.setMinimumHeight(0)
        self.ui_label_progress_status.setText(text)




    ####################################################################################################################

    ####################################################################################################################
    # INTERFACE OUTPUT FOR COMPLETER (OUTPUT DATA = DICTIONARY):
    ####################################################################################################################


    def send_data_2_completer(self):

        cond_tooltips = {}
        Completer.cond_tooltips.clear()
        cond_dict = {}
        cond_model = QStandardItemModel()
        a2l_model = QStandardItemModel()
        dspace_model = QStandardItemModel()

        for root_row in range(self.ROOT.rowCount()):
            current_file_node = self.ROOT.child(root_row, 0)
            if isinstance(current_file_node, ConditionFileNode):
                condition_dict, condition_list, cond_tooltips = current_file_node.data_4_completer()
                if cond_tooltips:
                    Completer.cond_tooltips.update(cond_tooltips)



                for cond, values_list in condition_dict.items():
                    if cond not in cond_dict:
                        values_model = QStandardItemModel()
                        for value in values_list:
                            values_model.appendRow(value)

                        cond_dict.update({cond: values_model})

                        for cond_item in condition_list:
                            if cond_item.data(role=Qt.ToolTipRole) == cond:
                                cond_model.appendRow(cond_item)

            elif isinstance(current_file_node, A2lFileNode):
                a2l_list = current_file_node.data_4_completer()
                for a2l_item in a2l_list:
                    a2l_model.appendRow(a2l_item)

            elif isinstance(current_file_node, DspaceFileNode):
                dspace_model = current_file_node.data_4_completer()


        
        Completer.cond_tooltips.update(tooltips)

        Completer.cond_dict.clear()
        Completer.cond_model = QStandardItemModel()
        Completer.dspace_model = QStandardItemModel()

        if cond_dict:
            Completer.cond_dict.update(cond_dict)
            Completer.cond_model = cond_model

        if a2l_model:
            Completer.a2l_model = a2l_model

        if dspace_model:
            Completer.dspace_model = dspace_model



        self.update_data_summary()



    ####################################################################################################################





    ####################################################################################################################

    def send_request_2_doors(self, password, paths, columns_names):
        DoorsConnection(self, paths, columns_names, self, password)
        self.downloading_of_requirements_is_in_progress = True
        
      


    def update_requirements(self, is_multiple_modules):
        requirements_file_nodes_present = False
        for row in range(self.ROOT.rowCount()):
            node = self.ROOT.child(row)
            if isinstance(node, RequirementFileNode):
                requirements_file_nodes_present = True

        if requirements_file_nodes_present:
            if is_multiple_modules:
                passwd_from_input_dlg, ok = QInputDialog.getText(
                    None, 
                    "Doors Connection", 
                    f"Database: {self.main_window.app_settings.doors_database_path}\nUsername: {self.main_window.app_settings.doors_user_name}\n\nEnter your password:", QLineEdit.Password)
                if ok and passwd_from_input_dlg:
                    paths = []
                    columns = []
                    for row in range(self.ROOT.rowCount()):
                        node = self.ROOT.child(row)
                        if isinstance(node, RequirementFileNode):
                            paths.append(node.path)
                            columns.append(node.columns_names)
                    
                    if paths and columns:
                        self.send_request_2_doors(passwd_from_input_dlg, paths, columns)
                        
                        self.update_progress_status(True, 'Initialising...')
                        self.ui_update_requirements.setEnabled(False)
                        

            else:
                selected_item_index = self.ui_tree_view.currentIndex()
                selected_item = self.model.itemFromIndex(selected_item_index)
                if isinstance(selected_item, RequirementFileNode):
                    passwd_from_input_dlg, ok = QInputDialog.getText(
                    None, 
                    "Doors Connection", 
                    f"Database: {self.main_window.app_settings.doors_database_path}\nUsername: {self.main_window.app_settings.doors_user_name}\n\nEnter your password:", QLineEdit.Password)
                    if ok and passwd_from_input_dlg:
                        self.send_request_2_doors(passwd_from_input_dlg, [selected_item.path,], [selected_item.columns_names,])
                        self.update_progress_status(True, 'Initialising...')
                        self._module_which_is_currently_donwnloaded = selected_item
                        self.ui_update_requirements.setEnabled(False)




    def receive_data_from_doors(self, doors_output, timestamp):
        self.downloading_of_requirements_is_in_progress = False
        if not doors_output:
            self.main_window.show_notification(f"Error: No data received.") 
            return

        if self._module_which_is_currently_donwnloaded:
            self._module_which_is_currently_donwnloaded.receive_data_from_doors(doors_output, timestamp)
            self._module_which_is_currently_donwnloaded = None
            return

        for row in range(self.ROOT.rowCount()):
            node = self.ROOT.child(row)
            if isinstance(node, RequirementFileNode):
                node.receive_data_from_doors(doors_output, timestamp)

        
        self.main_window.show_notification(f"Requirements have been Updated.") 
        self.is_project_saved = False
        self._display_values()
        self.update_data_summary()
        

        

    def create_dict_from_scripts_for_coverage_check(self):
        if self.disk_project_path:
            self.ui_check_coverage.setEnabled(False)        
            worker = Worker(self)
            worker.signals.status.connect(self.update_progress_status)
            worker.signals.finished.connect(self.check_coverage)
            self.threadpool.start(worker)


    @pyqtSlot(dict)
    def check_coverage(self, file_content_dict):
        if self.disk_project_path:
            self.ui_check_coverage.setEnabled(False)
            for row in range(self.ROOT.rowCount()):
                current_item = self.ROOT.child(row)
                if isinstance(current_item, RequirementFileNode):
                    current_item.check_coverage_with_file_pointers(self.disk_project_path, file_content_dict)
            self.update_data_summary()
            self.ui_check_coverage.setEnabled(True)






    #####################################################################################################################################################
    #   UPDATE DATA SUMMARY
    #####################################################################################################################################################

    def update_data_summary(self):
        requirements_number = 0
        covered_number = 0

        def browse_children(parent_node):                
            nonlocal requirements_number, covered_number
            for row in range(parent_node.rowCount()):
                item = parent_node.child(row)   
                if not item.heading:
                    if item.is_covered == True:
                        covered_number += 1
                        requirements_number += 1
                        item.update_coverage(True)
                        item.get_requirement_module().coverage_dict.update({item.reference: list(item.file_references)})
                    elif item.is_covered == False:
                        requirements_number += 1
                        item.update_coverage(False)
                        item.get_requirement_module().coverage_dict.update({item.reference: list(item.file_references)})
                    else:
                        item.update_coverage(None)                    
                browse_children(item)

        for row in range(self.ROOT.rowCount()):
            current_node = self.ROOT.child(row)
            if isinstance(current_node, RequirementFileNode) and current_node.coverage_check:          
                current_node.coverage_dict.clear()
                browse_children(current_node)    
                
                current_node.update_title_text()                                                   


        self.progress_bars[0].update_value(requirements_number, covered_number)
        self.ui_lab_req_total.setText(str(requirements_number))
        self.ui_lab_req_covered.setText(str(covered_number))
        self.ui_lab_req_not_covered.setText(str(requirements_number-covered_number))
        self.ui_lab_project_path.setText(self.disk_project_path)

        self._display_values()















    ################################################################################################
    #  PROJECT HANDLING
    ################################################################################################

    def check_if_project_is_saved(self):
        if not self.is_project_saved:
            question = QMessageBox.question(self,
                            "R2ScriptEditor",
                            "Current project is not saved.\n\nDo you want to discard changes?",
                            QMessageBox.Yes | QMessageBox.No)
            if question == QMessageBox.Yes:
                return True
            else:
                return False
        
        else:
            return True


    @pyqtSlot(str)
    def save_project(self, path):

        data = {
            'disk_project_path': self.disk_project_path,
            'Conditions Files': [],
            'DSpace Files': [],
            'A2L Files': [],
            'REQUIREMENT MODULES': [],
        }

        for row in range(self.ROOT.rowCount()):
            current_node = self.ROOT.child(row)  # get node object

            received_data = current_node.data_4_project(data)

            data.update(received_data)

            if isinstance(current_node, (ConditionFileNode, DspaceFileNode)):
                if current_node.is_modified:
                    current_node.tree_2_file()

        try:
            with open(path, 'w', encoding='utf8') as f:
                f.write(json.dumps(data, indent=2))
                # HANDLE RECENT PROJECTS FILE
                self.update_recent_projects(path)
                self.is_project_saved = True
                self.main_window.show_notification(f"Project {path} has been saved.")    

        except Exception as e:
            dialog_message(self, "Unable to Save Project, error:" + str(e))





    @pyqtSlot(str)
    def open_project(self, path):

        if not self.check_if_project_is_saved():
            return

        self._erase_model()

        try:
            with open(path, 'r', encoding='utf8') as f:
                data = json.loads(f.read())

            # Handle project disk path
            self.disk_project_path = data.get('disk_project_path')
            if self.disk_project_path:
                if Path(self.disk_project_path).exists():
                    self.send_project_path.emit(self.disk_project_path)
                else:
                    dialog_message(self, f'Unable to Set Disk Project Path, {self.disk_project_path} does not exist!')
            # Handle project files
            condition_nodes.initialise(data, self.ROOT)
            dspace_nodes.initialise(data, self.ROOT)
            a2l_nodes.initialise(data, self.ROOT)
            requirement_nodes.initialise(data, self.ROOT)

            # HANDLE RECENT PROJECTS FILE
            self.update_recent_projects(path)
            self.is_project_saved = True

            self.main_window.show_notification(f"Project {path} has been loaded.") 
            self.send_data_2_completer()
            self.update_data_summary()

            self.main_window.opened_project_path = path
            self.main_window.update_title()
       
        
        except Exception as ex:
            dialog_message(self, f"Loading of JSON File failed:\n\n" + str(ex))
        



    @pyqtSlot(object)
    def new_project(self, data):

        if not self.check_if_project_is_saved():
            return

        self._erase_model()

        # Handle project disk path
        self.disk_project_path = data.get('disk_project_path')
        self.send_project_path.emit(self.disk_project_path)
        # Handle project files
        condition_nodes.initialise(data, self.ROOT)
        dspace_nodes.initialise(data, self.ROOT)
        a2l_nodes.initialise(data, self.ROOT)
        requirement_nodes.initialise(data, self.ROOT)

        self.is_project_saved = False


        self.update_data_summary()
        self.send_data_2_completer()

    
    def update_recent_projects(self, path):
        if self.settings.recent_projects:
            if path not in self.settings.recent_projects:
                self.settings.recent_projects.insert(0, path)
            else:
                self.settings.recent_projects.remove(path)
                self.settings.recent_projects.insert(0, path)
        else:
            self.settings.recent_projects = [path,]          


    def _erase_model(self):
        self.ROOT.removeRows(0, self.ROOT.rowCount())








    ####################################################################################################################
    # PRIVATE METHODS
    ####################################################################################################################


    def _hide_all_frames(self):
        # Common Area
        self.ui_frame_file.setVisible(False)
        self.frame_10.setVisible(False)
        # Condition Area
        self.ui_frame_cond.setVisible(False)
        self.ui_frame_cond.setFont(font)
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


    def _display_values(self):
        self._hide_all_frames()
        self._disable_all_buttons()
        self.ui_le_filter.setEnabled(False)
        self.ui_frame_requirement.setEnabled(True)
        # self.ui_group_box_all_frames.setEnabled(False)


        selected_item_index = self.ui_tree_view.currentIndex()
        selected_item = self.model.itemFromIndex(selected_item_index)

        # Recover last filter if there is some
        if selected_item:
            self.ui_le_filter.setText(selected_item.data(Qt.UserRole))
            

        # ConditionFileNode, DspaceFileNode, A2lFileNode
        if isinstance(selected_item, (ConditionFileNode, DspaceFileNode, A2lFileNode)):
            self.ui_le_filter.setEnabled(True)
            self.ui_frame_file.setVisible(True)
            self.ui_file_path.setText(selected_item.path)
            if isinstance(selected_item, (ConditionFileNode, DspaceFileNode)):
                # Buttons:
                self.ui_export.setEnabled(True)  
                self.ui_remove.setEnabled(True)          

        # RequirementFileNode
        elif isinstance(selected_item, RequirementFileNode):
            self.ui_le_filter.setEnabled(True)
            self.uiFrameRequirementModule.setVisible(True)
            self.uiLineEditModulePath.setText(selected_item.path)
            self.uiLineEditUpdateTime.setText(str(selected_item.timestamp))

            self.uiTextEditModuleBaseline.clear()
            # baseline_text = ""
            for attr, value in selected_item.baseline.items():
                self.uiTextEditModuleBaseline.insertHtml(f'<span style="color: rgb(150, 150, 150);">{attr.capitalize()}:</span>  <span> {value}</span><br>')
            # self.uiTextEditModuleBaseline.setPlainText(baseline_text)

            self.uiListWidgetModuleIgnoreList.clear()
            # self.uiListWidgetModuleIgnoreList.insertItems(0, selected_item.ignore_list)


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
            columns_names = selected_item.get_requirement_module().columns_names_backup

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
            filter_text = selected_item.get_requirement_module().data(Qt.UserRole)
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
        selected_item_index = self.ui_tree_view.currentIndex()
        selected_item = self.model.itemFromIndex(selected_item_index)
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
            self.ui_tree_view.setCurrentIndex(FOUND_NODE.index())
            self.ui_tree_view.scrollTo(FOUND_NODE.index())   



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
            self.ui_tree_view.setCurrentIndex(FOUND_NODE.index())
            self.ui_tree_view.scrollTo(FOUND_NODE.index())
            # self._update_previous_indexes(FOUND_NODE.index())
        else:
            dialog_message(self, "Module is missing.")


    def _goto_previous_index(self):
        self.ui_tree_view.goto_previous_index()


    def _doubleclick_on_tc_reference(self, list_item_text):

        self.send_file_path.emit(list_item_text.data(Qt.UserRole))
        self.main_window.manage_right_menu(self.main_window.tabs_splitter, self.main_window.ui_btn_text_editor)


    def _create_tc_template_with_req_reference(self, is_testable):
        selected_item_index = self.ui_tree_view.currentIndex()
        selected_item = self.model.itemFromIndex(selected_item_index)

        if isinstance(selected_item, RequirementNode):
            template = TemplateTestCase(req_id=selected_item.columns_data[0], req_text=selected_item.columns_data[-1], is_testable=is_testable)
            # print(template.generate_tc_template())
            text = template.generate_tc_template()
            file_path = None
            tab_name = 'Untitled'
            self.main_window.left_tabs.addTab(TextEdit(self.main_window, text, file_path), QIcon(u"ui/icons/16x16/cil-description.png"), tab_name)
            self.main_window.actual_text_edit.setFocus()
            self.main_window.manage_right_menu(self.main_window.tabs_splitter, self.main_window.ui_btn_text_editor)            




    def _context_menu(self, point):
        selected_item_index = self.ui_tree_view.indexAt(point)
        selected_item = self.model.itemFromIndex(selected_item_index)

        if not selected_item_index.isValid():
            return

        # # TEST:
        # selected_item_index = self.ui_tree_view.currentIndex()
        # selected_item = self.model.itemFromIndex(selected_item_index)

        menu = QMenu()
        menu.setStyleSheet("QMenu::separator {height: 0.5px; margin: 3px; background-color: rgb(38, 59, 115);}")

        menu.addAction(self.action_expand_all_children)
        menu.addAction(self.action_collapse_all_children)
        menu.addSeparator()
        if isinstance(selected_item, RequirementFileNode) and selected_item.coverage_check:
            
            if not selected_item.data(Qt.UserRole):
                menu.addAction(self.action_show_only_requirements_not_covered)                 
                menu.addAction(self.action_show_only_requirements_with_coverage)                   
                menu.addAction(self.action_show_all_requirements)
                menu.addSeparator()
                menu.addAction(self.action_remove_coverage_filter)          

        if isinstance(selected_item, RequirementFileNode):
            if not selected_item.data(Qt.UserRole):
                if not selected_item.coverage_check:
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
                if selected_item.reference in selected_item.get_requirement_module().ignore_list:                
                    menu.addAction(self.action_remove_from_ignore_list)
                elif selected_item.is_covered == False:
                    menu.addAction(self.action_add_to_ignore_list)
            menu.addSeparator()            

        if isinstance(selected_item, (TestStepNode, ValueNode, ConditionNode)):
            menu.addAction(self.action_duplicate)
            menu.addSeparator()            
        
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

    def stop_filtering(self):
        selected_item_index = self.ui_tree_view.currentIndex()
        selected_item = self.model.itemFromIndex(selected_item_index)
        if isinstance(selected_item, RequirementNode):
            module = selected_item.get_requirement_module()
            if module.data(Qt.UserRole):  
                def _collapse_all_children(node):
                    for row in range(node.rowCount()):
                        node_child = node.child(row)
                        if node_child:
                            self.ui_tree_view.collapse(node_child.index())
                            node_child.setForeground(QColor(200, 200, 200))
                            self.ui_tree_view.setRowHidden(row, node.index(), False)
                        _collapse_all_children(node_child)   
                
                _collapse_all_children(module)

                parent = selected_item.parent()
                while parent:
                    self.ui_tree_view.expand(parent.index())
                    parent = parent.parent()
                self.ui_tree_view.scrollTo(selected_item_index)
        elif isinstance(selected_item, RequirementFileNode):
            self.ui_le_filter.clear()
            selected_item.setData("", Qt.UserRole)
            self._reset_filter("")


    def _reset_filter(self, filtered_text):
        selected_item_index = self.ui_tree_view.currentIndex()
        selected_item = self.model.itemFromIndex(selected_item_index)     

        if filtered_text.strip() == "":
            def _collapse_all_children(node):
                for row in range(node.rowCount()):
                    node_child = node.child(row)
                    if node_child:
                        self.ui_tree_view.collapse(node_child.index())
                        node_child.setForeground(QColor(200, 200, 200))
                        self.ui_tree_view.setRowHidden(row, node.index(), False)
                    _collapse_all_children(node_child)   
            
            _collapse_all_children(selected_item)

            self.ui_tree_view.collapse(selected_item_index)

        else:
            self.ui_tree_view.expand(selected_item_index)




    def _filter_items(self, filtered_text):


        selected_item_index = self.ui_tree_view.currentIndex()
        selected_item = self.model.itemFromIndex(selected_item_index)        
        
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



        # Save filter text to items QUserRole Data
        selected_item.setData(filtered_text, Qt.UserRole)

        if isinstance(selected_item, (ValueNode, TestStepNode, DspaceDefinitionNode, DspaceVariableNode, RequirementNode)):
            return
        
        elif isinstance(selected_item, RequirementFileNode):      

            def _browse_children(node):         
                for row in range(node.rowCount()):
                    requirement_node = node.child(row)
                    if requirement_node:
                        data = " ".join(requirement_node.columns_data) + " " + str(requirement_node.reference)
                
                        if filtered_text.lower() in data.lower() :    
                            self.ui_tree_view.setRowHidden(row, node.index(), False)
                            requirement_node.setForeground(QColor("white"))
                            parent = requirement_node.parent()
                            while parent and parent.parent():
                                self.ui_tree_view.setRowHidden(parent.row(), parent.parent().index(), False)
                                self.ui_tree_view.expand(parent.index())
                                parent = parent.parent()
                        else:
                            self.ui_tree_view.setRowHidden(row, node.index(), True)
                            requirement_node.setForeground(QColor(90, 90, 90))
                            self.ui_tree_view.collapse(requirement_node.index())

                    _browse_children(requirement_node)
          

            if filtered_text.strip() == "":
                if selected_item.show_only_coverage:
                    self._show_only_items_with_coverage()  
                return            
            
            else:
                _browse_children(selected_item)



        elif isinstance(selected_item, DspaceFileNode):
            
            if filtered_text.strip() != "":
                for row in range(selected_item.rowCount()):
                    ds_definition = selected_item.child(row)
                    rows_hidden = 0
                    for definition_row in range(ds_definition.rowCount()):
                        if filtered_text.lower() in ds_definition.child(definition_row).text().lower():
                            self.ui_tree_view.setRowHidden(definition_row, ds_definition.index(), False)
                            self.ui_tree_view.expand(ds_definition.index())
                        else:
                            self.ui_tree_view.setRowHidden(definition_row, ds_definition.index(), True)
                            rows_hidden += 1
                        if rows_hidden == ds_definition.rowCount():
                            self.ui_tree_view.setRowHidden(row, selected_item.index(), True)
                        else:
                            self.ui_tree_view.setRowHidden(row, selected_item.index(), False)

            


        elif isinstance(selected_item, (ConditionFileNode, A2lFileNode)):
            for row in range(selected_item.rowCount()):
                if filtered_text.lower() in selected_item.child(row).text().lower():
                    self.ui_tree_view.setRowHidden(row, selected_item_index, False)
                else:
                    self.ui_tree_view.setRowHidden(row, selected_item_index, True)

















##############################################################################################################################
# COVERAGE FILTER (ONLY VIEW AFFECTING)
##############################################################################################################################


    def _show_only_items_with_coverage(self):
        index = self.ui_tree_view.currentIndex()
        requirement_file_node = self.model.itemFromIndex(index)

        def _browse_children(node, hide):         
            for row in range(node.rowCount()):
                requirement_node = node.child(row)
                if hide and requirement_node.is_covered is None:
                    self.ui_tree_view.setRowHidden(row, node.index(), True)
                else:
                    self.ui_tree_view.setRowHidden(row, node.index(), False)
                _browse_children(requirement_node, hide)

        _browse_children(requirement_file_node, hide=True)
        requirement_file_node.show_only_coverage = True
        requirement_file_node.show_only_not_covered = False

        # ICONS:
        self.action_show_all_requirements.setIcon(QIcon())
        self.action_show_only_requirements_not_covered.setIcon(QIcon())
        self.action_show_only_requirements_with_coverage.setIcon(QIcon(u"ui/icons/24x24/cil-check-alt.png"))           






    def _show_only_items_not_covered(self):
        index = self.ui_tree_view.currentIndex()
        requirement_file_node = self.model.itemFromIndex(index)

        def _browse_children(node, hide):         
            for row in range(node.rowCount()):
                requirement_node = node.child(row)
                if hide and requirement_node.is_covered is not False:
                    self.ui_tree_view.setRowHidden(row, node.index(), True)
                else:
                    self.ui_tree_view.setRowHidden(row, node.index(), False)
                _browse_children(requirement_node, hide)

        _browse_children(requirement_file_node, hide=True)
        requirement_file_node.show_only_coverage = False
        requirement_file_node.show_only_not_covered = True

        # ICONS:
        self.action_show_all_requirements.setIcon(QIcon())
        self.action_show_only_requirements_not_covered.setIcon(QIcon(u"ui/icons/24x24/cil-check-alt.png"))
        self.action_show_only_requirements_with_coverage.setIcon(QIcon())             






    def _show_all_items(self):
        index = self.ui_tree_view.currentIndex()
        requirement_file_node = self.model.itemFromIndex(index)

        def _browse_children(node, hide):         
            for row in range(node.rowCount()):
                requirement_node = node.child(row)
                if hide and requirement_node.is_covered is None:
                    self.ui_tree_view.setRowHidden(row, node.index(), True)
                else:
                    self.ui_tree_view.setRowHidden(row, node.index(), False)
                _browse_children(requirement_node, hide)

        _browse_children(requirement_file_node, hide=False)
        requirement_file_node.show_only_coverage = False
        requirement_file_node.show_only_not_covered = False
        # ICONS:
        self.action_show_all_requirements.setIcon(QIcon(u"ui/icons/24x24/cil-check-alt.png"))
        self.action_show_only_requirements_not_covered.setIcon(QIcon())
        self.action_show_only_requirements_with_coverage.setIcon(QIcon())



        


 
        



##############################################################################################################################
# COVERAGE FILTER (DATA AFFECTING)
##############################################################################################################################


    def _open_form_for_coverage_filter(self):
        selected_item_index = self.ui_tree_view.currentIndex()
        selected_item = self.model.itemFromIndex(selected_item_index)
        if isinstance(selected_item, RequirementFileNode):
            self.form_req_filter = FormAddCoverageFilter(self, selected_item)
            self.form_req_filter.show()
            # Remove View Filter
            self._show_all_items()


    def _remove_coverage_filter(self):
        index = self.ui_tree_view.currentIndex()
        requirement_file_node = self.model.itemFromIndex(index)   
        requirement_file_node.remove_coverage_filter()
        self.update_data_summary()
        #  Remove View Filter
        self._show_all_items()





    @pyqtSlot(str)
    def receive_data_from_req_filter_dialog(self, filter_string):
        pass
















    ####################################################################################################################
    # A2L NORMALISATIION:
    ####################################################################################################################
    def normalise_a2l_file(self):
        selected_item_index = self.ui_tree_view.currentIndex()
        selected_item = self.model.itemFromIndex(selected_item_index)

        if isinstance(selected_item, A2lFileNode):
            selected_item.normalise_file()  
            self.send_data_2_completer()      






    ####################################################################################################################
    # ADDING / MODIFYING / REMOVING / EXPORTING NODES DATA:
    ####################################################################################################################


    def tree_2_file(self):
        selected_item_index = self.ui_tree_view.currentIndex()
        selected_item = self.model.itemFromIndex(selected_item_index)
        if isinstance(selected_item, (ConditionFileNode, DspaceFileNode)):
            selected_item.tree_2_file()


    def remove_node(self):
        selected_item_index = self.ui_tree_view.currentIndex()
        selected_item = self.model.itemFromIndex(selected_item_index)

        selected_item_row = selected_item_index.row()
        parent_item_index = selected_item_index.parent()

        if self.model.rowCount(parent_item_index) > 1:
            
            if hasattr(selected_item, 'get_file_node'):
                selected_item.get_file_node().set_modified(True)

            self.main_window.show_notification(f"Item {selected_item.text()} has been removed.")  
            self.model.removeRow(selected_item_row, parent_item_index)                

            if isinstance(selected_item, RequirementNode):
                self.is_project_saved = False
                self.update_data_summary()            

        else:
            self.main_window.show_notification(f"Can not remove last item.")  

        self.send_data_2_completer()
            
    
    def add_node(self):
        selected_item_index = self.ui_tree_view.currentIndex()
        selected_item = self.model.itemFromIndex(selected_item_index)

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
        
        self.send_data_2_completer()


    def duplicate_node(self):
        selected_item_index = self.ui_tree_view.currentIndex()
        selected_item = self.model.itemFromIndex(selected_item_index)
        if isinstance(selected_item, (ConditionNode, ValueNode, TestStepNode)):            
            selected_item.parent().insertRow(selected_item_index.row() + 1, selected_item.get_node_copy())        
            if hasattr(selected_item, 'get_file_node'):
                selected_item.get_file_node().set_modified(True)
            self.main_window.show_notification(f"Item {selected_item.text()} has been duplicated.")  

    def copy_node(self):
        selected_item_index = self.ui_tree_view.currentIndex()
        selected_item = self.model.itemFromIndex(selected_item_index)    
        if isinstance(selected_item, (ConditionNode, ValueNode, TestStepNode)):         
            self.node_to_paste = selected_item.get_node_copy() 
            self.main_window.show_notification(f"Item {selected_item.text()} has been copied to Clipboard.")  


    def paste_node(self):
        selected_item_index = self.ui_tree_view.currentIndex()
        selected_item = self.model.itemFromIndex(selected_item_index)

        if self.node_to_paste and type(self.node_to_paste) == type(selected_item):
            new_item_row = selected_item_index.row() + 1
            selected_item.parent().insertRow(new_item_row, self.node_to_paste)
            self.main_window.show_notification(f"Item {self.node_to_paste.text()} has been inserted to Tree.") 
            self.node_to_paste = None
            selected_item.get_file_node().set_modified(True) 

            self.send_data_2_completer


    def edit_node(self, button_is_checked):
        selected_item_index = self.ui_tree_view.currentIndex()
        selected_item = self.model.itemFromIndex(selected_item_index)

        if not selected_item:
            return

        if button_is_checked:
            self.ui_tree_view.setEnabled(False)
            self.make_ui_components_editable()
            # if isinstance(selected_item, RequirementFileNode):
            #     self.uiLisWidgetModuleColumns.setStyleSheet("background-color: rgb(20, 20, 120);")
            #     self.uiLineEditModulePath.setStyleSheet("background-color: rgb(20, 20, 120);")
            #     self.uiLisWidgetModuleColumns.setEnabled(True)
            #     self.uiListWidgetModuleIgnoreList.setEnabled(False)
            # elif isinstance(selected_item, RequirementNode):
            #     self.uiTextEditRequirementNote.setStyleSheet("background-color: rgb(20, 20, 120);")
            #     self.uiTextEditRequirementNote.setReadOnly(False)


        else:
            
            self.ui_tree_view.setEnabled(True)
            self.make_ui_components_not_editable()
            
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
                # selected_item.set_is_saved(False)
            elif isinstance(selected_item, DspaceVariableNode):
                selected_item.name = self.ui_ds_name.text()
                selected_item.setText(selected_item.name)
                selected_item.value = self.ui_ds_value.text()
                selected_item.path = self.ui_ds_path.text()
                # change path for backup --> impossible to save two requirement files with same path
            elif isinstance(selected_item, RequirementFileNode):
                selected_item.path = self.uiLineEditModulePath.text()
                selected_item.setText(reduce_path_string(selected_item.path))
                self.uiLisWidgetModuleColumns.setEnabled(False)
                self.uiListWidgetModuleIgnoreList.setEnabled(True)
                selected_item.columns_names = self.uiLisWidgetModuleColumns.get_all_items()
                # self.uiLisWidgetModuleColumns.setStyleSheet("background-color: rgb(33, 37, 43); border-color: rgb(50, 50, 50)")
                # self.uiLineEditModulePath.setStyleSheet("background-color: rgb(33, 37, 43); border-color: rgb(50, 50, 50)")
            elif isinstance(selected_item, RequirementNode):
                note = self.uiTextEditRequirementNote.toPlainText()
                selected_item.update_note(note)
                # self.uiTextEditRequirementNote.setStyleSheet("background-color: rgb(33,37,43);")
                # self.uiTextEditRequirementNote.setReadOnly(True)
            
            if hasattr(selected_item, 'get_file_node'):
                selected_item.get_file_node().set_modified(True)

            
            self.send_data_2_completer()
            self.main_window.show_notification(f"Item {selected_item.text()} has been updated.")



    def receive_data_from_add_node_dialog(self, data: dict):    

        cond_data = data.get("cond_data")
        dspace_data = data.get("dspace_data")

        if dspace_data:
            dspace_name, dspace_value, dspace_path = dspace_data["dspace_name"], dspace_data["dspace_value"], dspace_data["dspace_path"]

        if cond_data:
            condition, value, test_step_name, test_step_action, test_step_comment, test_step_nominal \
                = cond_data["condition"], cond_data["value"], cond_data["test_step_name"], cond_data["test_step_action"], cond_data["test_step_comment"], cond_data["test_step_nominal"]            
        
        selected_item_index = self.ui_tree_view.currentIndex()
        selected_item = self.model.itemFromIndex(selected_item_index)

        if hasattr(selected_item, 'get_file_node'):
            selected_item.get_file_node().set_modified(True)

        if isinstance(selected_item, ConditionNode):
            # CONDITION:
            new_condition = ConditionNode(condition, '99')
            new_value = ValueNode(value, '99')
            new_ts = TestStepNode(test_step_name, test_step_action, test_step_comment, test_step_nominal)

            new_value.appendRow(new_ts)
            new_condition.appendRow(new_value)

            new_condition_row = selected_item_index.row() + 1
            selected_item.parent().insertRow(new_condition_row, new_condition)

        elif isinstance(selected_item, ValueNode):
            # VALUE:
            new_value = ValueNode(value, '99')
            new_ts = TestStepNode(test_step_name, test_step_action, test_step_comment, test_step_nominal)

            new_value.appendRow(new_ts)
            new_value_row = selected_item_index.row() + 1
            selected_item.parent().insertRow(new_value_row, new_value)

        elif isinstance(selected_item, TestStepNode):
            # TEST STEP:
            new_item = TestStepNode(test_step_name, test_step_action, test_step_comment, test_step_nominal)
            new_item_row = selected_item_index.row() + 1
            selected_item.parent().insertRow(new_item_row, new_item)

        elif isinstance(selected_item, DspaceVariableNode):
            # dSPACE VARIABLE:
            new_item = DspaceVariableNode(dspace_name, dspace_value, dspace_path)
            new_item_row = selected_item_index.row() + 1
            selected_item.parent().insertRow(new_item_row, new_item)
            # print("DSPACE VAR NODE ADDED")

        self.main_window.show_notification(f"Item has been inserted to Tree.") 
        self.send_data_2_completer()



    def move_node(self, direction):
        selected_item_index = self.ui_tree_view.currentIndex()
        selected_item = self.model.itemFromIndex(selected_item_index)
        
        if not selected_item: 
            return

        if not selected_item.parent() or isinstance(selected_item, (DspaceDefinitionNode, A2lFileNode)):
            return

        
        parent = selected_item.parent()

        if direction == 'up':
            new_item_row = selected_item_index.row() - 1
        else:
            new_item_row = selected_item_index.row() + 1
        
        if new_item_row < 0 or new_item_row > parent.rowCount()-1:
            return

        item = parent.takeChild(selected_item_index.row())
        self.model.removeRow(selected_item_index.row(), selected_item_index.parent())
        parent.insertRow(new_item_row, item)
        
        self.ui_tree_view.setCurrentIndex(item.index())

        if hasattr(selected_item, 'get_file_node'):
            selected_item.get_file_node().set_modified(True)
        
        self.send_data_2_completer()


    






   
    ####################################################################################################################
    # COVERAGE CHECK :
    ####################################################################################################################

import time
PATTERN_REQ_REFERENCE = re.compile(r"""(?:REFERENCE|\$REF:)\s*"(?P<req_reference>[\w\d,/\s\(\)-]+)"\s*""", re.IGNORECASE)

class Worker(QRunnable):
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.signals = WorkerSignals()


    @pyqtSlot()
    def run(self):
        reference_dict = {}       
        for root, dirs, files in os.walk(self.data_manager.disk_project_path):
            for filename in files:
                if filename.endswith((".par", ".txt")):
                    full_path = (root + '\\' + filename)
                    full_path = full_path.replace("\\", "/")

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
        # time.sleep(3)

        self.signals.finished.emit(reference_dict)




class WorkerSignals(QObject):
    finished = pyqtSignal(dict)
    status = pyqtSignal(bool, str)