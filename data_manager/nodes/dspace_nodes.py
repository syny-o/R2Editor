import os, stat
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from config.icon_manager import IconManager
from components.reduce_path_string import reduce_path_string
from data_manager.dspace_mapping import (
    parse_dspace_mapping,
    serialize_dspace_mapping,
)


def initialise(data: dict, root_node):
    paths = data.get('DSpace Files')
    if paths:
        [DspaceFileNode(root_node, path) for path in paths]


class DspaceFileNode(QStandardItem):
    def __init__(self, root_node, path):
        super().__init__()
        self.root_node = root_node
        self.data_manager = self.root_node.data(Qt.UserRole)
        self.path = path
        self.header = ''
        self.footer = ''

        self.setText(reduce_path_string(self.path))

        self.setIcon(IconManager.data_icon("dspace_file"))

        self.setEditable(False)

        self.file_2_tree()

        self.is_modified = False


    def set_modified(self, modified):
        self.is_modified = modified
        icon = (
            IconManager.data_icon("modified_file")
            if modified
            else IconManager.data_icon("dspace_file")
        )
        self.setIcon(icon)


    def file_2_tree(self):
        try:
            with open(self.path, 'r', encoding='utf8') as f:
                dspace_file_string = f.read()

            self.header, self.footer, definitions = parse_dspace_mapping(
                dspace_file_string
            )

            for definition_name, variables in definitions:
                definition_node = DspaceDefinitionNode(definition_name)
                self.appendRow(definition_node) # APPEND NODE AS A CHILD
                for variable_name, value, path in variables:
                    definition_node.appendRow(
                        DspaceVariableNode(variable_name, value, path)
                    )

            self.root_node.appendRow(self)  # APPEND NODE AS A CHILD

        except Exception as e:
            print(f'Unable to open file {self.path}, reason: {str(e)}')



    def tree_2_file(self):
        definitions = []
        for definition_row in range(self.rowCount()):
            current_definition = self.child(definition_row, 0)
            variables = []
            for variable_row in range(current_definition.rowCount()):
                current_variable = current_definition.child(variable_row, 0)
                variables.append(
                    (
                        current_variable.name,
                        current_variable.value,
                        current_variable.path,
                    )
                )
            definitions.append((current_definition.name, variables))

        output_text = serialize_dspace_mapping(
            self.header,
            self.footer,
            definitions,
        )

        try:
            # Check if the file ReadOnly and if so, unlock it:
            is_read_only = not(os.access(self.path, os.W_OK))
            if is_read_only:
                os.chmod(self.path, stat.S_IWRITE)             
            with open(self.path, 'w', encoding='utf8') as f:
                f.write(output_text)
            self.set_modified(False)
        except Exception as e:
            raise Exception(f'Unable to save file {self.path}, reason: {str(e)}') 



    def data_4_project(self, data):
        ds_list = data.get('DSpace Files')
        ds_list.append(self.path)
        data.update(
            {'DSpace Files': ds_list}
        )
        return data



    def data_4_completer(self):
        """

        COMMAND PATTERN
        create data of all pbc variables for auto-complete in text_editor

        :return:    updated data dict with list of pbc variables

        """
        dspace_model = QStandardItemModel()

        for i in range(self.rowCount()):  # iterate through all a2l variables

            dspace_definition = self.child(i)  # get object on <i=index> row = QStandardItem

            for j in range(dspace_definition.rowCount()):

                dspace_variable = dspace_definition.child(j)

                if len(dspace_variable.name) < 25:
                    new_dspace_variable = dspace_variable.clone()

                    # new_dspace_variable.setData(str(f'{dspace_variable.name : <40}{dspace_definition.text() : >40}'), Qt.DisplayRole)

                    new_dspace_variable.setData(dspace_variable.name, Qt.ToolTipRole)
                    new_dspace_variable.setData(dspace_variable.name, Qt.DisplayRole)
                    new_dspace_variable.setData([dspace_variable.path,], Qt.UserRole)

                    dspace_model.appendRow(new_dspace_variable)

        return dspace_model  # Return Updated Data



class DspaceDefinitionNode(QStandardItem):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.setText(name)

        self.setEditable(False)

    def get_file_node(self) -> DspaceFileNode:
        return self.parent()        


class DspaceVariableNode(QStandardItem):
    def __init__(self, name, value, path):
        super().__init__()
        self.setEditable(False)        
        
        self.name = name
        self.value = value
        self.path = path

    
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name
        self.setText(name)


    def get_file_node(self) -> DspaceFileNode:
        return self.parent().parent()

        
    def get_node_copy(self):
        return DspaceVariableNode(self.name, self.value, self.path)






