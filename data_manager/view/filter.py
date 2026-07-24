from abc import ABC, abstractmethod
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from data_manager.nodes.condition_file import ConditionFileNode
from data_manager.nodes.dspace_nodes import DspaceFileNode
from data_manager.nodes.a2l_nodes import A2lFileNode
from data_manager.nodes.requirement_module import RequirementModule
from config import constants
from data_manager.view.filter_specifications import (
    AllSpecification,
    CoveredSpecification,
    FullTextRequirementSpecification,
    FullTextSpecification,
    IgnoredSpecification,
    NotCoveredSpecification,
    Specification,
)


######################################################################################################################################
### SPECIFICATION PATTERN:
######################################################################################################################################
### DEFINE INTERFACES:

class iFilter(ABC):
    @abstractmethod
    def filter(self, TREEVIEW, requirement_nodes, specification):
        pass

######################################################################################################################################
### DEFINE FILTERS:

class StandardFirstLevelFilter(iFilter):
    def filter(self, TREE, node: ConditionFileNode|A2lFileNode, specification: Specification):
        for row in range(node.rowCount()):
            subnode = node.child(row)
            if specification.is_satisfied(subnode):
                TREE.setRowHidden(row, node.index(), False)
            else:
                TREE.setRowHidden(row, node.index(), True)
            # self.filter(TREE, subnode, specification)


class StandardLastLevelFilter(iFilter):
    def filter(self, TREE, node: ConditionFileNode|A2lFileNode, specification: Specification):
        for row in range(node.rowCount()):
            subnode = node.child(row)
            if specification.is_satisfied(subnode):
                TREE.setRowHidden(row, node.index(), False)
                parent = subnode.parent()
                while parent and parent.parent():
                    TREE.setRowHidden(parent.row(), parent.parent().index(), False)
                    parent = parent.parent()                
            else:
                TREE.setRowHidden(row, node.index(), True)
            self.filter(TREE, subnode, specification)            


class DecoratedAutoExpandingLastLevelFilter(iFilter):
    def filter(self, TREE, node: RequirementModule|DspaceFileNode, specification: Specification):
        for row in range(node.rowCount()):
            subnode = node.child(row)
            if specification.is_satisfied(subnode):
                TREE.setRowHidden(row, node.index(), False)
                subnode.setForeground(QColor(0, 150, 0))
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


def _show_only_items_with_coverage(TREE, NODE):
    StandardLastLevelFilter().filter(TREE, NODE, CoveredSpecification() | NotCoveredSpecification())    


def _show_only_items_not_covered(TREE, NODE):
    StandardLastLevelFilter().filter(TREE, NODE, NotCoveredSpecification())

def _show_only_items_covered(TREE, NODE):
    StandardLastLevelFilter().filter(TREE, NODE, CoveredSpecification())

def _show_only_items_ignored(TREE, NODE):
    StandardLastLevelFilter().filter(TREE, NODE, IgnoredSpecification())


def _show_all_items(TREE, NODE):
    StandardLastLevelFilter().filter(TREE, NODE, AllSpecification())

def _show_only_items_with_coverage_with_text(TREE, NODE, text):
    DecoratedAutoExpandingLastLevelFilter().filter(TREE, NODE, (CoveredSpecification() | NotCoveredSpecification()) & FullTextRequirementSpecification(text))    


def _show_only_items_not_covered_with_text(TREE, NODE, text):
    DecoratedAutoExpandingLastLevelFilter().filter(TREE, NODE, NotCoveredSpecification() & FullTextRequirementSpecification(text))

def _show_only_items_covered_with_text(TREE, NODE, text):
    DecoratedAutoExpandingLastLevelFilter().filter(TREE, NODE, CoveredSpecification() & FullTextRequirementSpecification(text))

def _show_only_items_ignored_with_text(TREE, NODE, text):
    DecoratedAutoExpandingLastLevelFilter().filter(TREE, NODE, IgnoredSpecification() & FullTextRequirementSpecification(text))

def _show_all_items_with_text(TREE, NODE, text):
    DecoratedAutoExpandingLastLevelFilter().filter(TREE, NODE, AllSpecification() & FullTextRequirementSpecification(text))    



COVERAGE_VIEWS_NO_TEXT: dict = {
    constants.ViewCoverageFilter.ALL: _show_all_items,
    constants.ViewCoverageFilter.COVERED_AND_NOT_COVERED: _show_only_items_with_coverage,
    constants.ViewCoverageFilter.COVERED : _show_only_items_covered,
    constants.ViewCoverageFilter.NOT_COVERED : _show_only_items_not_covered,
    constants.ViewCoverageFilter.IGNORED : _show_only_items_ignored,
}

COVERAGE_VIEWS_WITH_TEXT: dict = {
    constants.ViewCoverageFilter.ALL: _show_all_items_with_text,
    constants.ViewCoverageFilter.COVERED_AND_NOT_COVERED: _show_only_items_with_coverage_with_text,
    constants.ViewCoverageFilter.COVERED : _show_only_items_covered_with_text,
    constants.ViewCoverageFilter.NOT_COVERED : _show_only_items_not_covered_with_text,
    constants.ViewCoverageFilter.IGNORED : _show_only_items_ignored_with_text,
}


######################################################################################################################################
### INTERFACE --> FUNCTION TRIGGERED BY WRITING TEXT to uiLineEditFilter / Changing uiComboCoverageFilter:

def filter(TREE, item, text, coverage, reset_filter):
    text = text.strip()
    if reset_filter:
        _reset_filter(TREE, item, text)
    filter_func = TYPES_2_FILTERS[type(item)]
    filter_func(TREE, item, text, coverage)
    

######################################################################################################################################
### SPECIFIC FILTERS:

def _filter_requirement_file(TREE, item, text, coverage_string):
    if text == "":
        coverage_func = COVERAGE_VIEWS_NO_TEXT[constants.ViewCoverageFilter(coverage_string)]
        coverage_func(TREE, item)
    else:      
        coverage_func = COVERAGE_VIEWS_WITH_TEXT[constants.ViewCoverageFilter(coverage_string)]
        coverage_func(TREE, item, text)


def _filter_dspace_file(TREE, item, text, coverage):
    DecoratedAutoExpandingLastLevelFilter().filter(TREE, item, FullTextSpecification(text)) if text else _reset_filter(TREE, item, text)



def _filter_condition_or_a2l_file(TREE, item, text, coverage):
    StandardFirstLevelFilter().filter(TREE, item, FullTextSpecification(text))





# RULES FOR SPECIFIC FILTERS:

TYPES_2_FILTERS: dict = {
    RequirementModule: _filter_requirement_file,
    DspaceFileNode: _filter_dspace_file,
    A2lFileNode: _filter_condition_or_a2l_file,
    ConditionFileNode: _filter_condition_or_a2l_file,    
}


# RESET FILTER:

def _reset_filter(TREE, selected_item, filtered_text):  # browse all nodes ->  collapse them + set foreground color to default
    selected_item_index = TREE.currentIndex()
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





def stop_filtering(TREE, selected_item, coverage_string):  # cancels filter (show all items) and leaves selection on current node
    
    selected_item.MODULE.setData("", Qt.UserRole) 
    selected_item_index = TREE.currentIndex()
    _reset_filter(TREE, selected_item.MODULE, "")
    
    _filter_requirement_file(TREE, selected_item.MODULE, "", coverage_string)
    
    # TREE.collapse_all_children()
    TREE.expand(selected_item_index)
    TREE.setCurrentIndex(selected_item_index)
    TREE.scrollTo(selected_item_index)












# def stop_filtering(TREE, MODEL):  # cancels filter (show all items) and leaves selection on current node
#     selected_item_index = TREE.currentIndex()
#     selected_item = MODEL.itemFromIndex(selected_item_index)
#     if isinstance(selected_item, RequirementNode):
#         module = selected_item.MODULE
#         if module.data(Qt.UserRole):  
#             def _collapse_all_children(node):
#                 for row in range(node.rowCount()):
#                     node_child = node.child(row)
#                     if node_child:
#                         TREE.collapse(node_child.index())
#                         node_child.setForeground(QColor(200, 200, 200))
#                         TREE.setRowHidden(row, node.index(), False)
#                     _collapse_all_children(node_child)   
            
#             _collapse_all_children(module)

#             parent = selected_item.parent()
#             while parent:
#                 TREE.expand(parent.index())
#                 parent = parent.parent()
#             TREE.scrollTo(selected_item_index)
#     elif isinstance(selected_item, RequirementFileNode):
#         # ui_le_filter.clear() !TODO: Check it!
#         selected_item.setData("", Qt.UserRole)
#         _reset_filter(TREE, MODEL, "")     



 











