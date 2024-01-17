from abc import ABC, abstractmethod
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor

from data_manager.condition_nodes import ConditionFileNode, ConditionNode, ValueNode, TestStepNode
from data_manager.dspace_nodes import DspaceFileNode, DspaceDefinitionNode, DspaceVariableNode
from data_manager.a2l_nodes import A2lFileNode, A2lNode
from data_manager.requirement_nodes import RequirementFileNode, RequirementNode


######################################################################################################################################
### SPECIFICATION PATTERN:
######################################################################################################################################
### DEFINE INTERFACES:

class iSpecification(ABC):
    @abstractmethod
    def is_satisfied(self, requirement_node):
        pass

    def __and__(self, other):
        return AndSpecification(self, other)
            

class iFilter(ABC):
    @abstractmethod
    def filter(self, TREEVIEW, requirement_nodes, specification):
        pass

######################################################################################################################################
### DEFINE SPECIFICATIONS:

class AndSpecification(iSpecification):
    def __init__(self, *args: iSpecification):
        self.args = args

    def is_satisfied(self, requirement_node):
        return all(map(lambda spec: spec.is_satisfied(requirement_node), self.args))

#-------------------------------------------------------------------------------------------------------------------------------------#

class NotCoveredSpecification(iSpecification):
    def is_satisfied(self, node: RequirementNode):
        return node.node_icon == "red" 


class CoveredAndNotCoveredSpecification(iSpecification):
    def is_satisfied(self, node: RequirementNode):
        return node.node_icon is not None 
    

class AllSpecification(iSpecification):
    def is_satisfied(self, node: RequirementNode):
        return node is not None  # just hack to return True for all nodes  


class FullTextRequirementSpecification(iSpecification):
    def __init__(self, filtered_text):
        self.filtered_text = filtered_text

    def is_satisfied(self, node: RequirementNode):
        data = " ".join(node.columns_data) + " " + str(node.reference)        
        return self.filtered_text.lower() in data.lower()


class FullTextSpecification(iSpecification):
    def __init__(self, filtered_text):
        self.filtered_text = filtered_text

    def is_satisfied(self, node: ConditionNode|A2lNode|DspaceVariableNode):
        return self.filtered_text.lower() in node.text().lower()          

######################################################################################################################################
### DEFINE FILTERS:

class StandardFilter(iFilter):
    def __init__(self, recursive=True) -> None:
        super().__init__()
        self.recursive = recursive

    def filter(self, TREE, node: RequirementFileNode|DspaceFileNode, specification: iSpecification):
        for row in range(node.rowCount()):
            subnode = node.child(row)
            if specification.is_satisfied(subnode):
                TREE.setRowHidden(row, node.index(), False)
            else:
                TREE.setRowHidden(row, node.index(), True)
            
            if self.recursive:
                self.filter(TREE, subnode, specification)



class DecoratedFilter(iFilter):
    def filter(self, TREE, node: RequirementFileNode|DspaceFileNode, specification: iSpecification):
        for row in range(node.rowCount()):
            subnode = node.child(row)
            if specification.is_satisfied(subnode):
                TREE.setRowHidden(row, node.index(), False)
                subnode.setForeground(QColor("white"))
                parent = subnode.parent()
                while parent and parent.parent():
                    TREE.setRowHidden(parent.row(), parent.parent().index(), False)
                    TREE.expand(parent.index())
                    parent = parent.parent()
            else:
                TREE.setRowHidden(row, node.index(), True)
                subnode.setForeground(QColor(90, 90, 90))
                TREE.collapse(subnode.index())  
            self.filter(TREE, subnode, specification)



######################################################################################################################################
### FUNCTIONS TRIGGERED BY ACTIONS FROM DATA MANAGER:

def show_only_items_with_coverage(TREE, MODEL):
    requirement_file_node = MODEL.itemFromIndex(TREE.currentIndex())    
    StandardFilter().filter(TREE, requirement_file_node, CoveredAndNotCoveredSpecification())    
    requirement_file_node.view_filter = "not_covered_plus_covered" 


def show_only_items_not_covered(TREE, MODEL):
    requirement_file_node = MODEL.itemFromIndex(TREE.currentIndex())
    StandardFilter().filter(TREE, requirement_file_node, NotCoveredSpecification())
    requirement_file_node.view_filter = "not_covered"


def show_all_items(TREE, MODEL):
    requirement_file_node = MODEL.itemFromIndex(TREE.currentIndex())
    StandardFilter().filter(TREE, requirement_file_node, AllSpecification())
    requirement_file_node.view_filter = "all"  



######################################################################################################################################
### FUNCTION TRIGGERED BY WRITING TEXT to uiLineEditFilter IN DATA MANAGER:


def filter_items(TREE, MODEL, filtered_text):
    selected_item_index = TREE.currentIndex()
    selected_item = MODEL.itemFromIndex(selected_item_index)  

    _reset_filter(TREE, MODEL, filtered_text)

    if not selected_item: return

    selected_item.setData(filtered_text, Qt.UserRole) # Save filter text to items QUserRole Data

    if isinstance(selected_item, (ValueNode, TestStepNode, DspaceDefinitionNode, DspaceVariableNode, RequirementNode)):
        return  # not necessary cause uiLineEditFilter is not visible for these nodes ( but just to be sure )
    
    if isinstance(selected_item, (RequirementFileNode)):                     

        if filtered_text.strip() != "":
            if selected_item.view_filter == "not_covered_plus_covered":
                DecoratedFilter().filter(TREE, selected_item, AndSpecification(FullTextRequirementSpecification(filtered_text), CoveredAndNotCoveredSpecification()))
            elif selected_item.view_filter == "not_covered":
                DecoratedFilter().filter(TREE, selected_item, AndSpecification(FullTextRequirementSpecification(filtered_text), NotCoveredSpecification()))
            else:
                DecoratedFilter().filter(TREE, selected_item, FullTextRequirementSpecification(filtered_text)) 
        
        else:
            # reset_filter(TREE, MODEL, filtered_text)
            if selected_item.view_filter == "not_covered_plus_covered":
                StandardFilter().filter(TREE, selected_item, CoveredAndNotCoveredSpecification())
            elif selected_item.view_filter == "not_covered":
                StandardFilter().filter(TREE, selected_item, NotCoveredSpecification())



    elif isinstance(selected_item, DspaceFileNode):
        DecoratedFilter().filter(TREE, selected_item, FullTextSpecification(filtered_text))
        

    elif isinstance(selected_item, (ConditionFileNode, A2lFileNode)):
        StandardFilter(recursive=False).filter(TREE, selected_item, FullTextSpecification(filtered_text))




def _reset_filter(TREE, MODEL, filtered_text):  # browse all nodes ->  collapse them + set foreground color to default
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
        _reset_filter(TREE, MODEL, "")     




######################################################################################################################################
### ADJUST APPEARANCE OF VIEW FILTER ACTIONS:
######################################################################################################################################
# TODO: Move this function to ui_control_manager? --> its just about icons in Context Menu
def evaluate_view_filter(TREE, MODEL, action_show_all_requirements, action_show_only_requirements_with_coverage, action_show_only_requirements_not_covered):
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











