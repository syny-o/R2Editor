from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QComboBox, QStyle, QToolButton
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtGui import QIcon, QCursor

from data_manager.nodes.requirement_module import RequirementModule
from data_manager.nodes.condition_file import ConditionFileNode
from data_manager.nodes.dspace_nodes import DspaceFileNode
from data_manager.nodes.a2l_nodes import A2lFileNode

from data_manager.view.tree import DataTreeView
from data_manager.view.display_manager import DisplayManager
from data_manager.view.view_actions import create_view_actions
from data_manager.view.view_filter_controller import ViewFilterController
from data_manager.view.view_layout import setup_view_layout
from config import constants
from config.icon_manager import IconManager


class View(QWidget):
    def __init__(self, DATA_MANAGER, MODEL):
        super().__init__()
        # MANAGERS
        self.DATA_MANAGER = DATA_MANAGER
        self.MODEL = MODEL
        self.DISPLAY_MANAGER = DisplayManager(DATA_MANAGER) 
        self.filter_controller = ViewFilterController(self)
        # TREE
        self.uiDataTreeView = DataTreeView(self)
        self.uiDataTreeView.setModel(self.MODEL)
        self.uiDataTreeView.customContextMenuRequested.connect(self._context_menu) 
        selection_model = self.uiDataTreeView.selectionModel()
        selection_model.selectionChanged.connect(self._update_view)  # update line edits on Up/Down Arrows          
        # FILTER - COMBO
        self.COMBO_ITEMS = [
            (constants.ViewCoverageFilter.ALL.value , IconManager().ICON_COMBO_All_ITEMS), 
            (constants.ViewCoverageFilter.COVERED_AND_NOT_COVERED.value, QIcon("ui/icons/xcheck.png")),
            (constants.ViewCoverageFilter.NOT_COVERED.value, QPushButton().style().standardIcon(QStyle.SP_DialogCancelButton)),
            (constants.ViewCoverageFilter.COVERED.value, QIcon("ui/icons/check.png")),
            (constants.ViewCoverageFilter.IGNORED.value , IconManager().ICON_IGNORED_ITEM), 
        ]        
        self.uiComboCoverageFilter = QComboBox()
        for text, icon in self.COMBO_ITEMS:
            self.uiComboCoverageFilter.addItem(icon, text)              
        self.uiComboCoverageFilter.currentTextChanged.connect(lambda: self._trigger_filtering(reset_filter=False))        
        # FILTER - LINE EDIT
        self.uiLineEditTextFilter = QLineEdit()
        # self.uiLineEditTextFilter.setTextMargins(20, 20, 20, 20)
        # self.uiLineEditTextFilter.addAction(QIcon(":/16x16/icons/16x16/cil-magnifying-glass.png"), QLineEdit.LeadingPosition)
        self.uiLineEditTextFilter.setClearButtonEnabled(True)
        # self.uiLineEditTextFilter.findChild(QToolButton).setIcon(IconManager().ICON_SEARCH_BOX_CLEAR)
        self.uiLineEditTextFilter.textChanged.connect(lambda: self._trigger_filtering(reset_filter=True))
        # TEXT FILTER LINE EDIT
        self.uiLineEditTextFilter.setPlaceholderText('Filter')
        self.uiLineEditTextFilter.addAction(IconManager().ICON_SEARCH_BOX_FIND, QLineEdit.LeadingPosition)        
        self.uiLineEditTextFilter.setMaximumHeight(0)        

        setup_view_layout(self)
        self._create_actions() 
        for toolbutton in self.uiControlToolbar.children():
            if isinstance(toolbutton, QToolButton):
                toolbutton.setCursor(QCursor(Qt.PointingHandCursor))  


    ##############################################################################################################
    # CREATE ACTIONS
    ##############################################################################################################             
    def _create_actions(self):
        self.ACTIONS_HANDLER = create_view_actions(self)

    ##############################################################################################################
    # UPDATE VIEW
    ##############################################################################################################

    def _update_view(self):
        self.uiLineEditTextFilter.setMaximumHeight(0)
        self.uiComboCoverageFilter.setVisible(False)
        self.uiBtnPreviousView.setEnabled(False)
        self.uiBtnExpandAllChildren.setEnabled(False)
        self.uiBtnCollapseAllChildren.setEnabled(False)
        index = self.uiDataTreeView.currentIndex()
        if not index.isValid():
            self.ACTIONS_HANDLER.update_actions(None)
            self.DISPLAY_MANAGER.get_layout(None)
            return
        item = self.MODEL.itemFromIndex(index)

        if isinstance(item, (RequirementModule, ConditionFileNode, DspaceFileNode, A2lFileNode)):
            self.uiLineEditTextFilter.setMaximumHeight(500)
            self.uiLineEditTextFilter.setText(item.data(Qt.UserRole))
        if isinstance(item, RequirementModule) and item.coverage_filter:            
            self.uiComboCoverageFilter.setVisible(True)
        if isinstance(item, RequirementModule):
            self.uiComboCoverageFilter.setCurrentText(item.view_filter.value)         

        if item.hasChildren():
            self.uiBtnExpandAllChildren.setEnabled(True)
            self.uiBtnCollapseAllChildren.setEnabled(True)

        self.uiBtnPreviousView.setEnabled(True)


        self.ACTIONS_HANDLER.update_actions(item)
        self.DISPLAY_MANAGER.get_layout(item)


    def _context_menu(self, point):
        selected_item_index = self.uiDataTreeView.indexAt(point)
        selected_item = self.MODEL.itemFromIndex(selected_item_index)

        if not selected_item_index.isValid():
            return

        if isinstance(selected_item, RequirementModule) and selected_item in self.DATA_MANAGER._module_locker.locked_modules:
            return
        
        menu = self.ACTIONS_HANDLER.get_context_menu(selected_item)
        
        if menu:                       
            menu.exec_(QCursor().pos())


    ##############################################################################################################
    # EVENTS
    ##############################################################################################################

    # EVENTS FROM DATA TREE VIEW
    def uiDataTreeView_received_files(self, data):
        """ Emits signal to DATA_MANAGER to load data from file or drop event """
        self.DATA_MANAGER.receive_data_from_drop_or_file_manager(data)

    def uiDataTreeView_current_index_changed(self, current_index: QModelIndex, previous_index: QModelIndex):
        """ Updates view"""
        item = self.MODEL.itemFromIndex(current_index)        
        if item:
            self._update_view()


    def _trigger_filtering(self, *, reset_filter: bool):
        self.filter_controller.trigger(reset_filter)

    def _stop_filtering(self):
        self.filter_controller.stop()
