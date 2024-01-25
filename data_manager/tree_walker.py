import re
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem
from data_manager.nodes.requirement_module import RequirementModule



def find_node_by_identifier(parent_node: QStandardItem, identifier: str) -> QStandardItem:
    found_node = None

    for row in range(parent_node.rowCount()):            
        node = parent_node.child(row)
        if node.reference.lower() == identifier.lower():
            found_node = node
            break

        found_node = find_node_by_identifier(node, identifier)
        
        if found_node:
            return found_node
    
    return found_node




def at_least_one_module_is_present(root: QStandardItem) -> bool:
    for row in range(root.rowCount()):
        node = root.child(row)
        if type(node) == RequirementModule:
            return True
    return False



def is_module_present(root: QStandardItem, module_path: str) -> bool:
    for row in range(root.rowCount()):
        node = root.child(row)
        if type(node) == RequirementModule:
            if node.path == module_path:
                return True
    return False