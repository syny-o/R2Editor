import re
from PyQt5.QtWidgets import QWidget, QLabel, QListWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QTextEdit, QShortcut, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal, QTimer

from dialogs.dialog_message import dialog_message
from ui.form_general_ui import Ui_Form


from data_manager.nodes.requirement_module import RequirementModule, RequirementNode
from data_manager.nodes.condition_file import ConditionFileNode, ConditionNode, ValueNode, TestStepNode
from data_manager.nodes.dspace_nodes import DspaceFileNode, DspaceDefinitionNode, DspaceVariableNode
from data_manager.nodes.a2l_nodes import A2lFileNode, A2lNode

from components.helper_functions import layout_generate_one_row as generate_one_row, validate_line_edits
from components.my_list_widget import MyListWidget
from components.widgets.widget_baseline import WidgetBaseline
from components.widgets.widget_req_filter_text_edit import RequirementFilterTextEdit


stylesheet ="""
    QTextEdit {border: 1px solid rgb(50, 50, 50);}
"""


class FormEditNode(QWidget, Ui_Form):

    node_was_updated = pyqtSignal()

    def __init__(self, NODE, DATA_MANAGER):
        super().__init__()
        self.setupUi(self)
        if not isinstance(NODE, RequirementModule):
            self.setMaximumSize(800, 600)
        else:
            self.resize(1000, 800)
        self.setStyleSheet(stylesheet)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowOpacity(0.95)        
        self.uiLabelTitle.setText("Edit")
        self.uiBtnStatusBarClose.clicked.connect(self.close)
        self.uiBtnTitleBarClose.clicked.connect(self.close)
        if not isinstance(NODE, RequirementModule):
            self.uiBtnTitleBarClose.setShortcut('Esc')
        self.uiBtnOK.clicked.connect(self._ok_clicked)
        self.uiBtnOK.setShortcut('Return')
        self.uiBtnApply.setMaximumWidth(500)
        self.uiBtnApply.clicked.connect(self._apply_clicked)

        self.show() 

        self.NODE = NODE
        self.node_was_updated.connect(DATA_MANAGER.edit_node_response)

        condition_and_value_node_layout_generator = ConditionAndValueNodeLayoutGenerator(self.NODE)
        test_step_node_layout_generator = TestStepNodeLayoutGenerator(self.NODE)
        dspace_variable_node_layout_generator = DspaceVariableNodeLayoutGenerator(self.NODE)
        requirement_node_layout_generator = RequirementNodeLayoutGenerator(self.NODE)
        requirement_module_layout_generator = RequirementModuleLayoutGenerator(self.NODE)
        
        self.NODES_2_LAYOUTS = {
            ConditionNode:      condition_and_value_node_layout_generator,
            ValueNode:          condition_and_value_node_layout_generator,
            TestStepNode:       test_step_node_layout_generator,
            DspaceVariableNode: dspace_variable_node_layout_generator,
            RequirementNode:    requirement_node_layout_generator,
            RequirementModule: requirement_module_layout_generator,
        }

        if type(self.NODE) == RequirementModule:
            self.uiMainLayout_1.addLayout(self.NODES_2_LAYOUTS[type(self.NODE)].provide_layout())
        else:
            self.uiMainLayout_2.addLayout(self.NODES_2_LAYOUTS[type(self.NODE)].provide_layout())



    def _ok_clicked(self):
        try:
            if self.NODES_2_LAYOUTS[type(self.NODE)].update_data() and not isinstance(self.NODE, RequirementModule):
                self.node_was_updated.emit()
                if not isinstance(self.NODE, RequirementModule):
                    self.close()

            if isinstance(self.NODE, RequirementModule):
                self.close()

        except Exception as ex:
            dialog_message(self, str(ex), "Error")


    def _apply_clicked(self):
        try:
            if self.NODES_2_LAYOUTS[type(self.NODE)].update_data():
                self.node_was_updated.emit()
        except Exception as ex:
            dialog_message(self, str(ex), "Error")








class ConditionAndValueNodeLayoutGenerator:
    def __init__(self, NODE: ConditionNode|ValueNode) -> None:
        self.uiMainLayout = QVBoxLayout()
        self.uiMainLayout.setContentsMargins(50, 50, 50, 50)
        self.uiMainLayout.setSpacing(10)
        self.NODE = NODE       


    def _create_layout(self):
        self.uiLineEditName = generate_one_row("Name:", self.uiMainLayout)
        self.uiLineEditName.setText(self.NODE.name)
        self.uiLineEditCategory = generate_one_row("Category:", self.uiMainLayout)
        self.uiLineEditCategory.setText(self.NODE.category)
        
        QTimer.singleShot(100, lambda: self.uiLineEditName.setFocus())
        QTimer.singleShot(120, lambda: self.uiLineEditName.selectAll())


    def provide_layout(self) -> QVBoxLayout:
        self._create_layout() 
        return self.uiMainLayout

    def update_data(self):
        if validate_line_edits(self.uiLineEditName, self.uiLineEditCategory):
            self.NODE.name = self.uiLineEditName.text()
            self.NODE.category = self.uiLineEditCategory.text()
            self.NODE.get_file_node().set_modified(True)
            return True



class TestStepNodeLayoutGenerator:
    def __init__(self, NODE: TestStepNode) -> None:
        self.uiMainLayout = QVBoxLayout()
        self.uiMainLayout.setContentsMargins(50, 50, 50, 50)
        self.uiMainLayout.setSpacing(10)
        self.NODE = NODE       


    def _create_layout(self):
        self.uiLineEditName = generate_one_row("Name:", self.uiMainLayout)
        self.uiLineEditName.setText(self.NODE.name)
        self.uiLineEditAction = generate_one_row("Action:", self.uiMainLayout)
        self.uiLineEditAction.setText(self.NODE.action)
        self.uiLineEditComment = generate_one_row("Comment:", self.uiMainLayout)
        self.uiLineEditComment.setText(self.NODE.comment)
        self.uiLineEditNominal = generate_one_row("Nominal:", self.uiMainLayout)
        self.uiLineEditNominal.setText(self.NODE.nominal)
        
        QTimer.singleShot(100, lambda: self.uiLineEditName.setFocus())
        QTimer.singleShot(120, lambda: self.uiLineEditName.selectAll())

    def provide_layout(self) -> QVBoxLayout:
        self._create_layout() 
        return self.uiMainLayout

    def update_data(self):
        if validate_line_edits(self.uiLineEditAction):
            self.NODE.name = self.uiLineEditName.text()
            self.NODE.action = self.uiLineEditAction.text()
            self.NODE.comment = self.uiLineEditComment.text()
            self.NODE.nominal = self.uiLineEditNominal.text()
            self.NODE.get_file_node().set_modified(True)
            return True   



class DspaceVariableNodeLayoutGenerator:
    def __init__(self, NODE: DspaceVariableNode) -> None:
        self.uiMainLayout = QVBoxLayout()
        self.uiMainLayout.setContentsMargins(50, 50, 50, 50)
        self.uiMainLayout.setSpacing(10)
        self.NODE = NODE       


    def _create_layout(self):
        self.uiLineEditName = generate_one_row("Name:", self.uiMainLayout)
        self.uiLineEditName.setText(self.NODE.name)
        self.uiLineEditValue = generate_one_row("Value:", self.uiMainLayout)
        self.uiLineEditValue.setText(self.NODE.value)
        self.uiLineEditPath = generate_one_row("Path:", self.uiMainLayout)
        self.uiLineEditPath.setText(self.NODE.path)
        
        QTimer.singleShot(100, lambda: self.uiLineEditName.setFocus())
        QTimer.singleShot(120, lambda: self.uiLineEditName.selectAll()) 

    def provide_layout(self) -> QVBoxLayout:
        self._create_layout() 
        return self.uiMainLayout

    def update_data(self):
        if validate_line_edits(self.uiLineEditName, self.uiLineEditPath, self.uiLineEditValue):
            self.NODE.name = self.uiLineEditName.text()
            self.NODE.value = self.uiLineEditValue.text()
            self.NODE.path = self.uiLineEditPath.text()
            self.NODE.get_file_node().set_modified(True)
            return True                      
        


        
class RequirementNodeLayoutGenerator:
    def __init__(self, NODE: RequirementNode) -> None:
        self.uiMainLayout = QVBoxLayout()
        self.uiMainLayout.setContentsMargins(50, 50, 50, 50)
        self.uiMainLayout.setSpacing(10)
        self.NODE = NODE       


    def _create_layout(self):
        l = QHBoxLayout()
        self.uiTextEditNote = QTextEdit(self.NODE.note)
        l.addWidget(QLabel("Note:    "))
        l.addWidget(self.uiTextEditNote)
        self.uiMainLayout.addLayout(l) 

        QTimer.singleShot(100, lambda: self.uiTextEditNote.setFocus())

    def provide_layout(self) -> QVBoxLayout:
        self._create_layout() 
        return self.uiMainLayout

    def update_data(self) -> bool:
        self.NODE.note = self.uiTextEditNote.toPlainText()
        return True  










##############################################################################################################################
# REQUIREMENT MODULE
##############################################################################################################################


class RequirementModuleLayoutGenerator:
    def __init__(self, NODE: RequirementModule) -> None:
        self.uiMainLayout = QVBoxLayout()
        self.uiMainLayout.setContentsMargins(10, 10, 10, 10)
        self.uiMainLayout.setSpacing(10)
        self.NODE = NODE  


    def _create_layout(self):
        # self.uiLineEditPath = generate_one_row("Path:      ", self.uiMainLayout, extend_label_width=False)
        # self.uiLineEditPath.setText(self.NODE.path)
        uiLayoutModuleColumns = QHBoxLayout()
        uiLayoutModuleColumns.setContentsMargins(0, 20, 0, 0)
        uiLayoutModuleColumns.addWidget(QLabel("Columns:"))

        self.uiListWidgetModuleAttributes = MyListWidget(context_menu=False)
        self.uiListWidgetModuleAttributes.setAcceptDrops(False)
        uiLayoutModuleColumns.addWidget(self.uiListWidgetModuleAttributes)  

        uiLayoutBaseline = QHBoxLayout()
        uiLayoutBaseline.addWidget(QLabel("Baseline:"))
        self.uiWidgetBaselines = WidgetBaseline(view_only=False)
        self.uiWidgetBaselines.setMaximumHeight(160)
        self.uiWidgetBaselines.update(self.NODE)
        uiLayoutBaseline.addWidget(self.uiWidgetBaselines)      
        self.uiMainLayout.addLayout(uiLayoutBaseline)

        self.uiListWidgetModuleColumns = MyListWidget()
        self.uiListWidgetModuleColumns.setDefaultDropAction(Qt.MoveAction)
        QShortcut( 'Del', self.uiListWidgetModuleColumns ).activated.connect(self.uiListWidgetModuleColumns.remove_item)
        # self.uiListWidgetModuleColumns.setDefaultDropAction(Qt.MoveAction)
        uiLayoutModuleColumns.addWidget(self.uiListWidgetModuleColumns)        

        self.uiMainLayout.addLayout(uiLayoutModuleColumns)

        self.uiListWidgetModuleColumns.insertItems(0, self.NODE.columns_names)
        self.uiListWidgetModuleAttributes.insertItems(0, self.NODE.attributes)

        self.uiLabelWarning = QLabel()

        # QTimer.singleShot(100, lambda: self.uiLineEditPath.setFocus())         

        if self.NODE.coverage_filter:
            self.uiListWidgetModuleColumns.setEnabled(False)
            # self.uiLineEditPath.setEnabled(False)
            self.uiWidgetBaselines.setEnabled(False)
            self.uiLabelWarning.setText("Remove coverage filter to edit columns/baseline.")
            self.uiLabelWarning.setStyleSheet("color: red;")
            self.uiLabelWarning.setAlignment(Qt.AlignCenter)
            self.uiMainLayout.addWidget(self.uiLabelWarning)

        uiLayoutCoverageFilter = QHBoxLayout()
        uiLayoutCoverageFilter.addWidget(QLabel("Cv. Filter:"))
        # self.uiTexEditCoverageFilter = QTextEdit()
        self.uiTexEditCoverageFilter = RequirementFilterTextEdit(self.NODE.columns_names)
        if not self.NODE.columns_names:
            self.uiTexEditCoverageFilter.setEnabled(False)        
        self.uiTexEditCoverageFilter.setMaximumHeight(100)
        uiLayoutCoverageFilter.addWidget(self.uiTexEditCoverageFilter)
        if f := self.NODE.coverage_filter:
            self.uiTexEditCoverageFilter.setPlainText(str(f))
        self.uiLabelNumberOfFilteredRequirements = QLabel()
        self.uiLabelNumberOfFilteredRequirements.setAlignment(Qt.AlignCenter)
        self.uiMainLayout.addLayout(uiLayoutCoverageFilter)
        self.uiMainLayout.addWidget(self.uiLabelNumberOfFilteredRequirements)


        

    def provide_layout(self) -> QVBoxLayout:
        self._create_layout() 
        return self.uiMainLayout


    def update_data(self):
        change = False
        if self._evaluate_baseline_changes():
            self._save_baseline_changes()
            change = True
        if self._evaluate_columns_changes():
            self._save_columns_changes()
            change = True
        if self._evaluate_filter_changes():
            if self._save_filter_changes():
                change = True
            else:
                change = False
        return change



    def _evaluate_baseline_changes(self):
        if self.uiWidgetBaselines.switched_baseline != self.NODE.current_baseline:
            return True
        return False
    
    def _evaluate_columns_changes(self):
        if self.uiListWidgetModuleColumns.get_all_items() != self.NODE.columns_names:
            return True
        return False
    
    def _evaluate_filter_changes(self):
        if not self.NODE.coverage_filter:
            if self.uiTexEditCoverageFilter.toPlainText().strip():
                return True
            return False
            
        if self.uiTexEditCoverageFilter.toPlainText().strip() != self.NODE.coverage_filter:
            return True
        return False
    

    def _save_baseline_changes(self):
        self.NODE.current_baseline = self.uiWidgetBaselines.switched_baseline


    def _save_columns_changes(self):
        self.NODE.columns_names = self.uiListWidgetModuleColumns.get_all_items()


    def _save_filter_changes(self):
        if self.NODE.columns_names != self.NODE.columns_names_backup:
            self.uiLabelNumberOfFilteredRequirements.setText("Columns changed - Download data from Doors first.")
            self.uiLabelNumberOfFilteredRequirements.setStyleSheet("color: red; font-size: 16px; margin-top: 10px;")
            return False

        filter_string = self.uiTexEditCoverageFilter.toPlainText().strip()
        filter_string = filter_string.replace("\n", " ")
        if filter_string:
            try:
                self._apply_coverage_filter(filter_string)
                success = True
                
            except Exception as ex:
                self.uiLabelNumberOfFilteredRequirements.setText("Wrong Filter: " + str(ex))
                self.uiLabelNumberOfFilteredRequirements.setStyleSheet("color: red; font-size: 16px; margin-top: 10px;")
                success = False
                raise
            
            return success

        else:
            self._remove_coverage_filter()
            return True    


    def _apply_coverage_filter(self, filter_string):
        self.NODE.apply_coverage_filter(filter_string)  
        self.uiLabelNumberOfFilteredRequirements.setText(f"Filtered: {self.NODE.number_of_calculated_requirements}")
        self.uiLabelNumberOfFilteredRequirements.setStyleSheet("color: green; font-size: 16px; margin-top: 10px;")
        self.uiListWidgetModuleColumns.setEnabled(False)
        self.uiWidgetBaselines.setEnabled(False)
            

    def _remove_coverage_filter(self):
        self.NODE.remove_coverage_filter()
        self.uiLabelNumberOfFilteredRequirements.setText("")
        self.uiListWidgetModuleColumns.setEnabled(True)
        self.uiWidgetBaselines.setEnabled(True)
        self.uiLabelWarning.hide()

           







    ##############################################################################################################################
    # COVERAGE FILTER - OPENING FORM AND RECEIVING BACK COVERAGE FILTER STRING:
    ##############################################################################################################################

    # @pyqtSlot(str)
    # def receive_data_from_req_filter_form(self, filter_string):
    #     index = self.TREE.currentIndex()
    #     node = self.MODEL.itemFromIndex(index)
    #     node.apply_coverage_filter(filter_string) 
    #     self._update_data_summary()
    #     # Remove View Filter
    #     self._show_all_items()       
    #     self.set_project_saved(False) 


    # def _remove_coverage_filter(self):
    #     index = self.TREE.currentIndex()
    #     requirement_file_node = self.MODEL.itemFromIndex(index)   
    #     requirement_file_node.remove_coverage_filter()
    #     self._update_data_summary()
    #     #  Remove View Filter
    #     self._show_all_items()
    #     self.set_project_saved(False)
    