from PyQt5.Qt import QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import re
from .pbc_patterns import patterns
from dialogs.dialog_message import dialog_message
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QSettings, QRunnable, QThreadPool
import time
from components.reduce_path_string import reduce_path_string


def initialise(data: dict, root_node):
    paths = data.get('A2L Files')
    if paths:
        [A2lFileNode(root_node, path) for path in paths]



def extract_measurements_from_file(file_path):
    measurements = []
    with open(file_path) as f:
        file_string = f.read()
    
    pattern = re.compile(r'(/begin MEASUREMENT|/begin CHARACTERISTIC)(.*?)(/end MEASUREMENT|end CHARACTERISTIC)',
                         flags=re.S)
    matches = pattern.finditer(file_string)
    for i in matches:
        measurements.append(i.group())
    return measurements


def normalise_text(text):
    for key, value in patterns.items():
        # find all matches for each variable
        pattern = key
        iteration = pattern.finditer(text)

        # check how many matches have been found (in current iteration)
        matches = pattern.findall(text)

        # if multiple matches (variable definitions) have been found:
        if len(matches) > 1:
            string_to_replace = None
            smallest_match_length = 1000
            for i in iteration:

                # check if one of the matches is in correct form (pattern value) --> no replacement needed
                if i.group(2) == value:
                    string_to_replace = None  # 2021-07-27 FIXED BUG (f.e. Saic AS28 M2M3 issue)
                    break

                # if all matches are in wrong form, choose shortest one and replace it with correct pattern value
                elif len(i.group(2)) < smallest_match_length:
                    smallest_match_length = len(i.group(2))
                    string_to_replace = i.group(2)
                    string_to_replace_start, string_to_replace_end = i.span(2)

            if string_to_replace:
                text = text[:string_to_replace_start] + value + text[string_to_replace_end:]

        # only one match at all has been found
        elif len(matches) == 1:
            for i in iteration:

                string_to_replace = i.group(2)
                string_to_replace_start, string_to_replace_end = i.span(2)

                if string_to_replace != value:
                    text = text[:string_to_replace_start] + value + text[string_to_replace_end:]

    return text       





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

        # self.setIcon(QIcon(u"ui/icons/16x16/cil-folder.png"))
        self.setIcon(QIcon(u"ui/icons/a2l.png"))

        self.setEditable(False)

        self.file_2_tree()

        # THREAD CONFIGURATION
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(1)



    def file_2_tree(self):
        try:
            measurements = extract_measurements_from_file(self.path)
      

            for m in measurements:
                signal_name_pattern = re.compile(r'(/begin MEASUREMENT|/begin CHARACTERISTIC)\s+([^/\s]+)', flags=re.S)
                signal_name_match = signal_name_pattern.search(m)
                signal_name = signal_name_match.group(2)
                # signal address
                match_address = re.search(r'(ECU_ADDRESS|VALUE)\s+(\w+)', m)
                signal_address = match_address.group(2) if match_address else 'Unknown'
                if any(item in signal_name.lower() for item in ["pbcin", "pbcout", "ssmpbin", "ssmpbout"]):
                    a2l_node = A2lNode(signal_name, signal_address)
                    self.appendRow(a2l_node)    # APPEND NODE AS A CHILD

            self.root_node.appendRow(self)  # APPEND NODE AS A CHILD

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

            new_a2l_node.setData(str(f'{a2l_node.name : <40}{self.path : >40}'), Qt.DisplayRole)

            # TODO: change it
            if self.instances < 2:
                new_a2l_node.setData(a2l_node.name, Qt.ToolTipRole)
            else:
                new_a2l_node.setData('Xpeng_E28A_Slave:' + a2l_node.name, Qt.ToolTipRole)

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
        worker = Worker(self)
        self.threadpool.start(worker)




        






class A2lNode(QStandardItem):
    def __init__(self, name, address):
        super().__init__()
        self.name = name
        self.address = address

        self.setText(name)

        self.setEditable(False)

        self.setIcon(QIcon(u"ui/icons/a2l.png"))




class Worker(QRunnable):

    def __init__(self, a2l_file_node):
        super().__init__()
        self.a2l_file_node = a2l_file_node

    @pyqtSlot()
    def run(self):
        print("Thread start - Normalising a2l file")
        self.a2l_file_node.data_manager.update_progress_status(True, "Normalising according to VDA spec...")
        try:
            with open(self.a2l_file_node.path, 'r') as f:
                a2l_file_string = f.read()
        except Exception as e:
            print(f'Unable to open file {self.a2l_file_node.path}, reason: {str(e)}')

        normalised_text = normalise_text(a2l_file_string)

        try:
            with open(self.a2l_file_node.path, 'w') as f:
                f.write(normalised_text)

                self.a2l_file_node.remove_all_children()
                self.a2l_file_node.file_2_tree()

                self.a2l_file_node.data_manager.update_progress_status(False)

        except Exception as e:
            print(f'Unable to save file {self.a2l_file_node.path}, reason: {str(e)}')
            dialog_message(self.a2l_file_node.data_manager, f'Unable to save file {self.a2l_file_node.path}, reason: {str(e)}')
            










