import re
from dataclasses import dataclass
from typing import Callable, Type

from PyQt5.QtGui import QStandardItem, QIcon, QTextCursor, QTextCharFormat, QColor
from PyQt5.QtWidgets import QToolButton, QListWidgetItem, QFrame, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QApplication
from PyQt5.QtCore import Qt

from data_manager.nodes.requirement_module import RequirementModule, RequirementNode
from data_manager.nodes.condition_file import ConditionFileNode, ConditionNode, ValueNode, TestStepNode
from data_manager.nodes.dspace_nodes import DspaceFileNode, DspaceDefinitionNode, DspaceVariableNode
from data_manager.nodes.a2l_nodes import A2lFileNode, A2lNode
from components.reduce_path_string import reduce_path_string
from components.widgets.widget_req_text_edit import RequirementTextEdit

from components.widgets.widgets_pointing_hand import ListWidgetPointingHand
from config.icon_manager import IconManager
from data_manager.view.layout_base import LayoutGenerator
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

        self.ICON_MANAGER = IconManager()       

        
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




class RequirementNodeLayoutGenerator(LayoutGenerator):
    def __init__(self, DATA_MANAGER: Type) -> None:
        self.DATA_MANAGER = DATA_MANAGER
        
        self.uiMainLayout = QVBoxLayout()
        self.uiMainLayout.setContentsMargins(0, 0, 0, 0)
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
        uiHeaderLayout.addWidget(QLabel("Id:    "))
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
        self.uiRequirementTextEdit.setReadOnly(True)
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
        self.uiListWidgetLinks = ListWidgetPointingHand() 
        self.uiListWidgetLinks.setMaximumHeight(120)
        uiLinksScriptsLayout.addWidget(self.uiListWidgetLinks)
        uiLinksScriptsLayout.addWidget(QLabel("Scripts:"))
        self.uiListWidgetScripts = ListWidgetPointingHand()
        self.uiListWidgetScripts.setMaximumHeight(120)
        uiLinksScriptsLayout.addWidget(self.uiListWidgetScripts)        
        self.uiMainLayout.addLayout(uiLinksScriptsLayout)
  
    def _fill_links_layout(self, NODE):
        self.uiListWidgetLinks.clear()
        for outlink in NODE.outlinks:
            outlink_lw_item = QListWidgetItem()
            outlink_lw_item.setData(Qt.DisplayRole, reduce_path_string(outlink))
            outlink_lw_item.setData(Qt.UserRole, outlink)
            outlink_lw_item.setData(Qt.DecorationRole, self.DATA_MANAGER.MAIN.ICON_MANAGER.ICON_OUTLINK)
            outlink_lw_item.setData(Qt.ToolTipRole, self.DATA_MANAGER._get_tooltip_from_link(outlink))
            self.uiListWidgetLinks.addItem(outlink_lw_item)
        for inlink in NODE.inlinks:
            inlink_lw_item = QListWidgetItem()
            inlink_lw_item.setData(Qt.DisplayRole, reduce_path_string(inlink))
            inlink_lw_item.setData(Qt.UserRole, inlink)
            inlink_lw_item.setData(Qt.ToolTipRole, self.DATA_MANAGER._get_tooltip_from_link(inlink))
            inlink_lw_item.setData(Qt.DecorationRole, self.DATA_MANAGER.MAIN.ICON_MANAGER.ICON_INLINK)
            self.uiListWidgetLinks.addItem(inlink_lw_item)         

    def _fill_scripts_layout(self, NODE):
        self.uiListWidgetScripts.clear()
        for file_reference in NODE.file_references:
            ref_lw_item = QListWidgetItem()
            ref_lw_item.setData(Qt.DisplayRole, reduce_path_string(file_reference))
            ref_lw_item.setData(Qt.UserRole, file_reference)
            ref_lw_item.setIcon(self.DATA_MANAGER.MAIN.ICON_MANAGER.ICON_SCRIPT_REFERENCE)
            self.uiListWidgetScripts.addItem(ref_lw_item)  


    def _generate_note_layout(self):
        uiNoteLayout = QHBoxLayout()
        self.uiTextEditNote = QTextEdit()
        self.uiTextEditNote.setMaximumHeight(50)
        self.uiTextEditNote.setReadOnly(True)
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
                f.setBackground(QColor(0, 150, 0))
                tc.setCharFormat(f) 

    
    def _copy_to_clipboard(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.uiLineEditIdentifier.text(), mode=cb.Clipboard)
        # TODO: Reduce coupling
        self.DATA_MANAGER.MAIN.show_notification(f"Item {self.uiLineEditIdentifier.text()} copied to Clipboard.")

