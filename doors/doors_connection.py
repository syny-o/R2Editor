import re
import time
import socket
import subprocess
import os


from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QSettings, QRunnable, QThreadPool, QTimer

SW_MINIMIZE = 6
SW_HIDE = 0

dxl_file = "doors_downloader.dxl"


def create_time_stamp():
    t = time.localtime()
    return time.strftime("%d %B %Y %H:%M", t)


def _create_dxl_columns_string(module_columns: list) -> str:
    return ''.join(['"<<<COLUMN>>>"o."' + column + '"' for column in module_columns])



def _create_dxl_query(
    module_path: str,
    module_columns: list[str],):
    dxl_query = r'''
    
    m = read("''' + str(module_path) + r'''",true)

    b = getMostRecentBaseline(m)

    module_name = name m
    module_path = path m
    out << "<<<MODULE>>><<<PATH>>>" module_path "/" module_name ""
    out << "<<<BASELINE>>><<<VERSION>>>"(major b)"."(minor b)"."(suffix b)"<<<USER>>>" (user b) "<<<DATE>>>" (dateOf b)"<<<ANNOTATION>>>"(annotation b)""

    for objAttrName in (m) do
    { 
        out << "<<<ATTRIBUTE>>>" objAttrName 
    }

    for o in entire(m) do {
        out << "<<<REQUIREMENT>>><<<ID>>>"identifier(o)"<<<LEVEL>>>"level(o)"<<<HEADING>>>"o."Object Heading"''' + _create_dxl_columns_string(module_columns) + r'''""
        for outLink in (o -> "*") do {
            out << "<<<OUTLINK>>>"(fullName targetVersion outLink) ":" (targetAbsNo (outLink)) ""         
        }
        for lrIn in each (o <- "*") do {            
            out << "<<<INLINK>>>"(fullName sourceVersion lrIn) ":" (sourceAbsNo (lrIn)) "" 
        }        
    }

    '''
    return dxl_query



# def _create_dxl_query(
#     module_path: str,
#     module_columns: list[str],):
#     dxl_query = r'''
    
#     m = read("''' + str(module_path) + r'''",true)

#     b = getMostRecentBaseline(m)

#     module_name = name m
#     module_path = path m
#     out << "<<<MODULE>>><<<PATH>>>" module_path "/" module_name ""
#     out << "<<<BASELINE>>><<<VERSION>>>"(major b)"."(minor b)"."(suffix b)"<<<USER>>>" (user b) "<<<DATE>>>" (dateOf b)"<<<ANNOTATION>>>"(annotation b)""

#     Module mBaseline = load (m, getMostRecentBaseline(m, false), false)

#     for as in m do
#     { 
#         out << "<<<ATTRIBUTE>>>" as 
#     }

#     for o in entire(mBaseline) do {
#         out << "<<<REQUIREMENT>>><<<ID>>>"identifier(o)"<<<LEVEL>>>"level(o)"<<<HEADING>>>"o."Object Heading"''' + _create_dxl_columns_string(module_columns) + r'''""
#         for outLink in (o -> "*") do {
#             out << "<<<OUTLINK>>>"(fullName targetVersion outLink) ":" (targetAbsNo (outLink)) ""         
#         }
#         for lrIn in each (o <- "*") do {            
#             out << "<<<INLINK>>>"(fullName sourceVersion lrIn) ":" (sourceAbsNo (lrIn)) "" 
#         }        
#     }

#     '''
#     return dxl_query



def _create_dxl_script(module_paths:list[str], module_columns:list[list]):
    dxl_header = r"""
    // Turn off runlimit for timing
    pragma encoding,"utf-8"
    pragma runLim,0

    string file_location = "doors/doors_output.txt"

    // Open stream
    Stream out = write file_location
    Object o
    Link outLink
    LinkRef lrIn
    Module m
    Baseline b
    string module_name
    AttrDef ad
    string objAttrName 
    """

    content = ""

    for i in range(len(module_paths)):
        content += _create_dxl_query(module_paths[i], module_columns[i])
        content += "\n"



    return dxl_header + content








class DoorsConnection(QObject):

    send_downloaded_requirements = pyqtSignal(object, object)
    send_progress_status = pyqtSignal(bool, str)

    # SET PATH TO BATCH SERVER
    # my_app_directory = os.getcwd()
    # batchserver_path = str(my_app_directory) + r'\doors\batchserver.dxl'

    def __init__(self, requirement_node, paths: list, columns_names: list, data_manager, password):
        super().__init__()

        self.data_manager = data_manager

        self.paths = paths
        self.columns_names = columns_names

        self.send_downloaded_requirements.connect(data_manager.receive_data_from_doors)
        self.send_progress_status.connect(data_manager.update_progress_status)

        self.settings = QSettings(r'.\app_config.ini', QSettings.IniFormat)
        self.app_path = self.settings.value('doors/doors_app_path')
        self.database_path = self.settings.value('doors/doors_database_path')
        self.user_name = self.settings.value('doors/doors_user_name')
        # self.user_passwd = self.settings_doors.value('doors_user_passwd')
        self.user_passwd = password

        self.cmd = fr'{self.app_path} -data "{self.database_path}" -u "{self.user_name}" -P "{self.user_passwd}" -batch "{dxl_file}"'

        # self.start_doors()

        # self.start()

        # self.close_connection()

        # THREADS CONFIGURATION
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(1)
        worker = Worker(self, paths, columns_names)
        self.threadpool.start(worker)

        print(self.database_path)
        print(self.paths)

        self.percentage = 0

        self.timer = QTimer()
        if len(self.paths) > 1:
            self.timer.start(3500)
        else:
            self.timer.start(3000)
        

        self.timer.timeout.connect(self.update_percentage)



    # def __del__(self):
    #     self.process.
    #     subprocess





    def update_percentage(self):
        if self.percentage < 100:
            self.percentage += 1
            self.send_progress_status.emit(True,f"Downloading requirements: {self.percentage}%")
        else:
            self.send_progress_status.emit(True,f"Downloading requirements: {self.percentage}%, updating data...")



    def create_and_run_dxl_script(
        self,
        module_paths: list[str],
        module_columns: list[list[str]],):



        file_content = _create_dxl_script(module_paths, module_columns)
        # print(file_content)

        with open(dxl_file, 'w', encoding='utf8') as new_dxl_file:
            new_dxl_file.write(file_content)
            
        self.process = subprocess.call(self.cmd, shell=False)  

        timestamp = create_time_stamp()
        try:
            with open("doors/doors_output.txt") as f:
                doors_string = f.read()
            self.send_downloaded_requirements.emit(doors_string, timestamp)

            self.send_progress_status.emit(False,"")
        except Exception as e:
            with open(f"error_{timestamp}.log", "w") as log:
                log.write("create_and_run_dxl_script ERROR:  " + str(e))
                









class Worker(QRunnable):
    def __init__(self, doors_connection, paths, columns):
        super().__init__()
        self.doors_connection = doors_connection
        self.paths = paths
        self.columns = columns

    @pyqtSlot()
    def run(self):
        print("Thread start - Connecting to Doors")
        try:

            self.doors_connection.create_and_run_dxl_script(self.paths, self.columns)

            
        except Exception as e:
            print(e)

        # finally:
        #     self.doors_connection.kill_doors_client()

            

