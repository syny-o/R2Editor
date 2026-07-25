import os, stat

from PyQt5.QtGui import QStandardItem
from PyQt5.QtCore import Qt

from config.icon_manager import IconManager
from data_manager.nodes.condition_node import ConditionNode
from data_manager.nodes.value_node import ValueNode
from data_manager.nodes.test_step_node import TestStepNode
from components.reduce_path_string import reduce_path_string
from data_manager.condition_file_format import (
    parse_condition_file,
    serialize_condition_file,
)




def initialise(data: dict, root_node):
    paths = data.get('Conditions Files')
    if paths:
        [ConditionFileNode(root_node, path) for path in paths]

class ConditionFileNode(QStandardItem):
    def __init__(self, root_node, path):
        super().__init__()
        
        self.ROOT = root_node
        self.DATA_MANAGER = self.ROOT.data(Qt.UserRole)
        
        self.path = path
        
        self.setText(reduce_path_string(self.path))
        self.setIcon(IconManager.data_icon("condition_file"))
        self.setEditable(False)
                
        self.header = ''
        self.is_modified = False

        self.file_2_tree()
        



    def set_modified(self, modified):
        self.is_modified = modified
        icon = (
            IconManager.data_icon("modified_file")
            if modified
            else IconManager.data_icon("condition_file")
        )
        self.setIcon(icon)



    def file_2_tree(self):
        try:
            with open(self.path, 'r', encoding='utf8') as f:
                file_content = f.read()

            self.header, conditions = parse_condition_file(file_content)
            for condition in conditions:
                condition_node = ConditionNode(
                    condition["name"],
                    condition["category"],
                )
                self.appendRow(condition_node)
                for value in condition["values"]:
                    value_node = ValueNode(
                        value["name"],
                        value["category"],
                    )
                    condition_node.appendRow(value_node)
                    for test_step in value["test_steps"]:
                        value_node.appendRow(
                            TestStepNode(
                                test_step["name"],
                                test_step["action"],
                                test_step["comment"],
                                test_step["nominal"],
                            )
                        )

            self.ROOT.appendRow(self)

        except Exception as e:
            print(f'Unable to open file {self.path}, reason: {str(e)}')





    def tree_2_file(self):
        try:
            # Check if the file is read-only and if so, unlock it:
            if not os.access(self.path, os.W_OK):
                os.chmod(self.path, stat.S_IWRITE)

            with open(self.path, 'w', encoding='utf8') as file:
                file.write(self.build_output_text())

            self.set_modified(False)

        except Exception as e:
            raise Exception(f'Unable to save file {self.path}, reason: {str(e)}')



    def build_output_text(self):
        conditions = []
        for condition_row in range(self.rowCount()):
            condition = self.child(condition_row, 0)
            condition_data = {
                "name": condition.name,
                "category": condition.category,
                "values": [],
            }
            for value_row in range(condition.rowCount()):
                value = condition.child(value_row, 0)
                value_data = {
                    "name": value.name,
                    "category": value.category,
                    "test_steps": [],
                }
                for test_step_row in range(value.rowCount()):
                    test_step = value.child(test_step_row, 0)
                    value_data["test_steps"].append(
                        {
                            "name": test_step.name,
                            "action": test_step.action,
                            "nominal": test_step.nominal,
                            "comment": test_step.comment,
                        }
                    )
                condition_data["values"].append(value_data)
            conditions.append(condition_data)

        return serialize_condition_file(self.header, conditions)
    

    def data_4_project(self, data):
        cond_list = data.get('Conditions Files')
        cond_list.append(self.path)
        data.update(
            {'Conditions Files': cond_list}
        )
        return data    
            
                

# COMPLETER CONFIGURATION


    def create_node_4_completer(self, node):
        new_node = node.clone()
        new_node.setData(node.text(), Qt.DisplayRole)
        return new_node

    def create_value_node_4_completer(self, value_node):
        new_value_node = self.create_node_4_completer(value_node)
        test_step_list = [value_node.child(ti).text() for ti in range(value_node.rowCount())]        
        new_value_node.setData(test_step_list, Qt.UserRole)
        new_value_node.setData(value_node.model().indexFromItem(value_node), Qt.UserRole + 1)

        return new_value_node

    def data_4_completer(self):
        cond_dict = {}
        cond_list = []

        for ci in range(self.rowCount()):
            cond_node = self.child(ci)
            new_cond_node = self.create_node_4_completer(cond_node)
            cond_list.append(new_cond_node)

            values_list = []
            for vi in range(cond_node.rowCount()):
                value_node = cond_node.child(vi)
                new_value_node = self.create_value_node_4_completer(value_node)
                values_list.append(new_value_node)

            new_cond_node.setData([value.text() for value in values_list], Qt.UserRole)
            new_cond_node.setData(cond_node.model().indexFromItem(cond_node), Qt.UserRole + 1)
            cond_dict.update({cond_node.text(): values_list})

        return cond_dict, cond_list
