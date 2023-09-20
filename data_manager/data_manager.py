from pathlib import Path
from ui.model_editor_ui import Ui_Form
from config.font import font
import json
from PyQt5.QtWidgets import QWidget, QInputDialog, QMenu, QAction, QLineEdit, QShortcut, QTextEdit, QMessageBox, QStyle, QPushButton
from PyQt5.Qt import QStandardItemModel
from PyQt5.QtGui import QIcon, QCursor, QKeySequence
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QSettings
from data_manager.condition_nodes import ConditionFileNode, ConditionNode, ValueNode, TestStepNode
from data_manager.dspace_nodes import DspaceFileNode, DspaceDefinitionNode, DspaceVariableNode
from data_manager.a2l_nodes import A2lFileNode, A2lNode
from data_manager import a2l_nodes, condition_nodes, requirement_nodes, dspace_nodes
from data_manager.requirement_nodes import RequirementFileNode, RequirementNode
from data_manager.dlg_add_node import DlgAddNode
from dialogs.form_add_req_module import AddRequirementsModule
from dialogs.form_req_filter import RequirementFilter
from progress_bar.widget_modern_progress_bar import ModernProgressBar
from text_editor.completer import Completer
from components.droppable_tree_view import DroppableTreeView
from data_manager.req_text_edit import RequirementTextEdit
from text_editor.tooltips import tooltips
from text_editor.text_editor import TextEdit
from components.template_test_case import TemplateTestCase



class DataManager(QWidget, Ui_Form):

    send_project_path = pyqtSignal(str)

    send_file_path = pyqtSignal(str)

    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)

        self.main_window = main_window

        # SETTINGS FROM DISK
        self.settings = QSettings(r'.\config\configuration.ini', QSettings.IniFormat)

        # MODEL PART:
        self.model = QStandardItemModel()
        self.model.rowsInserted.connect(self.send_data_2_completer)
        self.model.rowsRemoved.connect(self.send_data_2_completer)
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
        self._hide_all_frames()



        ################## CONTEXT MENU START ###########################
        self.ui_tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui_tree_view.customContextMenuRequested.connect(self._context_menu)  
        # CONTEXT MENU ACTIONS:  

        self.action_create_testable_tc_template_with_req_reference = QAction("Create Testable Test Script")
        self.action_create_testable_tc_template_with_req_reference.triggered.connect(lambda: self.create_tc_template_with_req_reference(True))
        self.action_create_not_testable_tc_template_with_req_reference = QAction("Create NOT Testable Test Script")
        self.action_create_not_testable_tc_template_with_req_reference.triggered.connect(lambda: self.create_tc_template_with_req_reference(False))        

        self.action_update_requirements = QAction('Update Requirements')
        self.action_update_requirements.setIcon(QIcon(u"ui/icons/16x16/cil-cloud-download.png"))
        self.action_update_requirements.triggered.connect(self.update_requirements)

        self.action_remove = QAction(QIcon(u"ui/icons/16x16/cil-x.png"), 'Remove')
        self.action_remove.triggered.connect(self.remove_node)

        self.action_edit = QAction('Edit')
        self.action_edit.setIcon(QIcon(u"ui/icons/16x16/cil-pencil.png"))
        self.action_edit.triggered.connect(self.edit_node)

        self.action_duplicate = QAction('Duplicate')
        self.action_duplicate.setIcon(QIcon(u"ui/icons/16x16/cil-clone.png"))
        self.action_duplicate.triggered.connect(self.duplicate_node)
        
        self.action_add = QAction('Add')
        self.action_add.setIcon(QIcon(u"ui/icons/16x16/cil-plus.png"))
        self.action_add.triggered.connect(self.add_node)  

        self.action_copy = QAction('Copy')
        self.action_copy.setIcon(QIcon(u"ui/icons/16x16/cil-plus.png"))
        self.action_copy.triggered.connect(self.copy_node)          

        self.action_paste = QAction('Paste')
        self.action_paste.setIcon(QIcon(u"ui/icons/16x16/cil-plus.png"))
        self.action_paste.triggered.connect(self.paste_node)          

        self.action_save = QAction('Export')
        self.action_save.setIcon(QIcon(u"ui/icons/16x16/cil-save.png"))
        self.action_save.triggered.connect(self.tree_2_file) 

        self.action_move_up = QAction('Move Up')
        self.action_move_up.setIcon(QIcon(u"ui/icons/16x16/cil-level-up.png"))
        # self.action_move_up.setShortcut('Ctrl+u')
        self.action_move_up.triggered.connect(lambda: self.move(direction='up')) 

        self.action_move_down = QAction(QIcon(u"ui/icons/16x16/cil-level-down.png"), 'Move Down')
        # self.action_move_down.setShortcut(QKeySequence("Ctrl+d"))
        self.action_move_down.triggered.connect(lambda: self.move(direction='down')) 

        self.action_normalise_a2l_file = QAction('Normalise (VDA spec.)')
        self.action_normalise_a2l_file.setIcon(QIcon(u"ui/icons/16x16/cil-chart-line.png"))
        self.action_normalise_a2l_file.triggered.connect(self.normalise_a2l_file)  
        ################## CONTEXT MENU END ###########################

        ################## TreeView Shortcuts START ##########################
        QShortcut( 'Ctrl+d', self.ui_tree_view ).activated.connect(lambda: self.move(direction='down'))
        QShortcut( 'Ctrl+u', self.ui_tree_view ).activated.connect(lambda: self.move(direction='up'))
        QShortcut( 'Del', self.ui_tree_view ).activated.connect(self.remove_node)

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
        self.ui_export.clicked.connect(self.tree_2_file)
        self.ui_update_requirements.clicked.connect(self.update_requirements)
        self.ui_new_requirements.clicked.connect(self.add_req_node)
        self.ui_check_coverage.clicked.connect(self.check_coverage)
        self.ui_le_filter.textChanged.connect(self._filter_items)
        self.ui_btn_filter.clicked.connect(self.open_wildcard_filter)


        self.send_data_2_completer()

        self.update_data_summary()


        # node copied into memory by action COPY
        self.node_to_paste = None

        # SENDING REQUIREMENT LIST WIDGET ITEM TO MAIN WINDOW
        # signal for sending file path from requirement listwidget
        self.send_file_path.connect(main_window.file_open_from_tree)
        self.ui_lw_file_paths_coverage.itemDoubleClicked.connect(self.doubleclick_on_tc_reference)

        # Update of NODE EDITTING, just switch read only --> not enabling/disabling whole group box
        self.node_line_edits = self.ui_group_box_all_frames.findChildren(QLineEdit)
        self.lock_line_edits()


        # REQUIREMENT TEXT IMPROVEMENT
        self.ui_requirement_text = RequirementTextEdit(self.main_window)
        self.ui_layout_req_text.addWidget(self.ui_requirement_text)

    def lock_line_edits(self):
        for le in self.node_line_edits:
            le.setReadOnly(True)

    def unlock_line_edits(self):
        for le in self.node_line_edits:
            le.setReadOnly(False)  
    
    @property
    def disk_project_path(self):
        return self._disk_project_path            

    @disk_project_path.setter
    def disk_project_path(self, path):
        self._disk_project_path = path
        self.ui_lab_project_path.setText(path)


    def doubleclick_on_tc_reference(self, list_item_text):
        self.send_file_path.emit(list_item_text.text())
        self.main_window.manage_right_menu(self.main_window.tabs_splitter, self.main_window.ui_btn_text_editor)


    def create_tc_template_with_req_reference(self, is_testable):
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

      




    ####################################################################################################################
    # INTERFACE INPUT (INPUT DATA = LIST OF FILE PATHS):
    ####################################################################################################################


    @pyqtSlot(dict)
    def receive_data_from_drop_or_file_manager(self, data):
        condition_nodes.initialise(data, self.ROOT)
        dspace_nodes.initialise(data, self.ROOT)
        a2l_nodes.initialise(data, self.ROOT)
        self.is_project_saved = False



    def fill_model(self, file_paths):
        pass


    @pyqtSlot(str, list, bool)
    def receive_data_from_add_req_module_dialog(self, module_path, columns_names, coverage_check):
        r = RequirementFileNode(self.ROOT, module_path, columns_names, coverage_check)
        r.file_2_tree()
        self.is_project_saved = False


    def add_req_node(self):
        self.form_add_req_module = AddRequirementsModule(self)
        self.form_add_req_module.show()
        


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
    # A2L NORMALISATIION:
    ####################################################################################################################
    def normalise_a2l_file(self):
        selected_item_index = self.ui_tree_view.currentIndex()
        selected_item = self.model.itemFromIndex(selected_item_index)

        if isinstance(selected_item, A2lFileNode):
            selected_item.normalise_file()        


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
            self.model.removeRow(selected_item_row, parent_item_index)

        if isinstance(selected_item, RequirementNode):
            self.is_project_saved = False


        else:
            print('Not Possible to remove last item, remove whole parent!')
            
    
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


    def duplicate_node(self):
        selected_item_index = self.ui_tree_view.currentIndex()
        selected_item = self.model.itemFromIndex(selected_item_index)
        selected_item.parent().insertRow(selected_item_index.row() + 1, selected_item.get_node_copy())        
        if hasattr(selected_item, 'get_file_node'):
            selected_item.get_file_node().set_modified(True)

    def copy_node(self):
        selected_item_index = self.ui_tree_view.currentIndex()
        selected_item = self.model.itemFromIndex(selected_item_index)        
        self.node_to_paste = selected_item.get_node_copy()        

    def paste_node(self):
        selected_item_index = self.ui_tree_view.currentIndex()
        selected_item = self.model.itemFromIndex(selected_item_index)

        if self.node_to_paste and type(self.node_to_paste) == type(selected_item):
            new_item_row = selected_item_index.row() + 1
            selected_item.parent().insertRow(new_item_row, self.node_to_paste)
            self.node_to_paste = None
            selected_item.get_file_node().set_modified(True)


    def edit_node(self, button_is_checked):
        selected_item_index = self.ui_tree_view.currentIndex()
        selected_item = self.model.itemFromIndex(selected_item_index)

        if not selected_item:
            return

        if button_is_checked:
            self.ui_tree_view.setEnabled(False)
            # self.ui_group_box_all_frames.setEnabled(True)
            self.unlock_line_edits()

        else:
            self.ui_tree_view.setEnabled(True)
            self.lock_line_edits()
            # self.ui_group_box_all_frames.setEnabled(False)

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
                selected_item.path = self.ui_file_path.text()
                selected_item.setText(selected_item.path)
                selected_item.columns_names = self.ui_file_note_columns.text().strip().split(",")

            
            if hasattr(selected_item, 'get_file_node'):
                selected_item.get_file_node().set_modified(True)

            self.send_data_2_completer()



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
            print("DSPACE VAR NODE ADDED")



    def move(self, direction):
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


    ####################################################################################################################


    def update_requirements(self):
        selected_item_index = self.ui_tree_view.currentIndex()
        selected_item = self.model.itemFromIndex(selected_item_index)
        if isinstance(selected_item, RequirementFileNode):
            passwd_from_input_dlg, ok = QInputDialog.getText(None, "Enter your Password", "Password:", QLineEdit.Password)
            if ok and passwd_from_input_dlg:
                selected_item.send_request_2_doors(passwd_from_input_dlg)
                self.update_progress_status(True, 'Preparing ...')
                self.is_project_saved = False



    def check_coverage(self):
        if self.disk_project_path:
            # self.ui_check_coverage.setEnabled(False)
            for row in range(self.ROOT.rowCount()):
                current_item = self.ROOT.child(row)
                if isinstance(current_item, RequirementFileNode):
                    current_item.check_coverage_with_file_pointers(self.disk_project_path)
            # self.update_data_summary()


    def update_data_summary(self):
        requirements_number = 0
        covered_number = 0

        for row in range(self.ROOT.rowCount()):
            current_node = self.ROOT.child(row)
            if isinstance(current_node, RequirementFileNode) and current_node.coverage_check:                
                    requirements_number += current_node.rowCount()
                    covered_number += current_node.is_covered
                    if current_node.is_covered < current_node.rowCount():
                        current_node.setIcon(QPushButton().style().standardIcon(QStyle.SP_DialogCancelButton))
                    else:
                        current_node.setIcon(QIcon(u"ui/icons/check.png"))
                    for row in range(current_node.rowCount()):
                        req_node = current_node.child(row)
                        req_node.setIcon(QIcon(u"ui/icons/check.png")) if req_node.is_covered \
                            else req_node.setIcon(QPushButton().style().standardIcon(QStyle.SP_DialogCancelButton))
                    


        self.progress_bars[0].update_value(requirements_number, covered_number)
        self.ui_lab_req_total.setText(str(requirements_number))
        self.ui_lab_req_covered.setText(str(covered_number))
        self.ui_lab_req_not_covered.setText(str(requirements_number-covered_number))
        self.ui_lab_project_path.setText(self.disk_project_path)

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
            'Requirements': [],
        }

        for row in range(self.ROOT.rowCount()):
            current_node = self.ROOT.child(row)  # get node object

            received_data = current_node.data_4_project(data)

            data.update(received_data)

        with open(path, 'w', encoding='utf8') as f:
            f.write(json.dumps(data, indent=2))

        # HANDLE RECENT PROJECTS FILE
        self.update_recent_projects(path)
        self.is_project_saved = True



    @pyqtSlot(str)
    def open_project(self, path):


        if not self.check_if_project_is_saved():
            return



        self.erase_model()


        try:
            with open(path, 'r', encoding='utf8') as f:
                data = json.loads(f.read())

            # Handle project disk path
            self.disk_project_path = data.get('disk_project_path')
            if self.disk_project_path:
                if Path(self.disk_project_path).exists():
                    self.send_project_path.emit(self.disk_project_path)
                else:
                    print(f'Unable to Set Disk Project Path, {self.disk_project_path} does not exist!')
            # Handle project files
            condition_nodes.initialise(data, self.ROOT)
            dspace_nodes.initialise(data, self.ROOT)
            a2l_nodes.initialise(data, self.ROOT)
            requirement_nodes.initialise(data, self.ROOT)

            # HANDLE RECENT PROJECTS FILE
            self.update_recent_projects(path)
            self.is_project_saved = True
        
        except FileNotFoundError:
            print('File Not Found')
        



    @pyqtSlot(object)
    def new_project(self, data):

        if not self.check_if_project_is_saved():
            return

        self.erase_model()

        # Handle project disk path
        self.disk_project_path = data.get('disk_project_path')
        self.send_project_path.emit(self.disk_project_path)
        # Handle project files
        condition_nodes.initialise(data, self.ROOT)
        dspace_nodes.initialise(data, self.ROOT)
        a2l_nodes.initialise(data, self.ROOT)
        requirement_nodes.initialise(data, self.ROOT)

        self.is_project_saved = False

        # self.update_data_summary()
        # self.send_data_2_completer()

    
    def update_recent_projects(self, path):
        recent_projects = self.settings.value('RECENT_PROJECTS')
        if recent_projects:
            if path not in recent_projects:
                recent_projects.insert(0, path)
            else:
                recent_projects.remove(path)
                recent_projects.insert(0, path)
            self.settings.setValue('RECENT_PROJECTS', recent_projects[:10])
        else:
            recent_projects = [path,]          
            self.settings.setValue('RECENT_PROJECTS', recent_projects)


    def erase_model(self):
        self.ROOT.removeRows(0, self.ROOT.rowCount())



    ####################################################################################################################
    # PRIVATE METHODS
    ####################################################################################################################


    def _hide_all_frames(self):
        # Common Area
        self.ui_frame_file.setVisible(False)
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

    def _disable_all_buttons(self):
        self.ui_add.setEnabled(False)
        self.ui_edit.setEnabled(False)
        self.ui_remove.setEnabled(False)
        self.ui_duplicate.setEnabled(False)
        self.ui_export.setEnabled(False)
        self.ui_update_requirements.setEnabled(False)


    def _display_values(self):
        self._hide_all_frames()
        self._disable_all_buttons()
        self.ui_le_filter.setEnabled(False)

        # self.ui_group_box_all_frames.setEnabled(False)


        selected_item_index = self.ui_tree_view.currentIndex()
        selected_item = self.model.itemFromIndex(selected_item_index)

        # Recover last filter if there is some
        if selected_item:
            self.ui_le_filter.setText(selected_item.data(Qt.UserRole))

        # Common Area
        if isinstance(selected_item, (ConditionFileNode, DspaceFileNode, A2lFileNode, RequirementFileNode)):
            self.ui_le_filter.setEnabled(True)
            self.ui_frame_file.setVisible(True)
            self.ui_file_path.setText(selected_item.path)
            self.ui_file_note.clear()
            if isinstance(selected_item, RequirementFileNode):
                self.ui_file_note.setText(str(selected_item.timestamp))
                self.ui_file_note_columns.setText(",".join(selected_item.columns_names))
                # Buttons:
                self.ui_update_requirements.setEnabled(True)
                self.ui_remove.setEnabled(True)
                self.ui_edit.setEnabled(True)
            if isinstance(selected_item, (ConditionFileNode, DspaceFileNode)):
                # Buttons:
                self.ui_export.setEnabled(True)
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
        # Requirement Area
        elif isinstance(selected_item, RequirementNode):
            # self.ui_group_box_all_frames.setEnabled(True)
            self.ui_frame_requirement.setVisible(True)

            self.ui_requirement_id.setText(selected_item.text())
            self.ui_requirement_covered.setText(str(selected_item.is_covered))
            text_to_display = ''
            columns_data = selected_item.columns_data
            columns_names = selected_item.parent().columns_names_backup


            for i in range(len(columns_names)):
                text_to_display += f'{columns_names[i]}:\n{columns_data[i+1]} \n\n'
            self.ui_requirement_text.setPlainText(text_to_display)

            # Buttons:
            self.ui_edit.setEnabled(True)
            # Frame
            self.ui_frame_requirement.setEnabled(True)

            # print(selected_item.files_which_cover_this_requirement)
            self.ui_lw_file_paths_coverage.clear()
            self.ui_lw_file_paths_coverage.addItems(selected_item.files_which_cover_this_requirement)



    def _context_menu(self, point):
        selected_item_index = self.ui_tree_view.indexAt(point)
        selected_item = self.model.itemFromIndex(selected_item_index)

        if not selected_item_index.isValid():
            return

        menu = QMenu()
        if isinstance(selected_item, A2lFileNode):
            menu.addAction(self.action_normalise_a2l_file)
        if isinstance(selected_item, RequirementFileNode):
            menu.addAction(self.action_update_requirements)            
        elif isinstance(selected_item, (ConditionFileNode, DspaceFileNode)):
            menu.addAction(self.action_save)
        elif isinstance(selected_item, (ConditionNode, ValueNode, TestStepNode, DspaceVariableNode)):
            menu.addActions([self.action_add,])
        if isinstance(selected_item, (TestStepNode, ValueNode, ConditionNode)):
            menu.addAction(self.action_duplicate)
            menu.addSeparator()

        if selected_item.parent(): 
            menu.addAction(self.action_move_up)
            menu.addAction(self.action_move_down)
            menu.addSeparator()

        if not isinstance(selected_item, (DspaceDefinitionNode, A2lNode)):
            menu.addAction(self.action_remove)

        if isinstance(selected_item, RequirementNode):
            menu.addAction(self.action_create_testable_tc_template_with_req_reference)
            menu.addAction(self.action_create_not_testable_tc_template_with_req_reference)
            menu.addSeparator()            
        
        if hasattr(selected_item, 'get_node_copy'):
            menu.addSeparator()
            menu.addAction(self.action_copy)

        if self.node_to_paste and type(self.node_to_paste) == type(selected_item):
            menu.addAction(self.action_paste)


        menu.exec_(QCursor().pos())






    def _filter_items(self, filtered_text):
        selected_item_index = self.ui_tree_view.currentIndex()
        selected_item = self.model.itemFromIndex(selected_item_index)

        # Save filter text to items QUserRole Data
        selected_item.setData(filtered_text, Qt.UserRole)

        if isinstance(selected_item, (ValueNode, TestStepNode, DspaceDefinitionNode, DspaceVariableNode)):
            pass
        
        elif isinstance(selected_item, RequirementFileNode):
            for row in range(selected_item.rowCount()):
                if filtered_text.lower() in selected_item.child(row).columns_data[-1].lower() or filtered_text.lower() in selected_item.child(row).columns_data[-2].lower():
                    self.ui_tree_view.setRowHidden(row, selected_item_index, False)
                else:
                    self.ui_tree_view.setRowHidden(row, selected_item_index, True)

        elif isinstance(selected_item, DspaceFileNode):
            for row in range(selected_item.rowCount()):
                ds_definition = selected_item.child(row)
                rows_hidden = 0
                for definition_row in range(ds_definition.rowCount()):
                    if filtered_text.lower() in ds_definition.child(definition_row).text().lower():
                        self.ui_tree_view.setRowHidden(definition_row, ds_definition.index(), False)
                    else:
                        self.ui_tree_view.setRowHidden(definition_row, ds_definition.index(), True)
                        rows_hidden += 1
                    if rows_hidden == ds_definition.rowCount():
                        self.ui_tree_view.setRowHidden(row, selected_item.index(), True)
                    else:
                        self.ui_tree_view.setRowHidden(row, selected_item.index(), False)



        else:
            for row in range(selected_item.rowCount()):
                if filtered_text.lower() in selected_item.child(row).text().lower():
                    self.ui_tree_view.setRowHidden(row, selected_item_index, False)
                else:
                    self.ui_tree_view.setRowHidden(row, selected_item_index, True)























# TEST --> SUPER FILTER


    def open_wildcard_filter(self):
        selected_item_index = self.ui_tree_view.currentIndex()
        selected_item = self.model.itemFromIndex(selected_item_index)
        if isinstance(selected_item, RequirementFileNode):
            self.form_req_filter = RequirementFilter(self, selected_item)
            self.form_req_filter.show()

    @pyqtSlot(list)
    def receive_data_from_req_filter_dialog(self, columns_filters):
        print(columns_filters)

        selected_item_index = self.ui_tree_view.currentIndex()
        selected_item = self.model.itemFromIndex(selected_item_index)

        for row in range(selected_item.rowCount()):
            for column_filter_index in range(len(columns_filters)):
                column_filter = columns_filters[column_filter_index].lower()
                column_data = selected_item.child(row).columns_data[column_filter_index+1].lower()
                print(column_filter)
                print(column_data)
                if column_filter != '' and column_filter not in column_data:
                    self.ui_tree_view.setRowHidden(row, selected_item_index, True)


# END TEST --> SUPER FILTER







#
# app = QApplication(sys.argv)
#
# demo = DataManager()
# demo.show()
#
# sys.exit(app.exec_())

