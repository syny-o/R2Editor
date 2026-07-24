from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QToolBar,
    QVBoxLayout,
)

from config.icon_manager import IconManager


def setup_view_layout(view):
    icons = IconManager()

    view.uiBtnPreviousView = QPushButton()
    view.uiBtnPreviousView.setIcon(icons.ICON_PREVIOUS_VIEW)
    view.uiBtnPreviousView.clicked.connect(
        view.uiDataTreeView.goto_previous_index
    )
    view.uiBtnPreviousView.setToolTip("Previous View")
    view.uiBtnPreviousView.setCursor(QCursor(Qt.PointingHandCursor))
    view.uiBtnPreviousView.setMinimumWidth(150)
    view.uiBtnPreviousView.setText(" Previous View")

    view.uiBtnExpandAllChildren = QPushButton()
    view.uiBtnExpandAllChildren.setIcon(icons.ICON_EXPAND_ALL_CHILDREN)
    view.uiBtnExpandAllChildren.clicked.connect(
        view.uiDataTreeView.expand_all_children
    )
    view.uiBtnExpandAllChildren.setToolTip("Expand All Children")
    view.uiBtnExpandAllChildren.setCursor(
        QCursor(Qt.PointingHandCursor)
    )

    view.uiBtnCollapseAllChildren = QPushButton()
    view.uiBtnCollapseAllChildren.setIcon(
        icons.ICON_COLLAPSE_ALL_CHILDREN
    )
    view.uiBtnCollapseAllChildren.clicked.connect(
        view.uiDataTreeView.collapse_all_children
    )
    view.uiBtnCollapseAllChildren.setToolTip("Collapse All")
    view.uiBtnCollapseAllChildren.setCursor(
        QCursor(Qt.PointingHandCursor)
    )

    view.uiComboCoverageFilter.setVisible(False)

    filter_layout = QHBoxLayout()
    filter_layout.addWidget(view.uiBtnExpandAllChildren)
    filter_layout.addWidget(view.uiBtnCollapseAllChildren)
    filter_layout.addWidget(view.uiLineEditTextFilter)
    filter_layout.addWidget(view.uiComboCoverageFilter)
    filter_layout.addWidget(view.uiBtnPreviousView)
    filter_layout.setAlignment(Qt.AlignLeft)

    view.uiControlToolbar = QToolBar()
    view.uiControlToolbar.setToolButtonStyle(
        Qt.ToolButtonTextUnderIcon
    )

    main_layout = QVBoxLayout()
    main_layout.addLayout(filter_layout)
    main_layout.addWidget(view.uiControlToolbar)
    main_layout.addWidget(view.uiDataTreeView)
    view.setLayout(main_layout)
