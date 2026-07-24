from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, pyqtSignal

from dialogs.dialog_message import dialog_message
from ui.form_general_ui import Ui_Form


from data_manager.nodes.requirement_module import RequirementModule, RequirementNode
from data_manager.nodes.condition_file import ConditionNode, ValueNode, TestStepNode
from data_manager.nodes.dspace_nodes import DspaceVariableNode

from data_manager.forms.requirement_module_edit_layout import (
    RequirementModuleLayoutGenerator,
)
from data_manager.forms.simple_edit_layouts import (
    ConditionAndValueNodeLayoutGenerator,
    DspaceVariableNodeLayoutGenerator,
    RequirementNodeLayoutGenerator,
    TestStepNodeLayoutGenerator,
)


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
            self.resize(1000, 900)
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

