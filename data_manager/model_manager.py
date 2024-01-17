from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtCore import Qt

from text_editor.completer import Completer
from data_manager.condition_nodes import ConditionFileNode, ConditionNode, ValueNode, TestStepNode
from data_manager.dspace_nodes import DspaceFileNode, DspaceDefinitionNode, DspaceVariableNode
from data_manager.requirement_nodes import RequirementNode
from data_manager.a2l_nodes import A2lFileNode, A2lNode
from text_editor.tooltips import tooltips




def export_file(selected_item):
    if isinstance(selected_item, (ConditionFileNode, DspaceFileNode)):
        try:
            selected_item.tree_2_file()
            return True, ""
        except Exception as e:
            return False, str(e)

def remove_node(TREE, MODEL):
    selected_item_index = TREE.currentIndex()
    selected_item = MODEL.itemFromIndex(selected_item_index)

    selected_item_row = selected_item_index.row()
    parent_item_index = selected_item_index.parent()

    if isinstance(selected_item, (RequirementNode, A2lNode)):
        return False

    if MODEL.rowCount(parent_item_index) > 1:        
        if hasattr(selected_item, 'get_file_node'):
            selected_item.get_file_node().set_modified(True)
        MODEL.removeRow(selected_item_row, parent_item_index)
        return True
    return False   


def duplicate_node(TREE, MODEL):
    selected_item_index = TREE.currentIndex()
    selected_item = MODEL.itemFromIndex(selected_item_index)
    if isinstance(selected_item, (ConditionNode, ValueNode, TestStepNode, DspaceVariableNode)):            
        selected_item.parent().insertRow(selected_item_index.row() + 1, selected_item.get_node_copy())        
        if hasattr(selected_item, 'get_file_node'):
            selected_item.get_file_node().set_modified(True)
            return True
    return False


def copy_node(TREE, MODEL):
    selected_item_index = TREE.currentIndex()
    selected_item = MODEL.itemFromIndex(selected_item_index)    
    if isinstance(selected_item, (ConditionNode, ValueNode, TestStepNode, DspaceVariableNode)):         
        return selected_item.get_node_copy()     


def paste_node(TREE, MODEL, node_to_paste):
    selected_item_index = TREE.currentIndex()
    selected_item = MODEL.itemFromIndex(selected_item_index)

    if node_to_paste is not None:
        if type(node_to_paste) == type(selected_item):
            new_item_row = selected_item_index.row() + 1
            selected_item.parent().insertRow(new_item_row, node_to_paste)            
            selected_item.get_file_node().set_modified(True) 
            return True
    return False
    

def move_node(TREE, MODEL, direction):
    selected_item_index = TREE.currentIndex()
    selected_item = MODEL.itemFromIndex(selected_item_index)
    
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
    MODEL.removeRow(selected_item_index.row(), selected_item_index.parent())
    parent.insertRow(new_item_row, item)
    
    TREE.setCurrentIndex(item.index())

    if hasattr(selected_item, 'get_file_node'):
        selected_item.get_file_node().set_modified(True)














def send_data_2_completer(ROOT):

    cond_tooltips = {}
    Completer.cond_tooltips.clear()
    cond_dict = {}
    cond_model = QStandardItemModel()
    a2l_model = QStandardItemModel()
    dspace_model = QStandardItemModel()

    for root_row in range(ROOT.rowCount()):
        current_file_node = ROOT.child(root_row, 0)
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
