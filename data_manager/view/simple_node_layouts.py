from PyQt5.QtWidgets import QFrame, QVBoxLayout

from components.helper_functions import (
    layout_generate_one_row as generate_one_row,
)
from data_manager.view.layout_base import LayoutGenerator


class SimpleNodeLayoutGenerator(LayoutGenerator):
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(20)
        self.frame = QFrame()
        self.frame.setLayout(self.main_layout)
        self.frame.setVisible(False)

    def provide_layout(self):
        return self.frame

    def fill_with_data(self, node):
        self.frame.setVisible(True)


class FileNodeLayoutGenerator(SimpleNodeLayoutGenerator):
    def __init__(self, data_manager):
        super().__init__(data_manager)
        self.file_path = generate_one_row(
            'Path:',
            self.main_layout,
            set_read_only=True,
        )

    def fill_with_data(self, node):
        super().fill_with_data(node)
        self.file_path.setText(node.path)


class A2lNodeLayoutGenerator(SimpleNodeLayoutGenerator):
    def __init__(self, data_manager):
        super().__init__(data_manager)
        self.name = generate_one_row(
            'Name:',
            self.main_layout,
            set_read_only=True,
        )
        self.address = generate_one_row(
            'Address:',
            self.main_layout,
            set_read_only=True,
        )

    def fill_with_data(self, node):
        super().fill_with_data(node)
        self.name.setText(node.name)
        self.address.setText(node.address)


class ConditionValueNodeLayoutGenerator(SimpleNodeLayoutGenerator):
    def __init__(self, data_manager):
        super().__init__(data_manager)
        self.name = generate_one_row(
            'Name:',
            self.main_layout,
            set_read_only=True,
        )
        self.category = generate_one_row(
            'Category:',
            self.main_layout,
            set_read_only=True,
        )

    def fill_with_data(self, node):
        super().fill_with_data(node)
        self.name.setText(node.name)
        self.category.setText(node.category)


class TestStepNodeLayoutGenerator(SimpleNodeLayoutGenerator):
    def __init__(self, data_manager):
        super().__init__(data_manager)
        self.name = generate_one_row(
            'Name:',
            self.main_layout,
            set_read_only=True,
        )
        self.action = generate_one_row(
            'Action:',
            self.main_layout,
            set_read_only=True,
        )
        self.comment = generate_one_row(
            'Comment:',
            self.main_layout,
            set_read_only=True,
        )
        self.nominal = generate_one_row(
            'Nominal:',
            self.main_layout,
            set_read_only=True,
        )

    def fill_with_data(self, node):
        super().fill_with_data(node)
        self.name.setText(node.name)
        self.action.setText(node.action)
        self.comment.setText(node.comment)
        self.nominal.setText(node.nominal)


class DspaceDefinitionNodeLayoutGenerator(SimpleNodeLayoutGenerator):
    def __init__(self, data_manager):
        super().__init__(data_manager)
        self.name = generate_one_row(
            'Name:',
            self.main_layout,
            set_read_only=True,
        )

    def fill_with_data(self, node):
        super().fill_with_data(node)
        self.name.setText(node.name)


class DspaceVariableNodeLayoutGenerator(SimpleNodeLayoutGenerator):
    def __init__(self, data_manager):
        super().__init__(data_manager)
        self.name = generate_one_row(
            'Name:',
            self.main_layout,
            set_read_only=True,
        )
        self.value = generate_one_row(
            'Value:',
            self.main_layout,
            set_read_only=True,
        )
        self.path = generate_one_row(
            'Path:',
            self.main_layout,
            set_read_only=True,
        )

    def fill_with_data(self, node):
        super().fill_with_data(node)
        self.name.setText(node.name)
        self.value.setText(node.value)
        self.path.setText(node.path)
