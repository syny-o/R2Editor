# from PyQt5.Qt import QStandardItem
from PyQt5.QtGui import QStandardItem, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyle, QPushButton
import re
from dialogs.dialog_message import dialog_message
from components.reduce_path_string import reduce_path_string


def initialise(data: dict, root_node):
    paths = data.get('Conditions Files')
    if paths:
        [ConditionFileNode(root_node, path) for path in paths]


class ConditionFileNode(QStandardItem):
    def __init__(self, root_node, path):
        super().__init__()
        self.root_node = root_node
        self.data_manager = self.root_node.data(Qt.UserRole)
        
        self.path = path
        self.header = ''

        self.setText(reduce_path_string(self.path))

        self.setIcon(QIcon(u"ui/icons/xml.png"))
        

        self.setEditable(False)

        self.file_2_tree()



    def set_modified(self, modified):
        if modified:
            self.setIcon(QIcon(u"ui/icons/modified_file.png"))
        else:
            self.setIcon(QIcon(u"ui/icons/xml.png"))



    def file_2_tree(self):
        try:
            with open(self.path, 'r') as f:
                cond_file_string = f.read()
            cond_sections = re.split('<Condition ', cond_file_string)
            self.header = cond_sections.pop(0)

            ####### CONDITIONS #######
            for cs in cond_sections:
                c_key_match = re.search(r'Name\s*=\s*"([^"]+)', cs)
                c_category_match = re.search(r'Type\s*=\s*"([^"]+)', cs)
                c_key = c_key_match.group(1)  # COND NAME
                c_category = c_category_match.group(1)  # COND TYPE

                # node management
                c_node = ConditionNode(c_key, c_category)
                self.appendRow(c_node)  # APPEND NODE AS A CHILD

                ####### VALUES #######
                value_sections = re.split('<Value ', cs)

                for vs in value_sections[1:]:
                    v_key_match = re.search(r'Name\s*=\s*"([^"]+)', vs)
                    v_category_match = re.search(r'Type\s*=\s*"([^"]+)', vs)
                    v_key = v_key_match.group(1)  # VALUE NAME
                    v_category = v_category_match.group(1)  # VALUE TYPE

                    # node management
                    v_node = ValueNode(v_key, v_category)
                    c_node.appendRow(v_node)  # APPEND NODE AS A CHILD

                    ####### TEST STEPS #######
                    ts_sections = re.split('TS', vs)
                    for ts in ts_sections[1:]:
                        ts_name = re.search(r'Name=\s*"([^"]+)', ts)
                        ts_action = re.search(r'A\s*=\s*"([^"]+)', ts)
                        ts_nominal = re.search(r'Nominal\s*=\s*"([^"]+)', ts)
                        ts_comment = re.search(r'Comment\s*=\s*"([^"]+)', ts)

                        ts_name = ts_name.group(1) if ts_name else ''  # TS NAME
                        ts_action = ts_action.group(1) if ts_action else ''  # TS ACTION
                        ts_nominal = ts_nominal.group(1) if ts_nominal else ''  # TS NOMINAL
                        ts_comment = ts_comment.group(1) if ts_comment else ''  # TS COMMENT

                        # node management
                        ts_node = TestStepNode(ts_name, ts_action, ts_comment, ts_nominal)
                        v_node.appendRow(ts_node)  # APPEND NODE AS A CHILD

            self.root_node.appendRow(self)  # APPEND NODE AS A CHILD

        except Exception as e:
            print(f'Unable to open file {self.path}, reason: {str(e)}')






    def tree_2_file(self):
        output_text = ''
        output_text += self.header
        for condition_row in range(self.rowCount()):
            # Condition Level
            current_condition = self.child(condition_row, 0)
            output_text += f'\t<Condition Name="{current_condition.name}" Type="{current_condition.category}">\n'
            for value_row in range(current_condition.rowCount()):
                # Value Level
                current_value = current_condition.child(value_row, 0)
                output_text += f'\t\t<Value Name="{current_value.name}" Type="{current_value.category}">\n'
                for test_step_row in range(current_value.rowCount()):
                    # Test Step Level
                    current_test_step = current_value.child(test_step_row, 0)
                    output_text += f'\t\t\t<TS Name="{current_test_step.name}" A="{current_test_step.action}" Nominal="{current_test_step.nominal}" Comment="{current_test_step.comment}" />\n'
                output_text += '\t\t</Value>\n'
            output_text += '\t</Condition>\n'
        output_text += '</Conditions>'

        try:
            with open(self.path, 'w', encoding='utf8') as f:
                f.write(output_text)

            self.set_modified(False)

        except Exception as e:
            print(str(e))
            dialog_message(self.data_manager, str(e))     
            
                

        



    def data_4_completer(self):
        """

        COMMAND PATTERN
        create data of all conditions/values for auto-complete in text_editor

        :return:    cond_dict -->   keys = conditions names,
                                    values = QStandardItemModel where each QStandardItem represents value

                    cond_model -->   QStandardItemModel where each item represents condition

        """

        condition_dict = {}
        condition_list = []
        for ci in range(self.rowCount()):  # iterate through all condition nodes

            cond_node = self.child(ci)  # get copy of object on <ci=cond index> row
            new_cond_node = cond_node.clone()

            #  set DATA to QStandardItem


            new_cond_node.setData(str(f'{cond_node.text() : <40}{self.path : >40}'), Qt.DisplayRole)
            new_cond_node.setData(cond_node.text(), Qt.ToolTipRole)

            condition_list.append(new_cond_node)  # add QStandardItem to List

            values_list = []  # init values model

            for vi in range(cond_node.rowCount()):
                # print(cond_node.text() + " ::: ")
                value_node = cond_node.child(vi)

                new_value_node = value_node.clone()

                #  set DATA to QStandardItem

                # TEST
                test_steps_string = "".join([value_node.child(ti).text() for ti in range(value_node.rowCount())])
                if len(test_steps_string) > 60:
                    test_steps_string = test_steps_string[:60] + "..."
                else:
                    test_steps_string = test_steps_string + (" " * (60-len(test_steps_string)))
            
                #TEST END
                new_value_node.setData(str(f'{value_node.text() : <40}{test_steps_string : >40}'), Qt.DisplayRole)
                new_value_node.setData(value_node.text(), Qt.ToolTipRole)

                values_list.append(new_value_node)  # add QStandardItem to model

            condition_dict.update({cond_node.text(): values_list})


        # TEST TOOLTIPS INCLUDE TEST STEPS
        cond_tooltips = {}
        for ci in range(self.rowCount()):
            cond_node = self.child(ci)
            cond_name = cond_node.text()
            values = {}
            for vi in range(cond_node.rowCount()):
                value_node = cond_node.child(vi)
                value_name = value_node.text()
                test_steps = []
                for ti in range(value_node.rowCount()):
                    test_step = value_node.child(ti)
                    test_steps.append(test_step.text())
                values.update({value_node.text(): test_steps})
            cond_tooltips.update({cond_node.text(): values})
            
        # print(cond_tooltips["PRE"])


        return condition_dict, condition_list, cond_tooltips



    def data_4_project(self, data):
        cond_list = data.get('Conditions Files')
        cond_list.append(self.path)
        data.update(
            {'Conditions Files': cond_list}
        )
        return data






class ConditionNode(QStandardItem):
    def __init__(self, name, category):
        super().__init__()
        self.name = name
        self.category = category

        self.setText(name)

        self.setEditable(False)

        self.setIcon(QIcon(u"ui/icons/condition.png"))

    def get_file_node(self):
        return self.parent()

    def get_node_copy(self):
        # create list of children --> ValueNode objects
        my_val_nodes = [self.child(row) for row in range(self.rowCount())]
        # create copies of all children
        new_val_nodes = [val_node.get_node_copy() for val_node in my_val_nodes]
        new_cond_node = ConditionNode(self.name, self.category)
        new_cond_node.appendRows(new_val_nodes)
        return new_cond_node        



class ValueNode(QStandardItem):
    def __init__(self, name, category):
        super().__init__()
        self.name = name
        self.category = category

        self.setText(name)

        self.setEditable(False)

        self.setIcon(QIcon(u"ui/icons/value.png"))

    def get_file_node(self):
        return self.parent().parent()

    @property
    def my_test_step_nodes(self):
        return [self.child(row) for row in range(self.rowCount())]

    def get_node_copy(self):
        new_ts_nodes = [ts_node.get_node_copy() for ts_node in self.my_test_step_nodes]
        new_value_node = ValueNode(self.name, self.category)
        new_value_node.appendRows(new_ts_nodes)
        return new_value_node


class TestStepNode(QStandardItem):
    def __init__(self, name, action, comment, nominal):
        super().__init__()
        self.name = name
        self.action = action
        self.comment = comment
        self.nominal = nominal

        self.setText(action)

        self.setEditable(False)

        self.setIcon(QIcon(u"ui/icons/ts.png"))

    def get_file_node(self):
        return self.parent().parent().parent()

    def get_node_copy(self):
        return TestStepNode(self.name, self.action, self.comment, self.nominal)






