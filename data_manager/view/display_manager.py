import re
from dataclasses import dataclass
from typing import Callable, Type
from abc import ABC, abstractmethod

from PyQt5.QtGui import QStandardItem, QIcon, QTextCursor, QTextCharFormat, QColor, QCursor
from PyQt5.QtWidgets import QToolButton, QListWidgetItem, QLayout, QFrame, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QApplication, QStyle
from PyQt5.QtCore import Qt

from data_manager.nodes.requirement_module import RequirementModule, RequirementNode
from data_manager.nodes.condition_nodes import ConditionFileNode, ConditionNode, ValueNode, TestStepNode
from data_manager.nodes.dspace_nodes import DspaceFileNode, DspaceDefinitionNode, DspaceVariableNode
from data_manager.nodes.a2l_nodes import A2lFileNode, A2lNode
from components.reduce_path_string import reduce_path_string
from components.widgets.widget_req_text_edit import RequirementTextEdit
from components.widgets.widget_baseline import WidgetBaseline

from components.helper_functions import layout_generate_one_row as generate_one_row
from components.widgets.list_widget_event_filter import ListWidgetEventFilter


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




class iLayoutGenerator(ABC):
    @abstractmethod
    def fill_with_data(self):
        """Get Data from Node and display them in Widgets"""

    @abstractmethod
    def provide_layout(self):
        """Provide Layout (Frame) for main layout in Data Manager"""




class RequirementNodeLayoutGenerator(iLayoutGenerator):
    def __init__(self, DATA_MANAGER: Type) -> None:
        self.DATA_MANAGER = DATA_MANAGER
        
        self.uiMainLayout = QVBoxLayout()
        self.uiFrame = QFrame()
        self.uiFrame.setVisible(False)
        self.uiFrame.setLayout(self.uiMainLayout)
        self._generate_header_layout()
        self._generate_data_layout()
        self._generate_links_scripts_layout()
        self._generate_note_layout()
        self._connect_signals()


    def provide_layout(self) -> QFrame:
        return self.uiFrame

    def fill_with_data(self, NODE):
        self._fill_header_layout(NODE)
        self._fill_data_layout(NODE)
        self._fill_links_layout(NODE)
        self._fill_scripts_layout(NODE)
        self._fill_note_layout(NODE)
        self._highlight_fulltext_filter_results(NODE) 
        self.uiFrame.setVisible(True)  


    def _connect_signals(self):
        self.uiListWidgetLinks.itemClicked.connect(self.DATA_MANAGER._doubleclick_on_outlink)
        self.uiListWidgetScripts.itemClicked.connect(self.DATA_MANAGER._doubleclick_on_tc_reference) 
        # self.uiBtnCopyReqRef.clicked.connect(self._copy_to_clipboard)    


    def _generate_header_layout(self):
        uiHeaderLayout = QHBoxLayout()
        self.uiLineEditIdentifier = QLineEdit()
        # self.uiBtnCopyReqRef = QPushButton(QIcon(u"ui/icons/20x20/cil-copy.png"), "")
        # self.uiBtnCopyReqRef.setCursor(QCursor(Qt.PointingHandCursor))
        # self.uiBtnCopyReqRef.setToolTip("Copy Identifier")
        uiHeaderLayout.addWidget(QLabel("Id:    "))
        # uiHeaderLayout.addWidget(self.uiBtnCopyReqRef)
        uiHeaderLayout.addWidget(self.uiLineEditIdentifier)
        self.action_copy_identifier = self.uiLineEditIdentifier.addAction(QIcon(u"ui/icons/20x20/cil-copy.png"), QLineEdit.LeadingPosition)
        self.action_copy_identifier.triggered.connect(self._copy_to_clipboard)
        for widget in self.uiLineEditIdentifier.findChildren(QToolButton):
            widget.setCursor(Qt.PointingHandCursor)
        self.uiMainLayout.addLayout(uiHeaderLayout)

    def _fill_header_layout(self, NODE):
        self.uiLineEditIdentifier.setText(NODE.reference)


    def _generate_data_layout(self):
        uiDataLayout = QHBoxLayout()
        self.uiRequirementTextEdit = RequirementTextEdit(self.DATA_MANAGER)
        uiDataLayout.addWidget(QLabel("Data:"))
        uiDataLayout.addWidget(self.uiRequirementTextEdit)
        self.uiMainLayout.addLayout(uiDataLayout)

    def _fill_data_layout(self, NODE: RequirementNode):
        text_to_display = ''
        for name, value in zip(NODE.MODULE.columns_names_backup, NODE.columns_data):
            text_to_display += f'<{name}>:\n{value} \n\n'
        # self.uiRequirementTextEdit.setPlainText(text_to_display)        
        self.uiRequirementTextEdit.set_text(text_to_display)        


    def _generate_links_scripts_layout(self):
        uiLinksScriptsLayout = QHBoxLayout()
        uiLinksScriptsLayout.addWidget(QLabel("Links:"))
        self.uiListWidgetLinks = ListWidgetEventFilter() 
        self.uiListWidgetLinks.setMaximumHeight(120)
        uiLinksScriptsLayout.addWidget(self.uiListWidgetLinks)
        uiLinksScriptsLayout.addWidget(QLabel("Scripts:"))
        self.uiListWidgetScripts = ListWidgetEventFilter()
        self.uiListWidgetScripts.setMaximumHeight(120)
        uiLinksScriptsLayout.addWidget(self.uiListWidgetScripts)        
        self.uiMainLayout.addLayout(uiLinksScriptsLayout)
  
    def _fill_links_layout(self, NODE):
        self.uiListWidgetLinks.clear()
        for outlink in NODE.outlinks:
            outlink_lw_item = QListWidgetItem()
            outlink_lw_item.setData(Qt.DisplayRole, reduce_path_string(outlink))
            outlink_lw_item.setData(Qt.UserRole, outlink)
            outlink_lw_item.setData(Qt.DecorationRole, QIcon(u"ui/icons/20x20/cil-arrow-right.png"))
            outlink_lw_item.setData(Qt.ToolTipRole, self.DATA_MANAGER._get_tooltip_from_link(outlink))
            self.uiListWidgetLinks.addItem(outlink_lw_item)
        for inlink in NODE.inlinks:
            inlink_lw_item = QListWidgetItem()
            inlink_lw_item.setData(Qt.DisplayRole, reduce_path_string(inlink))
            inlink_lw_item.setData(Qt.UserRole, inlink)
            inlink_lw_item.setData(Qt.ToolTipRole, self.DATA_MANAGER._get_tooltip_from_link(inlink))
            inlink_lw_item.setData(Qt.DecorationRole, QIcon(u"ui/icons/20x20/cil-arrow-left.png"))
            self.uiListWidgetLinks.addItem(inlink_lw_item)         

    def _fill_scripts_layout(self, NODE):
        self.uiListWidgetScripts.clear()
        for file_reference in NODE.file_references:
            ref_lw_item = QListWidgetItem()
            ref_lw_item.setData(Qt.DisplayRole, reduce_path_string(file_reference))
            ref_lw_item.setData(Qt.UserRole, file_reference)
            ref_lw_item.setIcon(QIcon(u"ui/icons/16x16/cil-file.png"))
            self.uiListWidgetScripts.addItem(ref_lw_item)  


    def _generate_note_layout(self):
        uiNoteLayout = QHBoxLayout()
        self.uiTextEditNote = QTextEdit()
        self.uiTextEditNote.setMaximumHeight(50)
        uiNoteLayout.addWidget(QLabel("Note:"))
        uiNoteLayout.addWidget(self.uiTextEditNote)
        self.uiMainLayout.addLayout(uiNoteLayout)

    def _fill_note_layout(self, NODE):
        self.uiTextEditNote.setPlainText(NODE.note)        


    def _highlight_fulltext_filter_results(self, NODE):
        filter_text = NODE.MODULE.data(Qt.UserRole)
        if filter_text:
            text_edit_content = self.uiRequirementTextEdit.toPlainText()
            for match in re.finditer(filter_text, text_edit_content, re.IGNORECASE):
                # print('%02d-%02d: %s' % (m.start(), m.end(), m.group(0)))
                tc = self.uiRequirementTextEdit.textCursor()
                tc.setPosition(match.start())
                for _ in range(match.end() - match.start()):
                    tc.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor)
                f = QTextCharFormat()
                f.setBackground(QColor(255, 0, 0))
                tc.setCharFormat(f) 

    
    def _copy_to_clipboard(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.uiLineEditIdentifier.text(), mode=cb.Clipboard)
        # TODO: Reduce coupling
        self.DATA_MANAGER.MAIN.show_notification(f"Item {self.uiLineEditIdentifier.text()} copied to Clipboard.")                  





class RequirementModuleLayoutGenerator(iLayoutGenerator):
    def __init__(self, DATA_MANAGER: Type) -> None:
        self.DATA_MANAGER = DATA_MANAGER 
        self.uiMainLayout = QVBoxLayout()
        self.uiMainLayout.setSpacing(20)
        self.uiFrame = QFrame()
        self.uiFrame.setLayout(self.uiMainLayout)
        self.uiFrame.setVisible(False)
        self._generate_header_layout()  
        # self._generate_baseline_layout()
        # self._generate_columns_attributes_layout() 
        self._generate_covered_list_layout()
        self._generate_not_covered_list_layout() 
        self._generate_ignore_list_layout()
        self._connect_signals()

    def show_coverage_layout(self, show: bool):
        self.uiListWidgetCoveredList.setVisible(show)
        self.uiListWidgetNotCoveredList.setVisible(show)
        self.uiListWidgetIgnoreList.setVisible(show)
        self.uiLabelCovered.setVisible(show)
        self.uiLabelNotCovered.setVisible(show)
        self.uiLabelIgnored.setVisible(show)


    def provide_layout(self) -> QFrame:
        return self.uiFrame

    def fill_with_data(self, NODE):
        self.uiFrame.setVisible(True)
        self._fill_header_layout(NODE) 
        # self._fill_columns_attributes_layout(NODE)
        # self._fill_baseline_layout(NODE)
        self._fill_covered_list_layout(NODE)
        self._fill_not_covered_list_layout(NODE)
        self._fill_ignore_list_layout(NODE)
        self.show_coverage_layout(bool(NODE.coverage_filter))


    def _connect_signals(self):
        self.uiListWidgetIgnoreList.itemClicked.connect(self.DATA_MANAGER._doubleclick_on_identifier)
        self.uiListWidgetNotCoveredList.itemClicked.connect(self.DATA_MANAGER._doubleclick_on_identifier)
        self.uiListWidgetCoveredList.itemClicked.connect(self.DATA_MANAGER._doubleclick_on_identifier)


    def _generate_header_layout(self):
        self.uiLineEditModulePath = generate_one_row("Path:", self.uiMainLayout, extend_label_width=True)
        self.uiLineEditTimestamp = generate_one_row("Updated:", self.uiMainLayout, extend_label_width=True)


    def _fill_header_layout(self, NODE):
        self.uiLineEditModulePath.setText(NODE.path)
        self.uiLineEditTimestamp.setText(NODE.timestamp)


    def _generate_covered_list_layout(self):
        self.uiAllListLayout = QHBoxLayout()
        # self.uiAllListLayout.setSpacing(10)
        self.uiMainLayout.addLayout(self.uiAllListLayout)

        self.uiListWidgetCoveredList = ListWidgetEventFilter()
        uiCoveredListLayout = QVBoxLayout()
        self.uiLabelCovered = QLabel()
        self.uiLabelCovered.setStyleSheet("QLabel {color: rgb(0, 179, 0); min-width: 120px}")
        uiCoveredListLayout.addWidget(self.uiLabelCovered)
        uiCoveredListLayout.addWidget(self.uiListWidgetCoveredList)
        self.uiAllListLayout.addLayout(uiCoveredListLayout)

        self.uiListWidgetCoveredList.setMouseTracking(True)
        self.uiListWidgetCoveredList.itemEntered.connect(self.DATA_MANAGER.set_tooltip_2_list_widget_item)

    def _fill_covered_list_layout(self, NODE):
        self.uiLabelCovered.setText(f"Covered: {len(NODE.covered_requirements)}")
        self.uiListWidgetCoveredList.clear()
        for str_identifier in NODE.covered_requirements:    
            covered_lw_item = QListWidgetItem(self.uiListWidgetCoveredList)    
            covered_lw_item.setData(Qt.DisplayRole, str_identifier.split('-')[-1])
            if len(NODE.coverage_dict) < 500:
                covered_lw_item.setData(Qt.DecorationRole, QIcon(u"ui/icons/check.png"))
            covered_lw_item.setData(Qt.UserRole, str_identifier)
            # self.uiListWidgetCoveredList.insertItem(0, covered_lw_item)   

    def _generate_not_covered_list_layout(self):
        self.uiListWidgetNotCoveredList = ListWidgetEventFilter()
        uiNotCoveredListLayout = QVBoxLayout()
        self.uiLabelNotCovered = QLabel()
        self.uiLabelNotCovered.setStyleSheet("QLabel {color: rgb(250,50,50); min-width: 120px}")
        uiNotCoveredListLayout.addWidget(self.uiLabelNotCovered)
        uiNotCoveredListLayout.addWidget(self.uiListWidgetNotCoveredList)
        self.uiAllListLayout.addLayout(uiNotCoveredListLayout)

        self.uiListWidgetNotCoveredList.setMouseTracking(True)
        self.uiListWidgetNotCoveredList.itemEntered.connect(self.DATA_MANAGER.set_tooltip_2_list_widget_item)        

    def _fill_not_covered_list_layout(self, NODE):
        self.uiLabelNotCovered.setText(f"Not Covered: {len(NODE.not_covered_requirements)}")
        self.uiListWidgetNotCoveredList.clear()
        for str_identifier in NODE.not_covered_requirements:
            
            not_covered_lw_item = QListWidgetItem(self.uiListWidgetNotCoveredList)    
            not_covered_lw_item.setData(Qt.DisplayRole, str_identifier.split('-')[-1])
            if len(NODE.coverage_dict) < 500:
                not_covered_lw_item.setData(Qt.DecorationRole, QPushButton().style().standardIcon(QStyle.SP_DialogCancelButton))
            not_covered_lw_item.setData(Qt.UserRole, str_identifier)


    def _generate_ignore_list_layout(self):
        self.uiListWidgetIgnoreList = ListWidgetEventFilter()
        uiIgnoreListLayout = QVBoxLayout()
        self.uiLabelIgnored = QLabel()
        self.uiLabelIgnored.setStyleSheet("QLabel {min-width: 120px}")
        uiIgnoreListLayout.addWidget(self.uiLabelIgnored)
        uiIgnoreListLayout.addWidget(self.uiListWidgetIgnoreList)
        self.uiAllListLayout.addLayout(uiIgnoreListLayout)

        self.uiListWidgetIgnoreList.setMouseTracking(True)
        self.uiListWidgetIgnoreList.itemEntered.connect(self.DATA_MANAGER.set_tooltip_2_list_widget_item) 


    def _fill_ignore_list_layout(self, NODE):
        self.uiLabelIgnored.setText(f"Ignored: {len(NODE.ignore_list)}")        
        self.uiListWidgetIgnoreList.clear()
        for str_identifier in NODE.ignore_list:
            ignore_lw_item = QListWidgetItem()    
            ignore_lw_item.setData(Qt.DisplayRole, str_identifier.split('-')[-1])
            ignore_lw_item.setData(Qt.UserRole, str_identifier)
            ignore_lw_item.setData(Qt.DecorationRole, QIcon(u"ui/icons/16x16/cil-low-vision.png"))
            
            self.uiListWidgetIgnoreList.insertItem(0, ignore_lw_item)   



class SimpleNodeLayoutGenerator(iLayoutGenerator):
    def __init__(self, DATA_MANAGER: Type) -> None:
        self.DATA_MANAGER = DATA_MANAGER 
        self.uiMainLayout = QVBoxLayout()
        self.uiMainLayout.setSpacing(20)
        # self.uiMainLayout.setContentsMargins(0, 50, 0, 0)
        # self.uiMainLayout.setAlignment(Qt.AlignCenter)
        self.uiFrame = QFrame()
        self.uiFrame.setLayout(self.uiMainLayout)
        self.uiFrame.setVisible(False)

    def provide_layout(self) -> QFrame:
        return self.uiFrame

    def fill_with_data(self, NODE):
        self.uiFrame.setVisible(True)



class FileNodeLayoutGenerator(SimpleNodeLayoutGenerator):
    def __init__(self, DATA_MANAGER: Type) -> None:
        super().__init__(DATA_MANAGER)
        self._generate_layout()  

    def fill_with_data(self, NODE):
        super().fill_with_data(NODE)
        self._fill_layout(NODE)           
    
    def _generate_layout(self):
        self.uiLineEditFilePath = generate_one_row("Path:", self.uiMainLayout)

    def _fill_layout(self, NODE):
        self.uiLineEditFilePath.setText(NODE.path)    

     



class A2lNodeLayoutGenerator(SimpleNodeLayoutGenerator):
    def __init__(self, DATA_MANAGER: Type) -> None:
        super().__init__(DATA_MANAGER)
        self._generate_layout()  

    def fill_with_data(self, NODE):
        super().fill_with_data(NODE)
        self._fill_layout(NODE)  
    
    def _generate_layout(self):
        self.uiLineEditName = generate_one_row("Name:", self.uiMainLayout)
        self.uiLineEditAddress = generate_one_row("Address:", self.uiMainLayout)

    def _fill_layout(self, NODE):
        self.uiLineEditName.setText(NODE.name)  
        self.uiLineEditAddress.setText(NODE.address)  



class ConditionValueNodeLayoutGenerator(SimpleNodeLayoutGenerator):
    def __init__(self, DATA_MANAGER: Type) -> None:
        super().__init__(DATA_MANAGER)
        self._generate_layout()  

    def fill_with_data(self, NODE):
        super().fill_with_data(NODE)
        self._fill_layout(NODE)  
    
    def _generate_layout(self):
        self.uiLineEditName = generate_one_row("Name:", self.uiMainLayout)
        self.uiLineEditCategory = generate_one_row("Category:", self.uiMainLayout)

    def _fill_layout(self, NODE):
        self.uiLineEditName.setText(NODE.name)
        self.uiLineEditCategory.setText(NODE.category)



class TestStepNodeLayoutGenerator(SimpleNodeLayoutGenerator):
    def __init__(self, DATA_MANAGER: Type) -> None:
        super().__init__(DATA_MANAGER)
        self._generate_layout()  

    def fill_with_data(self, NODE):
        super().fill_with_data(NODE)
        self._fill_layout(NODE)  

    
    def _generate_layout(self):
        self.uiLineEditName = generate_one_row("Name:", self.uiMainLayout)
        self.uiLineEditAction = generate_one_row("Action:", self.uiMainLayout)
        self.uiLineEditComment = generate_one_row("Comment:", self.uiMainLayout)
        self.uiLineEditNominal = generate_one_row("Nominal:", self.uiMainLayout)

    def _fill_layout(self, NODE):
        self.uiLineEditName.setText(NODE.name)
        self.uiLineEditAction.setText(NODE.action)
        self.uiLineEditComment.setText(NODE.comment)
        self.uiLineEditNominal.setText(NODE.nominal)



class DspaceDefinitionNodeLayoutGenerator(SimpleNodeLayoutGenerator):
    def __init__(self, DATA_MANAGER: Type) -> None:
        super().__init__(DATA_MANAGER)
        self._generate_layout()  

    def fill_with_data(self, NODE):
        super().fill_with_data(NODE)
        self._fill_layout(NODE)  

    def _generate_layout(self):
        self.uiLineEditName = generate_one_row("Name:", self.uiMainLayout)

    def _fill_layout(self, NODE):
        self.uiLineEditName.setText(NODE.name)


class DspaceVariableNodeLayoutGenerator(SimpleNodeLayoutGenerator):
    def __init__(self, DATA_MANAGER: Type) -> None:
        super().__init__(DATA_MANAGER)
        self._generate_layout()  

    def fill_with_data(self, NODE):
        super().fill_with_data(NODE)
        self._fill_layout(NODE)  

    
    def _generate_layout(self):
        self.uiLineEditName = generate_one_row("Name:", self.uiMainLayout)
        self.uiLineEditValue = generate_one_row("Value:", self.uiMainLayout)
        self.uiLineEditPath = generate_one_row("Path:", self.uiMainLayout)

    def _fill_layout(self, NODE):
        self.uiLineEditName.setText(NODE.name)
        self.uiLineEditValue.setText(NODE.value)
        self.uiLineEditPath.setText(NODE.path)
    







    # uiCoverageFilterLayout = QHBoxLayout()
    # self.uiLineEditCoverageFilter = QLineEdit()
    # uiCoverageFilterLayout.addWidget(QLabel("Coverage:"))
    # uiCoverageFilterLayout.addWidget(self.uiLineEditCoverageFilter)        
    
    # self.uiMainLayout.addLayout(uiTimestampLayout)
    # self.uiMainLayout.addLayout(uiCoverageFilterLayout)   


    # self.uiLineEditCoverageFilter.setText(NODE.coverage_filter)


    # def _generate_baseline_layout(self):
    #     uiBaselineLayout = QHBoxLayout()
    #     uiBaselineLayout.addWidget(QLabel("Baseline:"))
    #     self.widget_baseline = WidgetBaseline()
    #     uiBaselineLayout.addWidget(self.widget_baseline)
    #     # self.uiMainLayout.addLayout(uiBaselineLayout)

    # def _fill_baseline_layout(self, NODE):
    #     self.widget_baseline.update(NODE)

    
    # def _generate_columns_attributes_layout(self):
    #     uiAttributesColumnsLayout = QHBoxLayout()
    #     uiAttributesColumnsLayout.addWidget(QLabel("All:"))
    #     self.uiListWidgetAttributes = QListWidget() 
    #     uiAttributesColumnsLayout.addWidget(self.uiListWidgetAttributes)
    #     uiAttributesColumnsLayout.addWidget(QLabel("Current:"))
    #     self.uiListWidgetColumns = QListWidget() 
    #     uiAttributesColumnsLayout.addWidget(self.uiListWidgetColumns)        
    #     # self.uiMainLayout.addLayout(uiAttributesColumnsLayout)  


    # def _fill_columns_attributes_layout(self, NODE):
    #     self.uiListWidgetColumns.clear()
    #     self.uiListWidgetColumns.insertItems(0, NODE.columns_names)
    #     self.uiListWidgetAttributes.clear()
    #     self.uiListWidgetAttributes.insertItems(0, NODE.attributes) 











            



