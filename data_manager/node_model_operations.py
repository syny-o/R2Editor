from data_manager.nodes.condition_file import ConditionFileNode, ConditionNode, ValueNode, TestStepNode
from data_manager.nodes.dspace_nodes import DspaceFileNode, DspaceDefinitionNode, DspaceVariableNode
from data_manager.nodes.requirement_node import RequirementNode
from data_manager.nodes.a2l_nodes import A2lFileNode, A2lNode




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
