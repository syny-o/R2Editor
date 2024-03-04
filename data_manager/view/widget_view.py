from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QToolBar, QPushButton, QLineEdit, QComboBox, QStyle, QToolButton, QAction
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtGui import QIcon, QCursor

from data_manager.nodes.requirement_module import RequirementModule
from data_manager.nodes.requirement_node import RequirementNode
from data_manager.nodes.condition_nodes import ConditionFileNode
from data_manager.nodes.dspace_nodes import DspaceFileNode
from data_manager.nodes.a2l_nodes import A2lFileNode

from data_manager.view.tree import DataTreeView
from data_manager.view import filter
from data_manager.view import help_func
from data_manager.view.actions_handler import ActionsHandler
from data_manager.view.display_manager import DisplayManager
from config import constants
from config.icon_manager import IconManager


class View(QWidget):
    def __init__(self, DATA_MANAGER, MODEL):
        super().__init__()
        # MANAGERS
        self.DATA_MANAGER = DATA_MANAGER
        self.MODEL = MODEL
        self.DISPLAY_MANAGER = DisplayManager(DATA_MANAGER) 
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

        self._setup_ui() 
        self._create_actions() 
        for toolbutton in self.uiControlToolbar.children():
            if isinstance(toolbutton, QToolButton):
                toolbutton.setCursor(QCursor(Qt.PointingHandCursor))  


    ##############################################################################################################
    # CREATE ACTIONS
    ##############################################################################################################             
    def _create_actions(self):     
        self.action_expand_all_children = help_func.create_action(':/16x16/icons/16x16/cil-expand-down.png', 'Expand All', slot=self.uiDataTreeView.expand_all_children, toolbar=None)
        self.action_collapse_all_children = help_func.create_action(':/16x16/icons/16x16/cil-expand-up.png', 'Collapse All', slot=self.uiDataTreeView.collapse_all_children, toolbar=None)
        self.action_goto_previous_index = help_func.create_action(':/16x16/icons/16x16/cil-chevron-left.png', 'Previous', slot=self.uiDataTreeView.goto_previous_index, toolbar=None)
        # Standard operations with nodes:
        self.action_move_up = help_func.create_action(':/16x16/icons/16x16/cil-chevron-top.png', 'Move Up', slot=lambda: self.DATA_MANAGER.move_node(direction='up'), shortcut="Ctrl+Up", toolbar=self.uiControlToolbar)
        self.action_move_down = help_func.create_action(':/16x16/icons/16x16/cil-chevron-bottom.png', 'Move Down', slot=lambda: self.DATA_MANAGER.move_node(direction='down'), shortcut="Ctrl+Down", toolbar=self.uiControlToolbar)
        self.action_duplicate = help_func.create_action(':/16x16/icons/16x16/cil-library.png', 'Duplicate', slot=self.DATA_MANAGER.duplicate_node, shortcut="Ctrl+D", toolbar=self.uiControlToolbar)
        self.action_copy = help_func.create_action(':/16x16/icons/16x16/cil-clone.png', 'Copy', slot=self.DATA_MANAGER.copy_node, shortcut="Ctrl+C", toolbar=self.uiControlToolbar)
        self.action_paste = help_func.create_action(':/16x16/icons/16x16/cil-plus.png', 'Paste', slot=self.DATA_MANAGER.paste_node, shortcut="Ctrl+V", toolbar=self.uiControlToolbar)
        self.action_edit = help_func.create_action(':/16x16/icons/16x16/cil-pencil.png', 'Edit', slot=self.DATA_MANAGER.edit_node_request, shortcut="F4", toolbar=self.uiControlToolbar)
        self.action_remove = help_func.create_action(':/16x16/icons/16x16/cil-x.png', 'Remove', slot=self.DATA_MANAGER.remove_node, shortcut="Del", toolbar=self.uiControlToolbar)
        # File Nodes:
        self.action_export = help_func.create_action(':/16x16/icons/16x16/cil-save.png', 'Export', slot=self.DATA_MANAGER.tree_2_file, shortcut="Ctrl+E",toolbar=self.uiControlToolbar)
        self.action_normalise_a2l_file = help_func.create_action(':/16x16/icons/16x16/cil-chart-line.png', 'Normalise (VDA spec.)', slot=self.DATA_MANAGER._normalise_a2l_file, toolbar=None)
        self.action_update_module = help_func.create_action(':/16x16/icons/16x16/cil-cloud-download.png', 'Update', slot=lambda: self.DATA_MANAGER._open_form_for_doors_connection_inputs(all_modules=False), toolbar=None)
        self.action_add_to_ignore_list = help_func.create_action(':/16x16/icons/16x16/cil-task.png', 'Add To Ignore List', slot=self.DATA_MANAGER._add_to_ignore_list, toolbar=None)
        self.action_remove_from_ignore_list = help_func.create_action(':/16x16/icons/16x16/cil-external-link.png', 'Remove From Ignore List', slot=self.DATA_MANAGER._remove_from_ignore_list, toolbar=None)
        # Stop Filtering
        self.action_stop_filtering = help_func.create_action(':/16x16/icons/16x16/cil-x.png', 'Remove Text Filter', slot=self._stop_filtering, toolbar=None)
        # Actions Handler:
        self.ACTIONS_HANDLER = ActionsHandler(

            # TODO: refactor this
            DATA_MANAGER=self.DATA_MANAGER,

            action_expand_all_children=self.action_expand_all_children,
            action_collapse_all_children=self.action_collapse_all_children,
            action_remove_node=self.action_remove,
            action_edit_node=self.action_edit,
            action_duplicate_node=self.action_duplicate,
            action_copy_node=self.action_copy,
            action_paste_node=self.action_paste,
            action_export_node=self.action_export,
            action_move_up_node=self.action_move_up,
            action_move_down_node=self.action_move_down,
            action_normalise_a2l_file=self.action_normalise_a2l_file,
            action_update_module=self.action_update_module,
            action_add_to_ignore_list=self.action_add_to_ignore_list,
            action_remove_from_ignore_list=self.action_remove_from_ignore_list,

            action_stop_filtering=self.action_stop_filtering,


        )        

    ##############################################################################################################
    # SETUP UI
    ##############################################################################################################
    def _setup_ui(self):
        # FILTER + TREE NAVIGATION AREA
        self.uiBtnPreviousView = QPushButton()
        self.uiBtnPreviousView.setIcon(IconManager().ICON_PREVIOUS_VIEW)
        self.uiBtnPreviousView.clicked.connect(self.uiDataTreeView.goto_previous_index)
        self.uiBtnPreviousView.setToolTip("Previous View")
        self.uiBtnPreviousView.setCursor(QCursor(Qt.PointingHandCursor))
        self.uiBtnPreviousView.setMinimumWidth(150)
        self.uiBtnPreviousView.setText(" Previous View")
        # uiBtnPreviousView.setStyleSheet("font-size: 14px;")
        self.uiBtnExpandAllChildren = QPushButton()
        self.uiBtnExpandAllChildren.setIcon(IconManager().ICON_EXPAND_ALL_CHILDREN)
        self.uiBtnExpandAllChildren.clicked.connect(self.uiDataTreeView.expand_all_children)
        self.uiBtnExpandAllChildren.setToolTip("Expand All Children")
        self.uiBtnExpandAllChildren.setCursor(QCursor(Qt.PointingHandCursor))
        self.uiBtnCollapseAllChildren = QPushButton()
        self.uiBtnCollapseAllChildren.setIcon(IconManager().ICON_COLLAPSE_ALL_CHILDREN)
        self.uiBtnCollapseAllChildren.clicked.connect(self.uiDataTreeView.collapse_all_children)
        self.uiBtnCollapseAllChildren.setToolTip("Collapse All")
        self.uiBtnCollapseAllChildren.setCursor(QCursor(Qt.PointingHandCursor))


        # COVERAGE FILTER COMBO
        self.uiComboCoverageFilter.setVisible(False) 
        # FILTER LAYOUT
        uiFilterLayout = QHBoxLayout()
        uiFilterLayout.addWidget(self.uiBtnExpandAllChildren)
        uiFilterLayout.addWidget(self.uiBtnCollapseAllChildren)
        uiFilterLayout.addWidget(self.uiLineEditTextFilter)
        uiFilterLayout.addWidget(self.uiComboCoverageFilter) 
        uiFilterLayout.addWidget(self.uiBtnPreviousView)
        uiFilterLayout.setAlignment(Qt.AlignLeft)       
        # CONTROL TOOLBAR
        self.uiControlToolbar = QToolBar()
        self.uiControlToolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        # MAIN LAYOUT
        uiMainLayout = QVBoxLayout()
        uiMainLayout.addLayout(uiFilterLayout)
        uiMainLayout.addWidget(self.uiControlToolbar)
        uiMainLayout.addWidget(self.uiDataTreeView)
        self.setLayout(uiMainLayout)
        

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


    # FILTER EVENTS
    # def uiLineEditTextFilter_textChanged(self, text):
    #     """ Filters data by text """
    #     self._trigger_filtering(reset_filter=True)


    # def uiComboCoverageFilter_currentTextChanged(self, text):
    #     """ Filters data by coverage """
    #     self._trigger_filtering(reset_filter=False)


    def _trigger_filtering(self, *, reset_filter: bool):
        """ Triggers filtering """
        text = self.uiLineEditTextFilter.text()
        coverage = self.uiComboCoverageFilter.currentText()

        current_index = self.uiDataTreeView.currentIndex()
        if not current_index.isValid():
            return
        item = self.MODEL.itemFromIndex(current_index)

        if isinstance(item, RequirementNode):  # just hack to avoid filtering of RequirementNode (when STOP FILTERING is clicked)
            return

        item.view_filter = constants.ViewCoverageFilter(coverage)
        item.setData(text, Qt.UserRole)

        filter.filter(self.uiDataTreeView, item, text, coverage, reset_filter=reset_filter)




    def _stop_filtering(self):
        """ Stops filtering (just text filtering), COVERAGE view filter remains active"""
        coverage = self.uiComboCoverageFilter.currentText()
        current_index = self.uiDataTreeView.currentIndex()
        if not current_index.isValid():
            return

        self.uiLineEditTextFilter.clear()

        item = self.MODEL.itemFromIndex(current_index)
        filter.stop_filtering(self.uiDataTreeView, item, coverage)

        
