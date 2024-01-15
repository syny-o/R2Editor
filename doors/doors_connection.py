import time
import subprocess
import os

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QSettings, QRunnable, QThreadPool, QTimer
from dialogs.dialog_message import dialog_message



DEBUG = False




SW_MINIMIZE = 6
SW_HIDE = 0

DXL_FILE = "doors_downloader.dxl"


def create_time_stamp():
    t = time.localtime()
    return time.strftime("%d %B %Y %H:%M", t)


def _create_dxl_columns_string(module_columns: list) -> str:
    return ''.join(['"<COLUMN_START>"o."' + column + '""<COLUMN_END>"' for column in module_columns])



def _create_dxl_query(
    module_path:        str,
    module_columns:     list[str],
    baseline_string:    str | None, 
    ):

    if baseline_string:

        major, minor, suffix = baseline_string.split(".")

        if suffix: 

            baseline = f'{major},{minor},"{suffix}"'

        else:

            baseline = f"{major},{minor},null"
        
        dxl_query = r'''
        
        m = read("''' + str(module_path) + r'''",true)

        //b = getMostRecentBaseline(m)

        module_name = name m
        module_path = path m
        
        out << "<<<MODULE_START>>>\n<PATH_START>" module_path "/" module_name "<PATH_END>" "\n"

        out << "<BASELINES_START>" "\n"

        for b in m do {
            out << "<BASELINE_START><VERSION_START>"(major b)"."(minor b)"."(suffix b)"<VERSION_END><USER_START>" (user b) "<USER_END><DATE_START>" (dateOf b)"<DATE_END><ANNOTATION_START>"(annotation b)"<ANNOTATION_END><BASELINE_END>\n"
        }

        out << "<BASELINES_END>" "\n"

        out << "<ATTRIBUTES_START>" "\n"

        for objAttrName in (m) do
        { 
            out << "<ATTRIBUTE_START>" objAttrName "<ATTRIBUTE_END>" 
        }

        out << "<ATTRIBUTES_END>" "\n"

        out << "<REQUIREMENTS_START>" "\n"

        mSpecificBaseline = load (m, baseline(''' + baseline + r'''), false)
        
        for o in entire(mSpecificBaseline) do {
            out << "<REQUIREMENT_START><ID_START>"identifier(o)"<ID_END><LEVEL_START>"level(o)"<LEVEL_END><HEADING_START>"o."Object Heading""<HEADING_END><COLUMNS_START>"''' + _create_dxl_columns_string(module_columns) + r'''"<COLUMNS_END>"
            
            out << "<OUTLINKS_START>"
            for outLink in all (o -> "*") do {
                out << "<OUTLINK_START>"(fullName targetVersion outLink) ":" (targetAbsNo (outLink)) "<OUTLINK_END>"         
            }
            out << "<OUTLINKS_END>"
            out << "<INLINKS_START>"
            for lrIn in each (o <- "*") do {            
                out << "<INLINK_START>"(fullName sourceVersion lrIn) ":" (sourceAbsNo (lrIn)) "<INLINK_END>" 
            }
            out << "<INLINKS_END>"

            out << "<REQUIREMENT_END>"        
        }

        out << "<REQUIREMENTS_END>" "\n"    

        out << "<<<MODULE_END>>>" "\n"

        '''




    else:

        dxl_query = r'''
        
        m = read("''' + str(module_path) + r'''",true)

        //b = getMostRecentBaseline(m)

        module_name = name m
        module_path = path m
        
        out << "<<<MODULE_START>>>\n<PATH_START>" module_path "/" module_name "<PATH_END>" "\n"

        out << "<BASELINES_START>" "\n"

        for b in m do {
            out << "<BASELINE_START><VERSION_START>"(major b)"."(minor b)"."(suffix b)"<VERSION_END><USER_START>" (user b) "<USER_END><DATE_START>" (dateOf b)"<DATE_END><ANNOTATION_START>"(annotation b)"<ANNOTATION_END><BASELINE_END>\n"
        }

        out << "<BASELINES_END>" "\n"

        out << "<ATTRIBUTES_START>" "\n"

        for objAttrName in (m) do
        { 
            out << "<ATTRIBUTE_START>" objAttrName "<ATTRIBUTE_END>" 
        }

        out << "<ATTRIBUTES_END>" "\n"

        out << "<REQUIREMENTS_START>" "\n"

        for o in entire(m) do {
            out << "<REQUIREMENT_START><ID_START>"identifier(o)"<ID_END><LEVEL_START>"level(o)"<LEVEL_END><HEADING_START>"o."Object Heading""<HEADING_END><COLUMNS_START>"''' + _create_dxl_columns_string(module_columns) + r'''"<COLUMNS_END>"
            
            out << "<OUTLINKS_START>"
            for outLink in (o -> "*") do {
                out << "<OUTLINK_START>"(fullName targetVersion outLink) ":" (targetAbsNo (outLink)) "<OUTLINK_END>"         
            }
            out << "<OUTLINKS_END>"
            out << "<INLINKS_START>"
            for lrIn in each (o <- "*") do {            
                out << "<INLINK_START>"(fullName sourceVersion lrIn) ":" (sourceAbsNo (lrIn)) "<INLINK_END>" 
            }
            out << "<INLINKS_END>"

            out << "<REQUIREMENT_END>"        
        }

        out << "<REQUIREMENTS_END>" "\n"    

        out << "<<<MODULE_END>>>" "\n"

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



def _create_dxl_script(module_paths:list[str], module_columns:list[list], module_current_baselines:list[str|None]):
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

    Module mSpecificBaseline
    """

    content = ""

    for i in range(len(module_paths)):
        content += _create_dxl_query(module_paths[i], module_columns[i], module_current_baselines[i])
        content += "\n"



    return dxl_header + content








class DoorsConnection(QObject):

    send_downloaded_requirements = pyqtSignal(str, str)
    send_progress_status = pyqtSignal(bool, str)



    def __init__(self, data_manager, app_path, database_path, user_name, password, module_paths, columns_names, baselines):
        super().__init__()

        self.data_manager = data_manager
        self.app_path = app_path
        self.database_path = database_path
        self.user_name = user_name
        self.user_passwd = password
        self.paths = module_paths
        self.columns_names = columns_names
        self.module_current_baselines = baselines

        self.send_downloaded_requirements.connect(data_manager.receive_data_from_doors)
        self.send_progress_status.connect(data_manager.update_progress_status)

        self.cmd = fr'{self.app_path} -data "{self.database_path}" -u "{self.user_name}" -P "{self.user_passwd}" -batch "{DXL_FILE}" -W'


        if not DEBUG:
            # DELETE OLD DOORS OUTPUT
            if os.path.isfile("doors/doors_output.txt"):
                os.remove("doors/doors_output.txt")



        # THREADS CONFIGURATION
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(1)
        worker = Worker(self, self.paths, columns_names, self.module_current_baselines)
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
    #     self.end_time = time.time()
    #     delta = self.end_time - self.start_time
    #     if delta < 120:
    #         dialog_message(self.data_manager, f"Connection to {self.database_path} failed!\n Check User Name/Password.")
        


    def update_percentage(self):
        if self.percentage < 10:
            self.percentage += 1
            self.send_progress_status.emit(True,f"Connecting to {self.database_path}: {self.percentage}%")            
        elif self.percentage < 100:
            self.percentage += 1
            self.send_progress_status.emit(True,f"Downloading requirements: {self.percentage}%")
        else:
            self.send_progress_status.emit(True,f"Downloading requirements: {self.percentage}%, updating data...")



    def create_and_run_dxl_script(
        self,
        module_paths: list[str],
        module_columns: list[list[str]],
        module_current_baselines: list[str|None]):



        file_content = _create_dxl_script(module_paths, module_columns, module_current_baselines)
        # print(file_content)

        with open(DXL_FILE, 'w', encoding='utf8') as new_dxl_file:
            new_dxl_file.write(file_content)
            
        if not DEBUG:
            self.process = subprocess.call(self.cmd, shell=False)  

        timestamp = create_time_stamp()
        try:
            with open("doors/doors_output.txt") as f:
                doors_string = f.read()
            self.send_downloaded_requirements.emit(doors_string, timestamp)

            self.send_progress_status.emit(False,"")
        except Exception as e:
            print("Missing Doors Output")
            self.send_downloaded_requirements.emit("Connection Failed", "") 
            self.send_progress_status.emit(False, "")
            
                









class Worker(QRunnable):
    def __init__(self, doors_connection, paths, columns, module_current_baselines):
        super().__init__()
        self.doors_connection = doors_connection
        self.paths = paths
        self.columns = columns
        self.module_current_baselines = module_current_baselines

        self.start_time = time.time()   

    @pyqtSlot()
    def run(self):
        print("Thread start - Connecting to Doors")
        try:

            self.doors_connection.create_and_run_dxl_script(self.paths, self.columns, self.module_current_baselines)

            
        except Exception as e:
            print(e)

        # finally:
        #     self.doors_connection.kill_doors_client()



    # def __del__(self):
    #     self.end_time = time.time()
    #     delta = self.end_time - self.start_time
    #     # print(delta)
    #     if delta < 100:
    #         # self.doors_connection.send_progress_status.emit(True, f"Connection to {self.doors_connection.database_path} failed!")  
    #         self.doors_connection.send_downloaded_requirements.emit("Connection Failed", "")   

            

