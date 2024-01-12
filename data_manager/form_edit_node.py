from PyQt5.QtWidgets import QWidget, QLabel, QListWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QTextEdit
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPalette

from dialogs.dialog_message import dialog_message
from ui.form_general_ui import Ui_Form


from data_manager.requirement_nodes import RequirementFileNode, RequirementNode
from data_manager.condition_nodes import ConditionFileNode, ConditionNode, ValueNode, TestStepNode
from data_manager.dspace_nodes import DspaceFileNode, DspaceDefinitionNode, DspaceVariableNode
from data_manager.a2l_nodes import A2lFileNode, A2lNode

from components.helper_functions import layout_generate_one_row as generate_one_row, validate_line_edits

stylesheet ="""
    QLabel {min-width: 120px; text-align: left;}
"""


class FormEditNode(QWidget, Ui_Form):

    node_was_updated = pyqtSignal()

    def __init__(self, NODE, DATA_MANAGER):
        super().__init__()
        self.setupUi(self)
        # self.setMinimumSize(1200, 600)
        # self.setStyleSheet(stylesheet)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowOpacity(0.95)        
        self.uiLabelTitle.setText("Edit")
        self.uiBtnStatusBarClose.clicked.connect(self.close)
        self.uiBtnTitleBarClose.clicked.connect(self.close)
        self.uiBtnOK.clicked.connect(self._ok_clicked)
        self.uiBtnOK.setShortcut('Return')
        self.show() 

        self.NODE = NODE
        self.node_was_updated.connect(DATA_MANAGER.edit_node_response)

        condition_and_value_node_layout_generator = ConditionAndValueNodeLayoutGenerator(self.NODE)
        test_step_node_layout_generator = TestStepNodeLayoutGenerator(self.NODE)
        dspace_variable_node_layout_generator = DspaceVariableNodeLayoutGenerator(self.NODE)
        requirement_node_layout_generator = RequirementNodeLayoutGenerator(self.NODE)
        
        self.NODES_2_LAYOUTS = {
            ConditionNode:      condition_and_value_node_layout_generator,
            ValueNode:          condition_and_value_node_layout_generator,
            TestStepNode:       test_step_node_layout_generator,
            DspaceVariableNode: dspace_variable_node_layout_generator,
            RequirementNode:    requirement_node_layout_generator,
        }


        self.uiMainLayout_2.addLayout(self.NODES_2_LAYOUTS[type(self.NODE)].provide_layout())



    def _ok_clicked(self):
        if self.NODES_2_LAYOUTS[type(self.NODE)].update_data():
            self.node_was_updated.emit()
            self.close()








class ConditionAndValueNodeLayoutGenerator:
    def __init__(self, NODE: ConditionNode|ValueNode) -> None:
        self.uiMainLayout = QVBoxLayout()
        self.uiMainLayout.setContentsMargins(100, 100, 100, 100)
        self.uiMainLayout.setSpacing(10)
        self.NODE = NODE       


    def _create_layout(self):
        self.uiLineEditName = generate_one_row("Name:", self.uiMainLayout)
        self.uiLineEditName.setText(self.NODE.name)
        self.uiLineEditCategory = generate_one_row("Category:", self.uiMainLayout)
        self.uiLineEditCategory.setText(self.NODE.category)
        
        # self.uiLineEditPath.setFocusPolicy(Qt.StrongFocus)
        # self.uiLineEditPath.setFocus()
        # self.uiLineEditPath.selectAll()  

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
        self.uiMainLayout.setContentsMargins(100, 100, 100, 100)
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
        
        # self.uiLineEditPath.setFocusPolicy(Qt.StrongFocus)
        # self.uiLineEditPath.setFocus()
        # self.uiLineEditPath.selectAll()  

    def provide_layout(self) -> QVBoxLayout:
        self._create_layout() 
        return self.uiMainLayout

    def update_data(self):
        if validate_line_edits(self.uiLineEditName, self.uiLineEditNominal, self.uiLineEditComment, self.uiLineEditAction):
            self.NODE.name = self.uiLineEditName.text()
            self.NODE.action = self.uiLineEditAction.text()
            self.NODE.comment = self.uiLineEditComment.text()
            self.NODE.nominal = self.uiLineEditNominal.text()
            self.NODE.get_file_node().set_modified(True)
            return True   



class DspaceVariableNodeLayoutGenerator:
    def __init__(self, NODE: DspaceVariableNode) -> None:
        self.uiMainLayout = QVBoxLayout()
        self.uiMainLayout.setContentsMargins(100, 100, 100, 100)
        self.uiMainLayout.setSpacing(10)
        self.NODE = NODE       


    def _create_layout(self):
        self.uiLineEditName = generate_one_row("Name:", self.uiMainLayout)
        self.uiLineEditName.setText(self.NODE.name)
        self.uiLineEditValue = generate_one_row("Value:", self.uiMainLayout)
        self.uiLineEditValue.setText(self.NODE.value)
        self.uiLineEditPath = generate_one_row("Path:", self.uiMainLayout)
        self.uiLineEditPath.setText(self.NODE.path)

        
        # self.uiLineEditPath.setFocusPolicy(Qt.StrongFocus)
        # self.uiLineEditPath.setFocus()
        # self.uiLineEditPath.selectAll()  

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
        self.uiMainLayout.setContentsMargins(100, 100, 100, 100)
        self.uiMainLayout.setSpacing(10)
        self.NODE = NODE       


    def _create_layout(self):
        l = QHBoxLayout()
        self.uiTextEditNote = QTextEdit(self.NODE.note)
        l.addWidget(QLabel("Note"))
        l.addWidget(self.uiTextEditNote)
        self.uiMainLayout.addLayout(l) 

    def provide_layout(self) -> QVBoxLayout:
        self._create_layout() 
        return self.uiMainLayout

    def update_data(self) -> bool:
        self.NODE.note = self.uiTextEditNote.toPlainText()
        return True    


        #     elif isinstance(selected_item, RequirementFileNode):
        #         selected_item.path = self.uiLineEditModulePath.text()
        #         selected_item.setText(reduce_path_string(selected_item.path))
        #         self.uiLisWidgetModuleColumns.setEnabled(False)
        #         self.uiListWidgetModuleIgnoreList.setEnabled(True)
        #         selected_item.columns_names = self.uiLisWidgetModuleColumns.get_all_items()



        # self.uiLisWidgetModuleColumns = MyListWidget()
        # self.uiLisWidgetModuleColumns.setEnabled(False)
        # self.uiLayoutModuleColumns.addWidget(self.uiLisWidgetModuleColumns)

        # self.uiLisWidgetModuleAttributes = MyListWidget(context_menu=False)
        # self.uiLisWidgetModuleAttributes.setEnabled(False)
        # self.uiLayoutModuleAttributes.addWidget(self.uiLisWidgetModuleAttributes)

    