from cgi import test
from hmac import new
import os, stat, re

from PyQt5.QtGui import QStandardItem, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from data_manager.nodes.condition_node import ConditionNode
from data_manager.nodes.value_node import ValueNode
from data_manager.nodes.test_step_node import TestStepNode
from components.reduce_path_string import reduce_path_string
from utils.text.func_format import rstrip_and_add_dots




def initialise(data: dict, root_node):
    paths = data.get('Conditions Files')
    if paths:
        [ConditionFileNode(root_node, path) for path in paths]




def extract_data(pattern, text, default=''):
    match = re.search(pattern, text)
    return match.group(1) if match else default

def create_node(section, node_class, parent_node):
    key = extract_data(r'Name\s*=\s*"([^"]+)', section)
    category = extract_data(r'Type\s*=\s*"([^"]+)', section)
    node = node_class(key, category)
    parent_node.appendRow(node)
    return node

def process_test_steps(value_section, value_node):
    test_step_sections = re.split('TS', value_section)
    for test_step_section in test_step_sections[1:]:
        ts_name = extract_data(r'Name=\s*"([^"]+)', test_step_section)
        ts_action = extract_data(r'A\s*=\s*"([^"]+)', test_step_section)
        ts_nominal = extract_data(r'Nominal\s*=\s*"([^"]+)', test_step_section)
        ts_comment = extract_data(r'Comment\s*=\s*"([^"]+)', test_step_section)

        test_step_node = TestStepNode(ts_name, ts_action, ts_comment, ts_nominal)
        value_node.appendRow(test_step_node)

def process_values(condition_section, condition_node):
    value_sections = re.split('<Value ', condition_section)
    for value_section in value_sections[1:]:
        value_node = create_node(value_section, ValueNode, condition_node)
        process_test_steps(value_section, value_node)







class ConditionFileNode(QStandardItem):
    def __init__(self, root_node, path):
        super().__init__()
        
        self.ROOT = root_node
        self.DATA_MANAGER = self.ROOT.data(Qt.UserRole)
        
        self.path = path
        
        self.setText(reduce_path_string(self.path))
        self.setIcon(QIcon(u"ui/icons/xml.png"))
        self.setEditable(False)
                
        self.header = ''
        self.is_modified = False

        self.file_2_tree()
        



    def set_modified(self, modified):
        self.is_modified = modified
        icon_path = "ui/icons/modified_file.png" if modified else "ui/icons/xml.png"
        self.setIcon(QIcon(icon_path))



    def file_2_tree(self):
        try:
            with open(self.path, 'r') as f:
                file_content = f.read()

            condition_sections = re.split('<Condition ', file_content)
            self.header = condition_sections.pop(0)

            for condition_section in condition_sections:
                condition_node = create_node(condition_section, ConditionNode, self)
                process_values(condition_section, condition_node)

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
        output_lines = [self.header]

        for condition_row in range(self.rowCount()):
            condition = self.child(condition_row, 0)
            output_lines.append(f'\t<Condition Name="{condition.name}" Type="{condition.category}">')

            for value_row in range(condition.rowCount()):
                value = condition.child(value_row, 0)
                output_lines.append(f'\t\t<Value Name="{value.name}" Type="{value.category}">')

                for test_step_row in range(value.rowCount()):
                    test_step = value.child(test_step_row, 0)
                    output_lines.append(f'\t\t\t<TS Name="{test_step.name}" A="{test_step.action}" Nominal="{test_step.nominal}" Comment="{test_step.comment}" />')

                output_lines.append('\t\t</Value>')

            output_lines.append('\t</Condition>')

        output_lines.append('</Conditions>')

        return '\n'.join(output_lines)
    

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
        # test_steps_string = " ".join([value_node.child(ti).text() for ti in range(value_node.rowCount())])
        test_step_list = [value_node.child(ti).text() for ti in range(value_node.rowCount())]        
        # new_value_node.setData(str(f'{value_node.text() : <40}{rstrip_and_add_dots(test_steps_string, 50) : >50}'), Qt.DisplayRole)
        new_value_node.setData(test_step_list, Qt.UserRole)

        return new_value_node

    def create_condition_tooltip_4_completer(self, cond_node):
        values = {}
        for vi in range(cond_node.rowCount()):
            value_node = cond_node.child(vi)
            test_steps = [value_node.child(ti).text() for ti in range(value_node.rowCount())]
            values.update({value_node.text(): test_steps})
        return {cond_node.text(): values}

    def data_4_completer(self):
        cond_dict = {}
        cond_list = []
        cond_tooltips = {}

        for ci in range(self.rowCount()):
            cond_node = self.child(ci)
            new_cond_node = self.create_node_4_completer(cond_node)
            cond_list.append(new_cond_node)

            values_list = []
            for vi in range(cond_node.rowCount()):
                value_node = cond_node.child(vi)
                new_value_node = self.create_value_node_4_completer(value_node)
                values_list.append(new_value_node)

            # new_cond_node.setData(str(f'{cond_node.text() : <40}{" | ".join([v.data(Qt.ToolTipRole) for v in values_list])[:100] : >100}'), Qt.DisplayRole)
            new_cond_node.setData([value.text() for value in values_list], Qt.UserRole)
            cond_dict.update({cond_node.text(): values_list})

            cond_tooltips.update(self.create_condition_tooltip_4_completer(cond_node))

        return cond_dict, cond_list, cond_tooltips


    # def data_4_completer(self) -> dict:
    #     cond_dict = {}
    #     for ci in range(self.rowCount()):
    #         cond_node = self.child(ci)
    #         cond_key = cond_node.text()
    #         values = {}
    #         for vi in range(cond_node.rowCount()):
    #             value_node = cond_node.child(vi)
    #             value_key = value_node.text()
    #             test_steps = [value_node.child(ti).text() for ti in range(value_node.rowCount())]
    #             values.update({value_key: test_steps})
        
    #         cond_dict.update({cond_key: values})

    #     return cond_dict









