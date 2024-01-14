from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor

from data_manager.condition_nodes import ConditionFileNode, ConditionNode, ValueNode, TestStepNode
from data_manager.dspace_nodes import DspaceFileNode, DspaceDefinitionNode, DspaceVariableNode
from data_manager.a2l_nodes import A2lFileNode
from data_manager.requirement_nodes import RequirementFileNode, RequirementNode


######################################################################################################################################
### FILTER ITEMS BY COVERAGE:
######################################################################################################################################

def evaluate_view_filter(TREE, MODEL, action_show_all_requirements, action_show_only_requirements_not_covered, action_show_only_requirements_with_coverage):
        index = TREE.currentIndex()
        requirement_file_node = MODEL.itemFromIndex(index)
        action_show_all_requirements.setIcon(QIcon())
        action_show_only_requirements_not_covered.setIcon(QIcon())
        action_show_only_requirements_with_coverage.setIcon(QIcon())
        view_filter = requirement_file_node.view_filter
        if view_filter == "all":
            action_show_all_requirements.setIcon(QIcon(u"ui/icons/24x24/cil-check-alt.png"))
        elif view_filter == "not_covered":
            action_show_only_requirements_not_covered.setIcon(QIcon(u"ui/icons/24x24/cil-check-alt.png"))
        else:
            action_show_only_requirements_with_coverage.setIcon(QIcon(u"ui/icons/24x24/cil-check-alt.png"))  




def show_only_items_with_coverage(TREE, MODEL):
    index = TREE.currentIndex()
    requirement_file_node = MODEL.itemFromIndex(index)

    def _browse_children(node, hide):         
        for row in range(node.rowCount()):
            requirement_node = node.child(row)
            if hide and requirement_node.node_icon is None:
                TREE.setRowHidden(row, node.index(), True)
            else:
                TREE.setRowHidden(row, node.index(), False)
            _browse_children(requirement_node, hide)

    _browse_children(requirement_file_node, hide=True)

    requirement_file_node.view_filter = "not_covered_plus_covered"  



def show_only_items_not_covered(TREE, MODEL):
    index = TREE.currentIndex()
    requirement_file_node = MODEL.itemFromIndex(index)

    def _browse_children(node, hide):         
        for row in range(node.rowCount()):
            requirement_node = node.child(row)
            if hide and requirement_node.node_icon == "red":
                TREE.setRowHidden(row, node.index(), False)
            else:
                TREE.setRowHidden(row, node.index(), True)
            _browse_children(requirement_node, hide)

    _browse_children(requirement_file_node, hide=True)

    requirement_file_node.view_filter = "not_covered"



def show_all_items(TREE, MODEL):
    index = TREE.currentIndex()
    requirement_file_node = MODEL.itemFromIndex(index)

    def _browse_children(node):         
        for row in range(node.rowCount()):
            requirement_node = node.child(row)
            TREE.setRowHidden(row, node.index(), False)
            _browse_children(requirement_node)

    _browse_children(requirement_file_node)

    requirement_file_node.view_filter = "all"  













######################################################################################################################################
### FILTER ITEMS BY FULLTEXT:
######################################################################################################################################

def filter_items(TREE, MODEL, filtered_text):
    selected_item_index = TREE.currentIndex()
    selected_item = MODEL.itemFromIndex(selected_item_index)  

    if not selected_item: return

    selected_item.setData(filtered_text, Qt.UserRole) # Save filter text to items QUserRole Data

    if isinstance(selected_item, (ValueNode, TestStepNode, DspaceDefinitionNode, DspaceVariableNode, RequirementNode)):
        return
    
    if isinstance(selected_item, (RequirementFileNode, RequirementNode)):      

        def _browse_children(node):         
            for row in range(node.rowCount()):
                requirement_node = node.child(row)
                if requirement_node:
                    data = " ".join(requirement_node.columns_data) + " " + str(requirement_node.reference)
            
                    if filtered_text.lower() in data.lower() :    
                        TREE.setRowHidden(row, node.index(), False)
                        requirement_node.setForeground(QColor("white"))
                        parent = requirement_node.parent()
                        while parent and parent.parent():
                            TREE.setRowHidden(parent.row(), parent.parent().index(), False)
                            TREE.expand(parent.index())
                            parent = parent.parent()
                    else:
                        TREE.setRowHidden(row, node.index(), True)
                        requirement_node.setForeground(QColor(90, 90, 90))
                        TREE.collapse(requirement_node.index())

                _browse_children(requirement_node)
        

        if filtered_text.strip() == "":
            if selected_item.view_filter == "not_covered_plus_covered":
                show_only_items_with_coverage(TREE, MODEL)
            elif selected_item.view_filter == "not_covered":
                show_only_items_not_covered(TREE, MODEL)
            return            
        
        else:
            _browse_children(selected_item)



    elif isinstance(selected_item, DspaceFileNode):
        
        if filtered_text.strip() != "":
            for row in range(selected_item.rowCount()):
                ds_definition = selected_item.child(row)
                rows_hidden = 0
                for definition_row in range(ds_definition.rowCount()):
                    if filtered_text.lower() in ds_definition.child(definition_row).text().lower():
                        TREE.setRowHidden(definition_row, ds_definition.index(), False)
                        TREE.expand(ds_definition.index())
                    else:
                        TREE.setRowHidden(definition_row, ds_definition.index(), True)
                        rows_hidden += 1
                    if rows_hidden == ds_definition.rowCount():
                        TREE.setRowHidden(row, selected_item.index(), True)
                    else:
                        TREE.setRowHidden(row, selected_item.index(), False)

        


    elif isinstance(selected_item, (ConditionFileNode, A2lFileNode)):
        for row in range(selected_item.rowCount()):
            if filtered_text.lower() in selected_item.child(row).text().lower():
                TREE.setRowHidden(row, selected_item_index, False)
            else:
                TREE.setRowHidden(row, selected_item_index, True)
  



def reset_filter(TREE, MODEL, filtered_text):
    selected_item_index = TREE.currentIndex()
    selected_item = MODEL.itemFromIndex(selected_item_index)     

    if selected_item and filtered_text.strip() == "":
        def _collapse_all_children(node):
            for row in range(node.rowCount()):
                node_child = node.child(row)
                if node_child:
                    TREE.collapse(node_child.index())
                    node_child.setForeground(QColor(200, 200, 200))
                    TREE.setRowHidden(row, node.index(), False)
                _collapse_all_children(node_child)   
        
        _collapse_all_children(selected_item)

        TREE.collapse(selected_item_index)

    else:
        TREE.expand(selected_item_index)  





def stop_filtering(TREE, MODEL):
    selected_item_index = TREE.currentIndex()
    selected_item = MODEL.itemFromIndex(selected_item_index)
    if isinstance(selected_item, RequirementNode):
        module = selected_item.MODULE
        if module.data(Qt.UserRole):  
            def _collapse_all_children(node):
                for row in range(node.rowCount()):
                    node_child = node.child(row)
                    if node_child:
                        TREE.collapse(node_child.index())
                        node_child.setForeground(QColor(200, 200, 200))
                        TREE.setRowHidden(row, node.index(), False)
                    _collapse_all_children(node_child)   
            
            _collapse_all_children(module)

            parent = selected_item.parent()
            while parent:
                TREE.expand(parent.index())
                parent = parent.parent()
            TREE.scrollTo(selected_item_index)
    elif isinstance(selected_item, RequirementFileNode):
        # ui_le_filter.clear() !TODO: Check it!
        selected_item.setData("", Qt.UserRole)
        reset_filter(TREE, MODEL, "")        