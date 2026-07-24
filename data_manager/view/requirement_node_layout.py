import re

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor, QTextCharFormat, QTextCursor
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidgetItem,
    QTextEdit,
    QToolButton,
    QVBoxLayout,
)

from components.reduce_path_string import reduce_path_string
from components.widgets.widget_req_text_edit import RequirementTextEdit
from components.widgets.widgets_pointing_hand import ListWidgetPointingHand
from data_manager.view.layout_base import LayoutGenerator


class RequirementNodeLayoutGenerator(LayoutGenerator):
    def __init__(self, data_manager):
        self.DATA_MANAGER = data_manager
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

    def provide_layout(self):
        return self.uiFrame

    def fill_with_data(self, node):
        self._fill_header_layout(node)
        self._fill_data_layout(node)
        self._fill_links_layout(node)
        self._fill_scripts_layout(node)
        self._fill_note_layout(node)
        self._highlight_fulltext_filter_results(node)
        self.uiFrame.setVisible(True)

    def _connect_signals(self):
        self.uiListWidgetLinks.itemClicked.connect(
            self.DATA_MANAGER._doubleclick_on_outlink
        )
        self.uiListWidgetScripts.itemClicked.connect(
            self.DATA_MANAGER._doubleclick_on_tc_reference
        )

    def _generate_header_layout(self):
        layout = QHBoxLayout()
        self.uiLineEditIdentifier = QLineEdit()
        layout.addWidget(QLabel('Id:    '))
        layout.addWidget(self.uiLineEditIdentifier)
        self.action_copy_identifier = self.uiLineEditIdentifier.addAction(
            QIcon('ui/icons/20x20/cil-copy.png'),
            QLineEdit.LeadingPosition,
        )
        self.action_copy_identifier.triggered.connect(
            self._copy_to_clipboard
        )
        for widget in self.uiLineEditIdentifier.findChildren(QToolButton):
            widget.setCursor(Qt.PointingHandCursor)
        self.uiMainLayout.addLayout(layout)

    def _fill_header_layout(self, node):
        self.uiLineEditIdentifier.setText(node.reference)

    def _generate_data_layout(self):
        layout = QHBoxLayout()
        self.uiRequirementTextEdit = RequirementTextEdit(self.DATA_MANAGER)
        self.uiRequirementTextEdit.setReadOnly(True)
        layout.addWidget(QLabel('Data:'))
        layout.addWidget(self.uiRequirementTextEdit)
        self.uiMainLayout.addLayout(layout)

    def _fill_data_layout(self, node):
        text = ''
        for name, value in zip(
            node.MODULE.columns_names_backup,
            node.columns_data,
        ):
            text += f'<{name}>:\n{value} \n\n'
        self.uiRequirementTextEdit.set_text(text)

    def _generate_links_scripts_layout(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel('Links:'))
        self.uiListWidgetLinks = ListWidgetPointingHand()
        self.uiListWidgetLinks.setMaximumHeight(120)
        layout.addWidget(self.uiListWidgetLinks)
        layout.addWidget(QLabel('Scripts:'))
        self.uiListWidgetScripts = ListWidgetPointingHand()
        self.uiListWidgetScripts.setMaximumHeight(120)
        layout.addWidget(self.uiListWidgetScripts)
        self.uiMainLayout.addLayout(layout)

    def _fill_links_layout(self, node):
        self.uiListWidgetLinks.clear()
        for link, icon in (
            (outlink, self.DATA_MANAGER.MAIN.ICON_MANAGER.ICON_OUTLINK)
            for outlink in node.outlinks
        ):
            self._add_link_item(link, icon)
        for link, icon in (
            (inlink, self.DATA_MANAGER.MAIN.ICON_MANAGER.ICON_INLINK)
            for inlink in node.inlinks
        ):
            self._add_link_item(link, icon)

    def _add_link_item(self, link, icon):
        item = QListWidgetItem()
        item.setData(Qt.DisplayRole, reduce_path_string(link))
        item.setData(Qt.UserRole, link)
        item.setData(Qt.DecorationRole, icon)
        item.setData(
            Qt.ToolTipRole,
            self.DATA_MANAGER._get_tooltip_from_link(link),
        )
        self.uiListWidgetLinks.addItem(item)

    def _fill_scripts_layout(self, node):
        self.uiListWidgetScripts.clear()
        for file_reference in node.file_references:
            item = QListWidgetItem()
            item.setData(
                Qt.DisplayRole,
                reduce_path_string(file_reference),
            )
            item.setData(Qt.UserRole, file_reference)
            item.setIcon(
                self.DATA_MANAGER.MAIN.ICON_MANAGER.ICON_SCRIPT_REFERENCE
            )
            self.uiListWidgetScripts.addItem(item)

    def _generate_note_layout(self):
        layout = QHBoxLayout()
        self.uiTextEditNote = QTextEdit()
        self.uiTextEditNote.setMaximumHeight(50)
        self.uiTextEditNote.setReadOnly(True)
        layout.addWidget(QLabel('Note:'))
        layout.addWidget(self.uiTextEditNote)
        self.uiMainLayout.addLayout(layout)

    def _fill_note_layout(self, node):
        self.uiTextEditNote.setPlainText(node.note)

    def _highlight_fulltext_filter_results(self, node):
        filter_text = node.MODULE.data(Qt.UserRole)
        if not filter_text:
            return

        text = self.uiRequirementTextEdit.toPlainText()
        for match in re.finditer(filter_text, text, re.IGNORECASE):
            cursor = self.uiRequirementTextEdit.textCursor()
            cursor.setPosition(match.start())
            cursor.setPosition(match.end(), QTextCursor.KeepAnchor)
            text_format = QTextCharFormat()
            text_format.setBackground(QColor(0, 150, 0))
            cursor.setCharFormat(text_format)

    def _copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.clear(mode=clipboard.Clipboard)
        identifier = self.uiLineEditIdentifier.text()
        clipboard.setText(identifier, mode=clipboard.Clipboard)
        self.DATA_MANAGER.MAIN.show_notification(
            f'Item {identifier} copied to Clipboard.'
        )
