from PyQt5.Qt import QStandardItem
from PyQt5.QtCore import Qt, QThreadPool
from config.icon_manager import IconManager
from dialogs.dialog_message import dialog_message
from components.reduce_path_string import reduce_path_string
from data_manager.a2l.normalization_worker import A2lNormalizationWorker
from data_manager.a2l.parser import parse_supported_signals_from_file


def initialise(data: dict, root_node):
    paths = data.get('A2L Files')
    if paths:
        [A2lFileNode(root_node, path) for path in paths]

class A2lFileNode(QStandardItem):
    
    instances = 0
    def __init__(self, root_node, path):
        super().__init__()
        # TODO: change it
        A2lFileNode.instances += 1
        self.instances = A2lFileNode.instances

        

        self.root_node = root_node
        self.data_manager = self.root_node.data(Qt.UserRole)
        self.path = path
        


        
        
        self.setText(reduce_path_string(self.path))

        self.setIcon(IconManager.data_icon("a2l"))

        self.setEditable(False)

        self.file_2_tree()
        self.root_node.appendRow(self)  # APPEND NODE AS A CHILD

        # THREAD CONFIGURATION
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(1)



    def file_2_tree(self):
        try:
            signals = parse_supported_signals_from_file(self.path)
            for signal_name, signal_address in signals:
                self.appendRow(A2lNode(signal_name, signal_address))

        except Exception as e:
            print(f'Unable to open file {self.path}, reason: {str(e)}')
            dialog_message(self.data_manager, f'Unable to open file {self.path}, reason: {str(e)}')


    def tree_2_file(self):
        pass


    def remove_all_children(self):
        self.removeRows(0, self.rowCount())


    def data_4_completer(self):
        """

        COMMAND PATTERN
        create data of all pbc variables for auto-complete in text_editor

        :return:    updated data dict with list of pbc variables

        """
        a2l_list = []

        for i in range(self.rowCount()):  # iterate through all a2l variables

            a2l_node = self.child(i)  # get object on <i=index> row = QStandardItem

            new_a2l_node = a2l_node.clone()

            # new_a2l_node.setData(str(f'{a2l_node.name : <40}{self.path : >40}'), Qt.DisplayRole)

            new_a2l_node.setData(a2l_node.name, Qt.ToolTipRole)
            new_a2l_node.setData(a2l_node.name, Qt.DisplayRole)
            new_a2l_node.setData([a2l_node.address,], Qt.UserRole)


            if len(new_a2l_node.data(Qt.ToolTipRole)) < 45:
                a2l_list.append(new_a2l_node)  # add QStandardItem to List


        return a2l_list  # Return Updated Data


    def data_4_project(self, data):
        a2l_list = data.get('A2L Files')
        a2l_list.append(self.path)
        data.update(
            {'A2L Files': a2l_list}
        )
        return data

     


    def normalise_file(self):
        worker = A2lNormalizationWorker(self, self.data_manager)
        self.threadpool.start(worker)

class A2lNode(QStandardItem):
    def __init__(self, name, address):
        super().__init__()
        self.name = name
        self.address = address

        self.setText(name)

        self.setEditable(False)

        self.setIcon(IconManager.data_icon("a2l"))


