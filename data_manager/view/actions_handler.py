from dataclasses import dataclass, fields
from typing import Callable
from PyQt5.QtCore import Qt, QItemSelection
from PyQt5.QtWidgets import QPushButton, QAction, QMenu, QLineEdit, QComboBox
from PyQt5.QtGui import QStandardItem
from data_manager.nodes.requirement_module import RequirementModule, RequirementNode
from data_manager.nodes.condition_nodes import ConditionFileNode, ConditionNode, ValueNode, TestStepNode
from data_manager.nodes.dspace_nodes import DspaceFileNode, DspaceDefinitionNode, DspaceVariableNode
from data_manager.nodes.a2l_nodes import A2lFileNode, A2lNode
from config.icon_manager import IconManager


COLOR_ENABLED_ACTION = '#2222c8'
COLOR_DISABLED_ACTION = '#ccc'


@dataclass(kw_only=True)
class ActionsHandler:
    DATA_MANAGER:                                   object
    # VIEW:
    action_expand_all_children:                     QAction
    action_collapse_all_children:                   QAction    
    # Standard operations with nodes:
    action_remove_node:                             QAction
    action_edit_node:                               QAction
    action_duplicate_node:                          QAction
    action_copy_node:                               QAction
    action_paste_node:                              QAction
    action_export_node:                             QAction
    action_move_up_node:                            QAction
    action_move_down_node:                          QAction
    # A2L:
    action_normalise_a2l_file:                      QAction
    # Requirements:
    action_update_module:                           QAction   
    action_add_to_ignore_list:                      QAction
    action_remove_from_ignore_list:                 QAction
    # Stop Filtering
    action_stop_filtering:                          QAction


  


    def __post_init__(self):
        self.NODES_2_VIEW: dict = {
            RequirementModule: self._context_menu_requirement_module,
            RequirementNode: self._context_menu_requirement_node,
            ConditionFileNode: self._context_menu_condition_dspace_file_node,
            ConditionNode: self._context_menu_condition_value_test_step_ds_variable_node,
            ValueNode: self._context_menu_condition_value_test_step_ds_variable_node,
            TestStepNode: self._context_menu_condition_value_test_step_ds_variable_node,
            A2lFileNode: self._context_menu_a2l_file_node,
            A2lNode: self._context_menu_no_action,
            DspaceFileNode: self._context_menu_condition_dspace_file_node,
            DspaceDefinitionNode: self._context_menu_no_action,
            DspaceVariableNode: self._context_menu_condition_value_test_step_ds_variable_node,

            QStandardItem: self._context_menu_no_action,  # Sometimes it gets QStandardItem (probably RootNode)
            QItemSelection: self._context_menu_no_action,  # Sometimes it gets QItemSelection
        }

        self._disable_all_actions()
        self._set_up_icons()




    def _set_up_icons(self) -> None:       
        self.action_remove_node.setIcon(IconManager().ICON_NODE_REMOVE)
        self.action_edit_node.setIcon(IconManager().ICON_NODE_EDIT)
        self.action_duplicate_node.setIcon(IconManager().ICON_NODE_DUPLICATE)
        self.action_copy_node.setIcon(IconManager().ICON_NODE_COPY)
        self.action_paste_node.setIcon(IconManager().ICON_NODE_PASTE)
        self.action_move_down_node.setIcon(IconManager().ICON_NODE_MOVE_DOWN)
        self.action_move_up_node.setIcon(IconManager().ICON_NODE_MOVE_UP)
        self.action_export_node.setIcon(IconManager().ICON_NODE_EXPORT)
        self.action_expand_all_children.setIcon(IconManager().ICON_EXPAND_ALL_CHILDREN)
        self.action_collapse_all_children.setIcon(IconManager().ICON_COLLAPSE_ALL_CHILDREN)
        self.action_normalise_a2l_file.setIcon(IconManager().ICON_NORMALISE_A2L_FILE)
        self.action_update_module.setIcon(IconManager().ICON_UPDATE_MODULE)
        self.action_add_to_ignore_list.setIcon(IconManager().ICON_ADD_TO_IGNORE_LIST)
        self.action_remove_from_ignore_list.setIcon(IconManager().ICON_REMOVE_FROM_IGNORE_LIST)
        self.action_stop_filtering.setIcon(IconManager().ICON_STOP_FILTERING)

    # INTERFACE FROM DATA_MANAGER
    def get_context_menu(self, node: QStandardItem) -> Callable | None:
        return self.NODES_2_VIEW[type(node)](node) 


    def update_actions(self, node: QStandardItem):
        self._disable_all_actions()
        try:
            self.NODES_2_VIEW[type(node)](node)
        except KeyError:
            pass



    def _create_menu(self) -> QMenu:
        menu = QMenu()
        menu.setStyleSheet("QMenu::separator {height: 0.5px; margin: 3px; background-color: rgb(100, 100, 100);}")
        activate_action(self.action_expand_all_children, menu)
        activate_action(self.action_collapse_all_children, menu)
        menu.addSeparator()
        return menu




    def _context_menu_requirement_module(self, node: QStandardItem) -> QMenu:
        menu = self._create_menu()
        menu.addSeparator()
        activate_action(self.action_edit_node, menu)
        menu.addSeparator()
        activate_action(self.action_update_module, menu)
        menu.addSeparator()
        activate_action(self.action_remove_node, menu)

        return menu

    
    def _context_menu_requirement_node(self, node) -> QMenu:
        menu = self._create_menu()
        activate_action(self.action_edit_node, menu)
        menu.addSeparator()
        if not node.hasChildren():
            if node.reference in node.MODULE.ignore_list:                
                activate_action(self.action_remove_from_ignore_list, menu)
            elif node.is_covered == False:
                activate_action(self.action_add_to_ignore_list, menu)
        
        if node.MODULE.data(Qt.UserRole):
            menu.addSeparator()
            activate_action(self.action_stop_filtering, menu)
        return menu


    def _context_menu_condition_dspace_file_node(self, node) -> QMenu:
        menu = self._create_menu()
        menu.addSeparator()
        activate_action(self.action_export_node, menu)         
        menu.addSeparator()
        activate_action(self.action_remove_node, menu)
        return menu

    def _context_menu_condition_value_test_step_ds_variable_node(self, node) -> QMenu:
        menu = self._create_menu()
        activate_action(self.action_edit_node, menu)
        activate_action(self.action_duplicate_node, menu)
        activate_action(self.action_copy_node, menu)

        if self.DATA_MANAGER.node_2_paste and type(self.DATA_MANAGER.node_2_paste) == type(node):
            activate_action(self.action_paste_node, menu)

        if node.row() > 0:  activate_action(self.action_move_up_node, menu)
        if node.row() < node.parent().rowCount()-1:  activate_action(self.action_move_down_node, menu)
        menu.addSeparator()
        activate_action(self.action_remove_node, menu)
      
        return menu


    def _context_menu_a2l_file_node(self, node) -> QMenu:
        menu = self._create_menu()
        activate_action(self.action_normalise_a2l_file, menu)
        menu.addSeparator()
        activate_action(self.action_remove_node, menu)   
        return menu      


    def _context_menu_no_action(self, node) -> QMenu:
        return None      




    def _disable_all_actions(self):
        for field in fields(self):
            action = getattr(self, field.name)
            if isinstance(action, QAction):
                action.setEnabled(False)  
            # action.setVisible(False)   
            

# Helper functions:
def activate_action(action: QAction, menu: QMenu):
    # action.setVisible(True)
    action.setEnabled(True)
    menu.addAction(action)



    
    
    

        