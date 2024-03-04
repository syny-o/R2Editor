import os, stat
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QStandardItem, QStandardItemModel
import re
from dialogs.dialog_message import dialog_message
from components.reduce_path_string import reduce_path_string

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

        self.setIcon(QIcon(u"ui/icons/python.png"))

        self.setEditable(False)

        self.file_2_tree()

        self.is_modified = False


    def set_modified(self, modified):
        self.is_modified = modified
        if modified:
            self.setIcon(QIcon(u"ui/icons/modified_file.png"))
        else:
            self.setIcon(QIcon(u"ui/icons/python.png"))        


    def file_2_tree(self):
        try:
            with open(self.path, 'r') as f:
                dspace_file_string = f.read()

            ds_definitions = re.split(r'def ', dspace_file_string)

            # save first and last part for later export
            self.header = ds_definitions[0]
            self.footer = ds_definitions[-1]

            for definition in ds_definitions[1:-1]:  # start from second item and stop before last one
                ds_var = re.split(r'append', definition)
                # EXTRACT DEFINITION
                current_definition = re.split(r'\(', ds_var[0])[0].strip()
                definition_node = DspaceDefinitionNode(current_definition)
                self.appendRow(definition_node) # APPEND NODE AS A CHILD
                for v in ds_var[1:]:
                    try:
                        all_variables = re.split('"', v)
                        v_name = all_variables[1],  # name
                        v_value = all_variables[2].strip(', '),  # default value
                        v_path = all_variables[3],  # path
                        variable_node = DspaceVariableNode(v_name[0], v_value[0], v_path[0])
                        definition_node.appendRow(variable_node)  # APPEND NODE AS A CHILD
                    except Exception as e:
                        print('Error when loading DSpaceMapping.py: ' + str(e))
                        print(v_name)


            self.root_node.appendRow(self)  # APPEND NODE AS A CHILD

        except Exception as e:
            print(f'Unable to open file {self.path}, reason: {str(e)}')



    def tree_2_file(self):
        output_text = ''
        output_text += self.header
        for definition_row in range(self.rowCount()):
            # Definition Level
            current_definition = self.child(definition_row, 0)
            output_text += 'def ' + current_definition.name + '():\n'
            output_text += '\t' + current_definition.name + 'Var = []\n'

            for variable_row in range(current_definition.rowCount()):
                # Variable Level
                current_variable = current_definition.child(variable_row, 0)
                temp = current_variable.name + '"'
                output_text += '\t' + current_definition.name + 'Var.append(["' + f'{temp  : <70}' + ', ' + f'{current_variable.value : <5}' + ',"' + current_variable.path+ '"])\n'

            output_text += '\treturn ' + current_definition.name + 'Var\n'
            output_text += '\n'

        # APPEND FOOTER
        output_text += 'def '
        output_text += self.footer

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

                    new_dspace_variable.setData(str(f'{dspace_variable.name : <40}{dspace_definition.text() : >40}'), Qt.DisplayRole)

                    new_dspace_variable.setData(dspace_variable.name, Qt.ToolTipRole)

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






