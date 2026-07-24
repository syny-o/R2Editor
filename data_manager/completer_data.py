from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel

from data_manager.nodes.a2l_nodes import A2lFileNode
from data_manager.nodes.condition_file import ConditionFileNode
from data_manager.nodes.dspace_nodes import DspaceFileNode
from text_editor.completer import Completer


def send_data_to_completer(root):
    condition_models = {}
    condition_model = QStandardItemModel()
    a2l_model = QStandardItemModel()
    dspace_model = QStandardItemModel()

    for root_row in range(root.rowCount()):
        file_node = root.child(root_row, 0)
        if isinstance(file_node, ConditionFileNode):
            condition_dict, condition_list = file_node.data_4_completer()

            for condition, values in condition_dict.items():
                if condition in condition_models:
                    continue

                values_model = QStandardItemModel()
                for value in values:
                    values_model.appendRow(value)
                condition_models[condition] = values_model

                for condition_item in condition_list:
                    if condition_item.data(role=Qt.DisplayRole) == condition:
                        condition_model.appendRow(condition_item)

        elif isinstance(file_node, A2lFileNode):
            for a2l_item in file_node.data_4_completer():
                a2l_model.appendRow(a2l_item)

        elif isinstance(file_node, DspaceFileNode):
            dspace_model = file_node.data_4_completer()

    Completer.cond_dict.clear()
    Completer.cond_model = QStandardItemModel()
    Completer.dspace_model = QStandardItemModel()

    if condition_models:
        Completer.cond_dict.update(condition_models)
        Completer.cond_model = condition_model

    if a2l_model:
        Completer.a2l_model = a2l_model

    if dspace_model:
        Completer.dspace_model = dspace_model
