import re
from dataclasses import dataclass
from typing import Callable
from abc import ABC, abstractmethod

from PyQt5.QtGui import QStandardItem, QIcon, QTextCursor, QTextCharFormat, QColor, QCursor
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QLayout, QFrame, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QApplication
from PyQt5.QtCore import Qt
from data_manager.requirement_nodes import RequirementFileNode, RequirementNode
from data_manager.condition_nodes import ConditionFileNode, ConditionNode, ValueNode, TestStepNode
from data_manager.dspace_nodes import DspaceFileNode, DspaceDefinitionNode, DspaceVariableNode
from data_manager.a2l_nodes import A2lFileNode, A2lNode
from data_manager.data_manager import DataManager
from components.reduce_path_string import reduce_path_string
from data_manager.req_text_edit import RequirementTextEdit
from data_manager.widget_baseline import WidgetBaseline



@dataclass
class DisplayManager:

    DATA_MANAGER: DataManager

    def __post_init__(self):

        
        self.requirement_node_layout = RequirementNodeLayoutGenerator(self.DATA_MANAGER)
        self.requirement_module_layout = RequirementModuleLayoutGenerator(self.DATA_MANAGER)
        
        
        self.DATA_MANAGER.ui_layout_group_box.addWidget(self.requirement_node_layout.provide_layout())
        self.DATA_MANAGER.ui_layout_group_box.addWidget(self.requirement_module_layout.provide_layout())

        self._NODES_2_LAYOUT: dict = {
            RequirementNode:        self.requirement_node_layout.fill_with_data,
            RequirementFileNode:    self.requirement_module_layout.fill_with_data,
        }

    # INTERFACE FROM DATA_MANAGER
    def get_layout(self, node: QStandardItem) -> Callable | None:
        self.requirement_node_layout.provide_layout().setVisible(False)
        self.requirement_module_layout.provide_layout().setVisible(False)
        return self._NODES_2_LAYOUT[type(node)](node)      



    # def _display_requirement_node(self, node: QStandardItem) -> QLayout:
    #     return self.requirement_node_layout.fill_with_data(node)



class iLayoutGenerator(ABC):
    @abstractmethod
    def fill_with_data(self):
        """Get Data from Node and populate Widgets"""

    @abstractmethod
    def provide_layout(self):
        """Provide Layout (Frame) for main layout in Data Manager"""




class RequirementNodeLayoutGenerator(iLayoutGenerator):
    def __init__(self, DATA_MANAGER: DataManager) -> None:
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
        self.uiListWidgetLinks.itemDoubleClicked.connect(self.DATA_MANAGER._doubleclick_on_outlink)
        self.uiListWidgetScripts.itemDoubleClicked.connect(self.DATA_MANAGER._doubleclick_on_tc_reference) 
        self.uiBtnCopyReqRef.clicked.connect(self._copy_to_clipboard)    


    def _generate_header_layout(self):
        uiHeaderLayout = QHBoxLayout()
        self.uiLineEditIdentifier = QLineEdit()
        self.uiBtnCopyReqRef = QPushButton(QIcon(u"ui/icons/16x16/cil-copy.png"), "")
        self.uiBtnCopyReqRef.setCursor(QCursor(Qt.PointingHandCursor))
        uiHeaderLayout.addWidget(QLabel("Identifier:"))
        uiHeaderLayout.addWidget(self.uiLineEditIdentifier)
        uiHeaderLayout.addWidget(self.uiBtnCopyReqRef)
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
        columns_data = NODE.columns_data
        columns_names = NODE.MODULE.columns_names_backup
        # COLUMNS NAMES + DATA
        for i in range(len(columns_names)):
            text_to_display += f'<{columns_names[i]}>:\n{columns_data[i]} \n\n'
        self.uiRequirementTextEdit.setPlainText(text_to_display)        


    def _generate_links_scripts_layout(self):
        uiLinksScriptsLayout = QHBoxLayout()
        uiLinksScriptsLayout.addWidget(QLabel("Links:"))
        self.uiListWidgetLinks = QListWidget() 
        uiLinksScriptsLayout.addWidget(self.uiListWidgetLinks)
        uiLinksScriptsLayout.addWidget(QLabel("Scripts:"))
        self.uiListWidgetScripts = QListWidget() 
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
        # self.MAIN.show_notification(f"Item {self.ui_requirement_id.text()} copied to Clipboard.")                  








class RequirementModuleLayoutGenerator(iLayoutGenerator):
    def __init__(self, DATA_MANAGER: DataManager) -> None:
        self.DATA_MANAGER = DATA_MANAGER 
        self.uiMainLayout = QVBoxLayout()
        self.uiFrame = QFrame()
        self.uiFrame.setLayout(self.uiMainLayout)
        self.uiFrame.setVisible(False)
        self._generate_header_layout()  
        self._generate_baseline_layout()
        self._generate_columns_attributes_layout()  
        self._generate_ignore_list_layout()
        self._connect_signals()


    def provide_layout(self) -> QFrame:
        return self.uiFrame

    def fill_with_data(self, NODE):
        self.uiFrame.setVisible(True)
        self._fill_header_layout(NODE) 
        self._fill_columns_attributes_layout(NODE)
        self._fill_baseline_layout(NODE)
        self._fill_ignore_list_layout(NODE)


    def _connect_signals(self):
        self.uiListWidgetIgnoreList.itemDoubleClicked.connect(self.DATA_MANAGER._doubleclick_on_ignored_reference)


    def _generate_header_layout(self):
        uiModulePathLayout = QHBoxLayout()
        self.uiLineEditModulePath = QLineEdit()
        uiModulePathLayout.addWidget(QLabel("Path:"))
        uiModulePathLayout.addWidget(self.uiLineEditModulePath)

        uiTimestampLayout = QHBoxLayout()
        self.uiLineEditTimestamp = QLineEdit()
        uiTimestampLayout.addWidget(QLabel("Updated:"))
        uiTimestampLayout.addWidget(self.uiLineEditTimestamp)        
        
        uiCoverageFilterLayout = QHBoxLayout()
        self.uiLineEditCoverageFilter = QLineEdit()
        uiCoverageFilterLayout.addWidget(QLabel("Coverage:"))
        uiCoverageFilterLayout.addWidget(self.uiLineEditCoverageFilter)        
        
        self.uiMainLayout.addLayout(uiModulePathLayout)
        self.uiMainLayout.addLayout(uiTimestampLayout)
        self.uiMainLayout.addLayout(uiCoverageFilterLayout)        


    def _fill_header_layout(self, NODE):
        self.uiLineEditModulePath.setText(NODE.path)
        self.uiLineEditTimestamp.setText(NODE.timestamp)
        self.uiLineEditCoverageFilter.setText(NODE.coverage_filter)


    def _generate_baseline_layout(self):
        uiBaselineLayout = QHBoxLayout()
        uiBaselineLayout.addWidget(QLabel("Baseline:"))
        self.widget_baseline = WidgetBaseline()
        uiBaselineLayout.addWidget(self.widget_baseline)
        self.uiMainLayout.addLayout(uiBaselineLayout)

    def _fill_baseline_layout(self, NODE):
        self.widget_baseline.update(NODE)

    
    def _generate_columns_attributes_layout(self):
        uiAttributesColumnsLayout = QHBoxLayout()
        uiAttributesColumnsLayout.addWidget(QLabel("All:"))
        self.uiListWidgetAttributes = QListWidget() 
        uiAttributesColumnsLayout.addWidget(self.uiListWidgetAttributes)
        uiAttributesColumnsLayout.addWidget(QLabel("Current:"))
        self.uiListWidgetColumns = QListWidget() 
        uiAttributesColumnsLayout.addWidget(self.uiListWidgetColumns)        
        self.uiMainLayout.addLayout(uiAttributesColumnsLayout)  


    def _fill_columns_attributes_layout(self, NODE):
        self.uiListWidgetColumns.clear()
        self.uiListWidgetColumns.insertItems(0, NODE.columns_names)
        self.uiListWidgetAttributes.clear()
        self.uiListWidgetAttributes.insertItems(0, NODE.attributes) 


    def _generate_ignore_list_layout(self):
        self.uiListWidgetIgnoreList = QListWidget()
        uiIgnoreListLayout = QHBoxLayout()
        uiIgnoreListLayout.addWidget(QLabel("Ignored:"))
        uiIgnoreListLayout.addWidget(self.uiListWidgetIgnoreList)
        self.uiMainLayout.addLayout(uiIgnoreListLayout)

    def _fill_ignore_list_layout(self, NODE):
        self.uiListWidgetIgnoreList.clear()
        for item in NODE.ignore_list:
            ignore_lw_item = QListWidgetItem()    
            ignore_lw_item.setData(Qt.DisplayRole, reduce_path_string(item))
            ignore_lw_item.setData(Qt.UserRole, item)
            ignore_lw_item.setData(Qt.ToolTipRole, self.DATA_MANAGER._get_tooltip_from_link(f"{NODE.path}:{item.split('_')[-1]}"))
            self.uiListWidgetIgnoreList.insertItem(0, ignore_lw_item)   






        # self._show_filter_input(False)
        # self.ui_frame_requirement.setEnabled(True)
        # # self.ui_group_box_all_frames.setEnabled(False)




        # # Recover last filter if there is some
        # if selected_item:
        #     self.ui_le_filter.setText(selected_item.data(Qt.UserRole))
            

        # # ConditionFileNode, DspaceFileNode, A2lFileNode
        # if isinstance(selected_item, (ConditionFileNode, DspaceFileNode, A2lFileNode)):
        #     # self.ui_le_filter.setEnabled(True)
        #     self._show_filter_input(True)
        #     self.ui_frame_file.setVisible(True)
        #     self.ui_file_path.setText(selected_item.path)
        #     if isinstance(selected_item, (ConditionFileNode, DspaceFileNode)):
        #         # Buttons:
        #         self.ui_export.setEnabled(True)  
        #         self.ui_remove.setEnabled(True)          

        # # RequirementFileNode
        # elif isinstance(selected_item, RequirementFileNode):
        #     # self.ui_le_filter.setEnabled(True)
        #     # self.ui_le_filter.setVisible(True)
        #     self._show_filter_input(True)
        #     self.uiFrameRequirementModule.setVisible(True)
         

        # # Condition Area
        # elif isinstance(selected_item, ConditionNode):
        #     self.ui_frame_cond.setVisible(True)
        #     self.ui_cond_name.setText(selected_item.name)
        #     self.ui_cond_category.setText(selected_item.category)

        #     # Buttons:
        #     self.ui_edit.setEnabled(True)
        #     self.ui_add.setEnabled(True)
        #     self.ui_remove.setEnabled(True)
        # elif isinstance(selected_item, ValueNode):
        #     self.ui_frame_value.setVisible(True)
        #     self.ui_val_name.setText(selected_item.name)
        #     self.ui_val_category.setText(selected_item.category)

        #     # Buttons:
        #     self.ui_edit.setEnabled(True)
        #     self.ui_add.setEnabled(True)
        #     self.ui_remove.setEnabled(True)
        # elif isinstance(selected_item, TestStepNode):
        #     self.ui_frame_ts.setVisible(True)
        #     self.ui_ts_name.setText(selected_item.name)
        #     self.ui_ts_action.setText(selected_item.action)
        #     self.ui_ts_comment.setText(selected_item.comment)
        #     self.ui_ts_nominal.setText(selected_item.nominal)

        #     # Buttons:
        #     self.ui_edit.setEnabled(True)
        #     self.ui_add.setEnabled(True)
        #     self.ui_remove.setEnabled(True)
        #     self.ui_duplicate.setEnabled(True)

        # # dSpace Area
        # elif isinstance(selected_item, DspaceDefinitionNode):
        #     self.ui_frame_dspace_definition.setVisible(True)
        #     self.ui_ds_definition.setText(selected_item.name)
        # elif isinstance(selected_item, DspaceVariableNode):
        #     self.ui_frame_dspace_variable.setVisible(True)
        #     self.ui_ds_name.setText(selected_item.name)
        #     self.ui_ds_value.setText(selected_item.value)
        #     self.ui_ds_path.setText(selected_item.path)

        #     # Buttons:
        #     self.ui_edit.setEnabled(True)
        #     self.ui_add.setEnabled(True)
        #     self.ui_remove.setEnabled(True)
        #     self.ui_duplicate.setEnabled(True)
        # # A2L Area
        # elif isinstance(selected_item, A2lNode):
        #     self.ui_frame_a2l_variable.setVisible(True)
        #     self.ui_a2l_name.setText(selected_item.name)
        #     self.ui_a2l_address.setText(selected_item.address)

