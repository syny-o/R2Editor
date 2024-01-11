from dataclasses import dataclass, fields
from typing import Callable
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QAction, QMenu
from PyQt5.QtGui import QStandardItem


from data_manager.requirement_nodes import RequirementFileNode, RequirementNode
from data_manager.condition_nodes import ConditionFileNode, ConditionNode, ValueNode, TestStepNode
from data_manager.dspace_nodes import DspaceFileNode, DspaceDefinitionNode, DspaceVariableNode
from data_manager.a2l_nodes import A2lFileNode, A2lNode



@dataclass(kw_only=True)
class UIControlManager:
    # VIEW:
    action_expand_all_children:                     QAction
    action_collapse_all_children:                   QAction    
    # Standard operations with nodes:
    action_add_node:                                QAction
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
    action_open_coverage_filter:                    QAction
    action_edit_coverage_filter:                    QAction
    action_remove_coverage_filter:                  QAction    
    action_add_to_ignore_list:                      QAction
    action_remove_from_ignore_list:                 QAction
    action_show_only_requirements_with_coverage:    QAction    
    action_show_only_requirements_not_covered:      QAction
    action_show_all_requirements:                   QAction    


    def __post_init__(self):
        self.NODES_2_VIEW: dict = {
            RequirementFileNode: self._context_menu_requirement_module,
            RequirementNode: self._context_menu_requirement_node,
            ConditionFileNode: self._context_menu_condition_file_node,
            ConditionNode: self._context_menu_condition_value_test_step_node,
            ValueNode: self._context_menu_condition_value_test_step_node,
            TestStepNode: self._context_menu_condition_value_test_step_node,
            A2lFileNode: self._context_menu_a2l_file_node,
            A2lNode: self._context_menu_no_action,
            DspaceFileNode: self._context_menu_no_action,
            DspaceDefinitionNode: self._context_menu_no_action,
            DspaceVariableNode: self._context_menu_no_action,
        }

        # self._disable_all_actions()

        




    # INTERFACE FROM DATA_MANAGER
    def get_context_menu(self, node: QStandardItem) -> Callable | None:
        return self.NODES_2_VIEW[type(node)](node)  




    def _create_menu(self) -> QMenu:
        menu = QMenu()
        menu.setStyleSheet("QMenu::separator {height: 0.5px; margin: 3px; background-color: rgb(38, 59, 115);}")
        menu.addActions([self.action_expand_all_children, self.action_collapse_all_children])
        return menu




    def _context_menu_requirement_module(self, node: QStandardItem) -> QMenu:
        menu = self._create_menu()
        if not node.data(Qt.UserRole):  # if there is no FULLTEXT filter set within module (Search Line Edit is empty)
            menu.addActions([
                self.action_show_only_requirements_not_covered,
                self.action_show_only_requirements_with_coverage,
                self.action_show_all_requirements
            ])
        if not node.coverage_filter:
            menu.addAction(self.action_open_coverage_filter)
        else:
            menu.addActions([self.action_edit_coverage_filter, self.action_remove_coverage_filter])
        menu.addAction(self.action_update_module)
        return menu

    
    def _context_menu_requirement_node(self, node) -> QMenu:
        menu = self._create_menu()
        if not node.hasChildren():
            if node.reference in node.MODULE.ignore_list:                
                menu.addAction(self.action_remove_from_ignore_list)
            elif node.is_covered == False:
                menu.addAction(self.action_add_to_ignore_list)
        return menu


    def _context_menu_condition_file_node(self, node) -> QMenu:
        menu = self._create_menu()
        menu.addAction(self.action_export_node)
        return menu

    def _context_menu_condition_value_test_step_node(self, node) -> QMenu:
        menu = self._create_menu()
        menu.addActions([self.action_move_up_node, self.action_move_down_node])
        menu.addAction(self.action_duplicate_node)
        menu.addAction(self.action_copy_node)
        return menu


    def _context_menu_a2l_file_node(self, node) -> QMenu:
        menu = self._create_menu()
        menu.addAction(self.action_normalise_a2l_file)
        return menu      


    def _context_menu_no_action(self, node) -> QMenu:
        return None      




    # def _disable_all_actions(self):
    #     for field in fields(self):
    #         action = getattr(self, field.name)
    #         action.setEnabled(False)                    






    
    
    

        