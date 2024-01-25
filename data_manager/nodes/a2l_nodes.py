from PyQt5.Qt import QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import re, os, stat
from config.pbc_patterns import patterns, signals_to_check
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

            new_a2l_node.setData(a2l_node.name, Qt.ToolTipRole)


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
        worker = A2lNormWorker(self, self.data_manager)
        self.threadpool.start(worker)




        






class A2lNode(QStandardItem):
    def __init__(self, name, address):
        super().__init__()
        self.name = name
        self.address = address

        self.setText(name)

        self.setEditable(False)

        self.setIcon(QIcon(u"ui/icons/a2l.png"))















class A2lNormWorker(QRunnable):

    def __init__(self, a2l_file_node, data_manager):
        super().__init__()
        self.a2l_file_node = a2l_file_node
        self.signals = WorkerSignals()
        self.signals.status.connect(data_manager.update_progress_status)
        self.signals.finished.connect(data_manager.a2l_normalisation_finished) 

    
    def check_missing_signals(self, text):
        missing_signals = []
        for signal in signals_to_check:
            signal_to_check = text.find(signal)
            if signal_to_check == -1:
                if not contains_number(signal):
                    missing_signals.append(signal)
        return missing_signals





    def normalise_text(self, text):

        duplicated_signals = []
        total_counter = 0

        data_4_report = {}

        for key, value in patterns.items():
            # find all matches for each variable
            self.signals.status.emit(True, f"Checking: <{value}>")
            pattern = key
            iteration = pattern.finditer(text)

            # check how many matches have been found (in current iteration)
            matches = pattern.findall(text)

            # if multiple matches (variable definitions) have been found:
            if len(matches) > 1:

                if not contains_number(value):
                    duplicated_signals.append(value)

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
                    
                    # JUST INFORMATION FOR REPORT
                    total_counter += 1
                    # text_for_report += f" string_to_replace " + ' has been replaced with ' + value + '\n'
                    data_4_report.update({string_to_replace : value})

            # only one match at all has been found
            elif len(matches) == 1:
                for i in iteration:

                    string_to_replace = i.group(2)
                    string_to_replace_start, string_to_replace_end = i.span(2)

                    if string_to_replace != value:
                        text = text[:string_to_replace_start] + value + text[string_to_replace_end:]
                        
                        # JUST INFORMATION FOR REPORT                        
                        total_counter += 1
                        # text_for_report += string_to_replace + ' has been replaced with ' + value + '\n'
                        data_4_report.update({string_to_replace : value})
        

        return text, data_4_report, duplicated_signals                 
        



    @pyqtSlot()
    def run(self):
        self.signals.status.emit(True, "Normalising according to VDA spec...")
        try:
            with open(self.a2l_file_node.path, 'r') as f:
                a2l_file_string = f.read()
        except Exception as e:
            print(f'Unable to open file {self.a2l_file_node.path}, reason: {str(e)}')

        normalised_text, data_4_report, duplicated_signals = self.normalise_text(a2l_file_string)
        missing_signals = self.check_missing_signals(normalised_text)
        # self.signals.finished.emit(data_4_report, missing_signals, duplicated_signals)

        try:
            # Check if the file ReadOnly and if so, unlock it:
            is_read_only = not(os.access(self.a2l_file_node.path, os.W_OK))
            if is_read_only:
                os.chmod(self.a2l_file_node.path, stat.S_IWRITE)

            with open(self.a2l_file_node.path, 'w') as f:
                f.write(normalised_text)

                self.a2l_file_node.remove_all_children()
                self.a2l_file_node.file_2_tree()
                self.signals.finished.emit(data_4_report, missing_signals, duplicated_signals)


        except Exception as e:
            print(f'Unable to save file {self.a2l_file_node.path}, reason: {str(e)}')
            dialog_message(self.a2l_file_node.data_manager, f'Unable to save file {self.a2l_file_node.path}, reason: {str(e)}')

        finally:
            self.signals.status.emit(False, "")
            






class WorkerSignals(QObject):
    finished = pyqtSignal(dict, list, list)
    status = pyqtSignal(bool, str)


def contains_number(string):
    return any(char.isdigit() for char in string)    
            










