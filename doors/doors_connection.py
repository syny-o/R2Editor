import re
import time
import socket
import subprocess
import os


from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QSettings, QRunnable, QThreadPool

SW_MINIMIZE = 6
SW_HIDE = 0



def create_dxl_command(sys_module_path, columns_names):
    """
    COMMAND FOR XPENG/LIXIANG SYDESIGN, SYRS
    """

    dxl_columns_string = b''
    for c in columns_names:
        dxl_columns_string += b'''"<ATTRIBUTE>" o."''' + bytes(c, 'utf-8') + b'''"'''

    sys_dxl_command = b'''
                Object o
                string s = ""
                Module m = read("''' + bytes(sys_module_path, 'utf-8') + b'''", false)
                for o in all(m) do {
                  s = s "<REQUIREMENT>" identifier(o)''' + dxl_columns_string + b'''"\n"
                }
                return_ s
                '''
    return sys_dxl_command




def create_time_stamp():
    t = time.localtime()
    return time.strftime("%d %B %Y %H:%M", t)


def create_req_list(sys_string):
    """
    extract data from STRING which is received from DOORS
    :return: sys_rs(ad_func)(ad_tech)_dictionary according to input parameter

    format: [ [r_ID, Text, ... , ... ], ... ]
    """

    # SPLIT TEXT ACCORDING TO WORD <REQUIREMENT>
    sys_requirements = sys_string.split('<REQUIREMENT>')

    # CREATE LIST
    sys_list = []

    # FILL LIST WITH SUBLISTS WHERE SUBLIST HAS FORMAT [Object_Identifier, Object_Text, Custom_Column2, Custom_Column3, ...]
    for r in sys_requirements[1:]:
        r_list = r.split('<ATTRIBUTE>')
        sys_list.append(r_list)

    return sys_list




class DoorsConnection(QObject):

    send_downloaded_requirements = pyqtSignal(object, object)
    send_progress_status = pyqtSignal(bool, str)

    # SET PATH TO BATCH SERVER
    my_app_directory = os.getcwd()
    batchserver_path = str(my_app_directory) + r'\doors\batchserver.dxl'

    def __init__(self, requirement_node, req_path, columns_names, data_manager, password):
        super().__init__()

        self.data_manager = data_manager

        self.req_path = req_path
        self.columns_names = columns_names

        self.send_downloaded_requirements.connect(requirement_node.receive_data_from_doors)
        self.send_progress_status.connect(data_manager.update_progress_status)

        self.settings = QSettings(r'.\app_config.ini', QSettings.IniFormat)
        self.app_path = self.settings.value('doors/doors_app_path')
        self.database_path = self.settings.value('doors/doors_database_path')
        self.user_name = self.settings.value('doors/doors_user_name')
        # self.user_passwd = self.settings_doors.value('doors_user_passwd')
        self.user_passwd = password

        self.cmd = fr'{self.app_path} -data "{self.database_path}" -u "{self.user_name}" -P "{self.user_passwd}" -batch "{self.batchserver_path}" '

        # self.start_doors()

        # self.start()

        # self.close_connection()

        # THREADS CONFIGURATION
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(1)
        worker = Worker(self)
        self.threadpool.start(worker)

        print(self.database_path)
        print(self.req_path)




    def start_doors_client(self):
        info = subprocess.STARTUPINFO()
        info.dwFlags = subprocess.STARTF_USESHOWWINDOW
        info.wShowWindow = SW_HIDE
        self.my_process = subprocess.Popen(self.cmd, startupinfo=info)


    def establish_connection(self):
        for i in range(5, 0, -1):
            try:
                time.sleep(15)
                self.send_progress_status.emit(True, f'Connecting to {self.database_path}...')
                print(' Connecting to IBM Rational Doors...')
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect(("127.0.0.1", 5093))
                break
            except:
                if i > 1:
                    print(f' Connecting failed, waiting for another attempt ({i-1} remaining)...')
                    self.send_progress_status.emit(True, f' Connecting failed, waiting for another attempt ({i-1} remaining)...')
                else:
                    print("Licensed number of Doors users already reached!")
                    self.send_progress_status.emit(True, "Licensed number of Doors users already reached!")
                    time.sleep(10)
                    self.send_progress_status.emit(False,"")
            


    def download_requirements(self, dxl_command, text):

        self.socket.send(dxl_command)
        print(f' Downloading requirements: {text}...')
        self.send_progress_status.emit(True, f' Downloading requirements: {text}...')
        result = self.socket.recv(9999999)
        # print(result.decode("utf-8"))

        print(f' Updating requirements: {text} ...')
        self.send_progress_status.emit(True, f' Updating requirements: {text}...')

        f = open(f"doors/{text}.txt", "w", encoding='utf-8')
        f.write(result.decode("utf-8"))
        f.close()

        if result.decode("utf-8") == "":
            self.send_progress_status.emit(True, 'No Data received, please check Module Path / Column Names.')
            time.sleep(20)
            self.send_progress_status.emit(False,"")
        return result.decode("utf-8")


    def close_connection(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(("127.0.0.1", 5093))
        self.socket.send(b"quit_")
        self.socket.close()
        self.send_progress_status.emit(True, 'Requirements data have been updated.')
        time.sleep(15)
        self.send_progress_status.emit(False,"")

    def kill_doors_client(self):
        self.my_process.kill()


    def run(self):

        dxl_cmd = create_dxl_command(self.req_path, self.columns_names)
        self.establish_connection()
        received_string = self.download_requirements(dxl_cmd, self.req_path.split('/')[-1])
        req_list = create_req_list(received_string)

        timestamp = create_time_stamp()
        self.send_downloaded_requirements.emit(req_list, timestamp)






class Worker(QRunnable):
    def __init__(self, doors_connection):
        super().__init__()
        self.doors_connection = doors_connection

    @pyqtSlot()
    def run(self):
        print("Thread start - Connecting to Doors")
        try:
            self.doors_connection.start_doors_client()
            self.doors_connection.run()
            self.doors_connection.close_connection()
            
        except Exception as e:
            print(e)

        finally:
            self.doors_connection.kill_doors_client()

            

