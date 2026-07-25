from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidgetItem,
    QVBoxLayout,
)

from components.helper_functions import (
    layout_generate_one_row as generate_one_row,
)
from components.widgets.widgets_pointing_hand import ListWidgetPointingHand
from data_manager.view.layout_base import LayoutGenerator


class RequirementModuleLayoutGenerator(LayoutGenerator):
    def __init__(self, data_manager):
        self.DATA_MANAGER = data_manager
        self.uiMainLayout = QVBoxLayout()
        self.uiMainLayout.setSpacing(20)
        self.uiMainLayout.setContentsMargins(0, 0, 0, 0)
        self.uiFrame = QFrame()
        self.uiFrame.setLayout(self.uiMainLayout)
        self.uiFrame.setVisible(False)
        self._generate_header_layout()
        self._generate_covered_list_layout()
        self._generate_not_covered_list_layout()
        self._generate_ignore_list_layout()
        self._connect_signals()

    def show_coverage_layout(self, show):
        for widget in (
            self.uiListWidgetCoveredList,
            self.uiListWidgetNotCoveredList,
            self.uiListWidgetIgnoreList,
            self.uiLabelCovered,
            self.uiLabelNotCovered,
            self.uiLabelIgnored,
        ):
            widget.setVisible(show)

    def provide_layout(self):
        return self.uiFrame

    def fill_with_data(self, node):
        self.uiFrame.setVisible(True)
        self._fill_header_layout(node)
        self._fill_covered_list_layout(node)
        self._fill_not_covered_list_layout(node)
        self._fill_ignore_list_layout(node)
        self.show_coverage_layout(bool(node.coverage_filter))

    def _connect_signals(self):
        for list_widget in (
            self.uiListWidgetIgnoreList,
            self.uiListWidgetNotCoveredList,
            self.uiListWidgetCoveredList,
        ):
            list_widget.itemClicked.connect(
                self.DATA_MANAGER._doubleclick_on_identifier
            )

    def _generate_header_layout(self):
        self.uiLineEditModulePath = generate_one_row(
            'Path:',
            self.uiMainLayout,
            extend_label_width=True,
        )
        self.uiLineEditTimestamp = generate_one_row(
            'Updated:',
            self.uiMainLayout,
            extend_label_width=True,
        )

    def _fill_header_layout(self, node):
        self.uiLineEditModulePath.setText(node.path)
        self.uiLineEditTimestamp.setText(node.timestamp)

    def _generate_covered_list_layout(self):
        self.uiAllListLayout = QHBoxLayout()
        self.uiMainLayout.addLayout(self.uiAllListLayout)
        self.uiListWidgetCoveredList, self.uiLabelCovered = (
            self._create_list_column(
                'QLabel {color: rgb(0, 179, 0); min-width: 120px}'
            )
        )

    def _fill_covered_list_layout(self, node):
        self.uiLabelCovered.setText(
            f'Covered: {len(node.covered_requirements)}'
        )
        self.uiListWidgetCoveredList.clear()
        for identifier in node.covered_requirements:
            item = QListWidgetItem(self.uiListWidgetCoveredList)
            item.setData(Qt.DisplayRole, identifier.split('-')[-1])
            if len(node.coverage_dict) < 500:
                item.setData(
                    Qt.DecorationRole,
                    self.DATA_MANAGER.MAIN.ICON_MANAGER.ICON_REQUIREMENT_COVERED,
                )
            item.setData(Qt.UserRole, identifier)

    def _generate_not_covered_list_layout(self):
        self.uiListWidgetNotCoveredList, self.uiLabelNotCovered = (
            self._create_list_column(
                'QLabel {color: rgb(250,50,50); min-width: 120px}'
            )
        )

    def _fill_not_covered_list_layout(self, node):
        self.uiLabelNotCovered.setText(
            f'Not Covered: {len(node.not_covered_requirements)}'
        )
        self.uiListWidgetNotCoveredList.clear()
        for identifier in node.not_covered_requirements:
            item = QListWidgetItem(self.uiListWidgetNotCoveredList)
            item.setData(Qt.DisplayRole, identifier.split('-')[-1])
            if len(node.coverage_dict) < 500:
                item.setData(
                    Qt.DecorationRole,
                    self.DATA_MANAGER.MAIN.ICON_MANAGER.ICON_REQUIREMENT_NOT_COVERED,
                )
            item.setData(Qt.UserRole, identifier)

    def _generate_ignore_list_layout(self):
        self.uiListWidgetIgnoreList, self.uiLabelIgnored = (
            self._create_list_column('QLabel {min-width: 120px}')
        )

    def _fill_ignore_list_layout(self, node):
        self.uiLabelIgnored.setText(f'Ignored: {len(node.ignore_list)}')
        self.uiListWidgetIgnoreList.clear()
        for identifier in node.ignore_list:
            item = QListWidgetItem()
            item.setData(Qt.DisplayRole, identifier.split('-')[-1])
            item.setData(Qt.UserRole, identifier)
            item.setData(
                Qt.DecorationRole,
                self.DATA_MANAGER.MAIN.ICON_MANAGER.ICON_REQUIREMENT_IGNORED,
            )
            self.uiListWidgetIgnoreList.insertItem(0, item)

    def _create_list_column(self, label_style):
        layout = QVBoxLayout()
        label = QLabel()
        label.setStyleSheet(label_style)
        list_widget = ListWidgetPointingHand()
        list_widget.setMouseTracking(True)
        list_widget.itemEntered.connect(
            self.DATA_MANAGER.set_tooltip_2_list_widget_item
        )
        layout.addWidget(label)
        layout.addWidget(list_widget)
        self.uiAllListLayout.addLayout(layout)
        return list_widget, label
