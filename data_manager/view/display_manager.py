from dataclasses import dataclass
from typing import Callable, Type

from PyQt5.QtGui import QStandardItem

from data_manager.nodes.requirement_module import RequirementModule, RequirementNode
from data_manager.nodes.condition_file import ConditionFileNode, ConditionNode, ValueNode, TestStepNode
from data_manager.nodes.dspace_nodes import DspaceFileNode, DspaceDefinitionNode, DspaceVariableNode
from data_manager.nodes.a2l_nodes import A2lFileNode, A2lNode
from data_manager.view.simple_node_layouts import (
    A2lNodeLayoutGenerator,
    ConditionValueNodeLayoutGenerator,
    DspaceDefinitionNodeLayoutGenerator,
    DspaceVariableNodeLayoutGenerator,
    FileNodeLayoutGenerator,
    TestStepNodeLayoutGenerator,
)
from data_manager.view.requirement_module_layout import (
    RequirementModuleLayoutGenerator,
)
from data_manager.view.requirement_node_layout import (
    RequirementNodeLayoutGenerator,
)


@dataclass
class DisplayManager:

    DATA_MANAGER: Type

    def __post_init__(self):
        self.ALL_WIDGETS = []
        # 1. Create Widget and append it to ALL_WIDGETS
        self.requirement_node_layout = RequirementNodeLayoutGenerator(self.DATA_MANAGER)
        self.ALL_WIDGETS.append(self.requirement_node_layout)
        self.requirement_module_layout = RequirementModuleLayoutGenerator(self.DATA_MANAGER)
        self.ALL_WIDGETS.append(self.requirement_module_layout)
        self.file_node_layout = FileNodeLayoutGenerator(self.DATA_MANAGER)
        self.ALL_WIDGETS.append(self.file_node_layout)
        self.condition_value_node_layout = ConditionValueNodeLayoutGenerator(self.DATA_MANAGER)
        self.ALL_WIDGETS.append(self.condition_value_node_layout)
        self.test_step_node_layout = TestStepNodeLayoutGenerator(self.DATA_MANAGER)
        self.ALL_WIDGETS.append(self.test_step_node_layout)
        self.a2l_node_layout = A2lNodeLayoutGenerator(self.DATA_MANAGER)
        self.ALL_WIDGETS.append(self.a2l_node_layout)        
        self.dspace_definition_node_layout = DspaceDefinitionNodeLayoutGenerator(self.DATA_MANAGER)
        self.ALL_WIDGETS.append(self.dspace_definition_node_layout)        
        self.dspace_variable_node_layout = DspaceVariableNodeLayoutGenerator(self.DATA_MANAGER)
        self.ALL_WIDGETS.append(self.dspace_variable_node_layout) 

        # Add all widgets to Layout 
        for widget in self.ALL_WIDGETS:
            self.DATA_MANAGER.ui_layout_group_box.addWidget(widget.provide_layout())
        
        # 2. Add to Dictionary
        self._NODES_2_LAYOUT: dict = {
            RequirementNode:        self.requirement_node_layout.fill_with_data,
            RequirementModule:    self.requirement_module_layout.fill_with_data,
            ConditionFileNode:      self.file_node_layout.fill_with_data,
            A2lFileNode:            self.file_node_layout.fill_with_data,
            DspaceFileNode:         self.file_node_layout.fill_with_data,
            ConditionNode:          self.condition_value_node_layout.fill_with_data,
            ValueNode:              self.condition_value_node_layout.fill_with_data,
            TestStepNode:           self.test_step_node_layout.fill_with_data,
            A2lNode:                self.a2l_node_layout.fill_with_data,
            DspaceDefinitionNode:   self.dspace_definition_node_layout.fill_with_data,
            DspaceVariableNode:     self.dspace_variable_node_layout.fill_with_data,

            
        }

   
    # INTERFACE FROM DATA_MANAGER
    def get_layout(self, node: QStandardItem) -> Callable | None:

        for widget in self.ALL_WIDGETS:
            widget.provide_layout().setVisible(False)

        try:
            return self._NODES_2_LAYOUT[type(node)](node)
        
        except KeyError:
            return None

