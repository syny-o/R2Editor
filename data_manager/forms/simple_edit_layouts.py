from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QTextEdit, QVBoxLayout

from components.helper_functions import (
    layout_generate_one_row as generate_one_row,
    validate_line_edits,
)


class SimpleEditLayout:
    def __init__(self, node):
        self.NODE = node
        self.uiMainLayout = QVBoxLayout()
        self.uiMainLayout.setContentsMargins(50, 50, 50, 50)
        self.uiMainLayout.setSpacing(10)

    def provide_layout(self):
        self._create_layout()
        return self.uiMainLayout

    def _focus_name(self):
        QTimer.singleShot(100, self.uiLineEditName.setFocus)
        QTimer.singleShot(120, self.uiLineEditName.selectAll)


class ConditionAndValueNodeLayoutGenerator(SimpleEditLayout):
    def _create_layout(self):
        self.uiLineEditName = generate_one_row(
            'Name:',
            self.uiMainLayout,
        )
        self.uiLineEditName.setText(self.NODE.name)
        self.uiLineEditCategory = generate_one_row(
            'Category:',
            self.uiMainLayout,
        )
        self.uiLineEditCategory.setText(self.NODE.category)
        self._focus_name()

    def update_data(self):
        if validate_line_edits(
            self.uiLineEditName,
            self.uiLineEditCategory,
        ):
            self.NODE.name = self.uiLineEditName.text()
            self.NODE.category = self.uiLineEditCategory.text()
            self.NODE.get_file_node().set_modified(True)
            return True


class TestStepNodeLayoutGenerator(SimpleEditLayout):
    def _create_layout(self):
        self.uiLineEditName = generate_one_row(
            'Name:',
            self.uiMainLayout,
        )
        self.uiLineEditName.setText(self.NODE.name)
        self.uiLineEditAction = generate_one_row(
            'Action:',
            self.uiMainLayout,
        )
        self.uiLineEditAction.setText(self.NODE.action)
        self.uiLineEditComment = generate_one_row(
            'Comment:',
            self.uiMainLayout,
        )
        self.uiLineEditComment.setText(self.NODE.comment)
        self.uiLineEditNominal = generate_one_row(
            'Nominal:',
            self.uiMainLayout,
        )
        self.uiLineEditNominal.setText(self.NODE.nominal)
        self._focus_name()

    def update_data(self):
        if validate_line_edits(self.uiLineEditAction):
            self.NODE.name = self.uiLineEditName.text()
            self.NODE.action = self.uiLineEditAction.text()
            self.NODE.comment = self.uiLineEditComment.text()
            self.NODE.nominal = self.uiLineEditNominal.text()
            self.NODE.get_file_node().set_modified(True)
            return True


class DspaceVariableNodeLayoutGenerator(SimpleEditLayout):
    def _create_layout(self):
        self.uiLineEditName = generate_one_row(
            'Name:',
            self.uiMainLayout,
        )
        self.uiLineEditName.setText(self.NODE.name)
        self.uiLineEditValue = generate_one_row(
            'Value:',
            self.uiMainLayout,
        )
        self.uiLineEditValue.setText(self.NODE.value)
        self.uiLineEditPath = generate_one_row(
            'Path:',
            self.uiMainLayout,
        )
        self.uiLineEditPath.setText(self.NODE.path)
        self._focus_name()

    def update_data(self):
        if validate_line_edits(
            self.uiLineEditName,
            self.uiLineEditPath,
            self.uiLineEditValue,
        ):
            self.NODE.name = self.uiLineEditName.text()
            self.NODE.value = self.uiLineEditValue.text()
            self.NODE.path = self.uiLineEditPath.text()
            self.NODE.get_file_node().set_modified(True)
            return True


class RequirementNodeLayoutGenerator:
    def __init__(self, node):
        self.NODE = node
        self.uiMainLayout = QVBoxLayout()
        self.uiMainLayout.setContentsMargins(50, 50, 50, 50)
        self.uiMainLayout.setSpacing(10)

    def provide_layout(self):
        layout = QHBoxLayout()
        self.uiTextEditNote = QTextEdit(self.NODE.note)
        layout.addWidget(QLabel('Note:    '))
        layout.addWidget(self.uiTextEditNote)
        self.uiMainLayout.addLayout(layout)
        QTimer.singleShot(100, self.uiTextEditNote.setFocus)
        return self.uiMainLayout

    def update_data(self):
        self.NODE.note = self.uiTextEditNote.toPlainText()
        return True
