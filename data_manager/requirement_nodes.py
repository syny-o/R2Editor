from PyQt5.Qt import QStandardItem, QColor, QFont, QIcon
from PyQt5.QtCore import pyqtSlot, Qt, QRunnable, QThreadPool
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyle, QPushButton
import re, os
from doors.doors_connection import DoorsConnection
import time
from data_manager.tooltips_req import tooltips_req
from components.reduce_path_string import reduce_path_string


# PATTERN_REQ_REFERENCE = re.compile(r'EPB[\d\w_-]+(?:syDesign|funcDesign|techDesign|syRS)[_-]\d+', re.IGNORECASE)

PATTERN_REQ_REFERENCE = re.compile(r'\$REF:\s*"(?P<req_reference>[\w\d,\s\(\)-]+)"\s*\$', re.IGNORECASE)

# PATTERN_REQ_DETERMINE = re.compile(r"\d\d\d\d - Determine \w*'(?P<keyword>[\w]+)'.[^\s]+", re.IGNORECASE)
PATTERN_REQ_DETERMINE = re.compile(r"the (component|safety mechanism) shall determine '(?P<keyword>[\w]+)'", re.IGNORECASE)


PATTERN_CONSTANT = re.compile(r"^[A-Z0-9_]+$")

def initialise(data: dict, root_node):
    """
            data = {
        'disk_project_path': disk_project_path,
        'Conditions Files': cond_files,
        'DSpace Files': a2l_files,
        'A2L Files': a2l_files,
        'Requirements': requirements

        requirements = [{path: []} for path in req]
    }

    """
    requirements_list = data.get('Requirements')
    if requirements_list:
        for requirements_dict in requirements_list:
            for req_path, req_data in requirements_dict.items():
                data = req_data[0]
                columns_names = req_data[1]
                timestamp = req_data[2]
                coverage_check = req_data[3]
                if req_path and data:
                    r = RequirementFileNode(root_node, req_path, columns_names, coverage_check)
                    r.create_tree_from_requirements_data(data, timestamp)
                    r.file_2_tree()
                    
                    # r.check_coverage(self.disk_project_path)
                elif not data:
                    r = RequirementFileNode(root_node, req_path, columns_names, coverage_check)
                    r.file_2_tree()





class RequirementFileNode(QStandardItem):
    def __init__(self, root_node, path, columns_names, coverage_check):
        super().__init__()
        self.root_node = root_node
        self.data_manager = self.root_node.data(Qt.UserRole)
        # print(root_node.data(Qt.UserRole))
        self.path = path
        self.columns_names = columns_names
        # backup original column names, when column names are edited, these backuped columns are used for displying until new Updtate Req is performed
        self.columns_names_backup = [*columns_names]  
        self.coverage_check = coverage_check

        self.timestamp = None

        self.setIcon(QIcon(u"ui/icons/doors.png"))

        self.setText(reduce_path_string(self.path))

        self.setEditable(False)

        # self.file_2_tree()
        # self.root_node.appendRow(self)  # APPEND NODE AS A CHILD

        self.is_covered = 0

        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(1)



    def file_2_tree(self):
        self.root_node.appendRow(self)  # APPEND NODE AS A CHILD


        





    def create_tree_from_requirements_data(self, req_list, timestamp):
        self.timestamp = timestamp
        

        for req_values in req_list:
            
            is_covered = False
            file_references = None
            if type(req_values) is dict:
                is_covered = req_values.get("is_covered")
                file_references = req_values.get("file_references")
                req_values = req_values.get("columns_data")
                
                

            
            req_node = RequirementNode(req_values)
            req_node.is_covered = is_covered
            
            if req_node.is_covered:
                self.is_covered += 1

            if file_references:
                req_node.file_references = set([*file_references])

            self.appendRow(req_node)  # APPEND NODE AS A CHILD

            ### PRASARNA - NACIST DO TOOLTIPU NEKTERA DATA --> NAPR ZE SYDESIGN: 2022 - Determine 'DriverControlsTheVehicle'.True:

            if "SyDesign" in req_node.parent().path:
                if match := PATTERN_REQ_DETERMINE.search(req_node.columns_data[-1]):
                    key = match.group("keyword")
                    value = req_node.columns_data[-1]
                    if key in tooltips_req:
                        new_value = tooltips_req[key] + "\n" + value
                        tooltips_req.update({key : new_value})
                    else:
                        tooltips_req.update({key : value})
                
                elif match := PATTERN_REQ_DETERMINE.search(req_node.columns_data[-2]):
                    key = match.group("keyword")
                    value = req_node.columns_data[-2]
                    if key in tooltips_req:
                        new_value = tooltips_req[key] + "\n" + value
                        tooltips_req.update({key : new_value})
                    else:
                        tooltips_req.update({key : value})

            if "VC-EPBi" in req_node.parent().path:
                if match := PATTERN_CONSTANT.search(req_node.columns_data[-1].strip()):
                    key = match.group()
                    value = req_node.columns_data[1]
                    tooltips_req.update({key : f"{key} == {value}"}) 
                    # print(key, value)                   
            

        
        # print(tooltips_req)

        # self.sortChildren(0)

        


    # @pyqtSlot(object)
    def receive_data_from_doors(self, req_list, timestamp):
        # delete all children
        self.removeRows(0, self.rowCount())
        # create new children from received data
        self.create_tree_from_requirements_data(req_list, timestamp)
        # once succefull update is performed, update backup columns
        self.columns_names_backup = [*self.columns_names]


    def tree_2_file(self):
        pass


    def send_request_2_doors(self, password):
        DoorsConnection(self, self.path, self.columns_names, self.data_manager, password)


    def check_coverage_with_file_pointers(self, project_path):
        if project_path and self.coverage_check:
            # # COUPLING !!!!
            # self.data_manager.ui_check_coverage.setEnabled(False)
            # # COUPLING !!!!
            # worker = Worker(self, project_path)
            # self.threadpool.start(worker)


            if project_path and self.coverage_check:
                time_start = time.time()
                reference_dict = {}

                for root, dirs, files in os.walk(project_path):
                    for filename in files:
                        if filename.endswith((".par", ".txt")):
                            full_path = (root + '\\' + filename)
                            full_path = full_path.replace("\\", "/")
                            with open(full_path, 'r') as f:
                                text = f.read()
                                reference_list = PATTERN_REQ_REFERENCE.findall(text)

                                for ref_string in reference_list: # ref string is in following form: 
                                    references = ref_string.split(",")
                                    for ref in references:
                                        ref = ref.lower().strip()

                                        if ref in reference_dict:
                                            reference_dict[ref].add(full_path)
                                        else:
                                            reference_dict.update({ref: set([full_path,])})            


                    # with open(r"test_req.txt", 'w', encoding='utf8') as f:
                    #     f.write(str(reference_dict.keys()))




                # browse all children (req nodes) and update its coverage
                self.is_covered = 0
                for row in range(self.rowCount()):
                    current_req_node = self.child(row)
                    stepanova_picovina = current_req_node.text().replace("DTSyDesign", "DT-SyDesign")
                    stepanova_picovina_count = 0
                    # print(stepanova_picovina.lower())
                    # print(stepanova_picovina, "---->", current_req_node.text())

                    #  in dict is: epb_chrysler_my24_dt-sydesign_6724

                    if current_req_node.text().lower() in reference_dict:
                        current_req_node.update_coverage(True)
                        current_req_node.file_references = reference_dict.get(current_req_node.text().lower())
                        self.is_covered += 1
                    elif stepanova_picovina.lower() in reference_dict:
                        current_req_node.update_coverage(True)
                        current_req_node.file_references = reference_dict.get(stepanova_picovina.lower())
                        self.is_covered += 1
                        stepanova_picovina_count += 1
                        # print("Stepanova_picovina", stepanova_picovina_count, stepanova_picovina_count)
                    else:
                        current_req_node.update_coverage(False)
                        # self.setIcon(QPushButton().style().standardIcon(QStyle.SP_DialogCancelButton))
                time_end = time.time()
                time_delta = time_end - time_start
                print(f'Coverage Check took {time_delta} seconds')     
                self.data_manager.update_data_summary()  







            time_end = time.time()
            time_delta = time_end - time_start
            print(f'Coverage Check took {time_delta} seconds')


    def data_4_project(self, data):
        req_list = data.get('Requirements')

        req_node_data = []
        


        for i in range(self.rowCount()):  # iterate through all req nodes
            req_node_subdata = {}
            req_node = self.child(i)  # get object on <i=index> row
            req_node_subdata.update({
                "columns_data" : req_node.columns_data,
                "is_covered" : req_node.is_covered,
                "file_references" : list(req_node.file_references),
                })

            req_node_data.append(req_node_subdata)
            
            




        req_list.append({
            self.path: [req_node_data, self.columns_names_backup, self.timestamp, self.coverage_check]
        })

        data.update(
            {
                'Requirements': req_list
            }
        )

        return data



class RequirementNode(QStandardItem):
    def __init__(self, columns_data: list):
        """
        column_names = ['Object Text_DXL', '010_Object Type', '011_DXL_Object State', '050_Test Department']
        column_data = ['EPBi_Lixiang_X03-SyDesign-123', 'Requirement', 'Approved', 'EPB_TV_1']
        """
        super().__init__()
        self.columns_data = columns_data

        self.is_covered = False

        self.file_references = set()


        self.setText(columns_data[0])

        self.setEditable(False)


    def update_coverage(self, is_covered: bool):
        # self.setIcon(QIcon(u"ui/icons/check.png")) if is_covered \
        #     else self.setIcon(QPushButton().style().standardIcon(QStyle.SP_DialogCancelButton))
        # if not is_covered:
        #     self.setForeground(QColor("red"))
        # else:
        #     self.setForeground(QColor("white"))
        self.is_covered = is_covered








# class Worker(QRunnable):

#     def __init__(self, requirement_file_node, project_path):
#         super().__init__()
#         self.requirement_file_node = requirement_file_node
#         self.project_path = project_path

#     @pyqtSlot()
#     def run(self):

#         try:
#             # !!! START COUPLING
#             # self.requirement_file_node.data_manager.ui_check_coverage.setEnabled(False) NEJDE
#             # !!! END COUPLING

#             if self.project_path and self.requirement_file_node.coverage_check:

#                 print(self.requirement_file_node)
#                 print(self.project_path)
#                 time_start = time.time()
#                 reference_dict = {}

#                 for root, dirs, files in os.walk(self.project_path):
#                     for filename in files:
#                         if filename.endswith((".par", ".txt")):
#                             full_path = (root + '\\' + filename)
#                             full_path = full_path.replace("\\", "/")
#                             with open(full_path, 'r') as f:
#                                 text = f.read()
#                                 reference_list = PATTERN_REQ_REFERENCE.findall(text)

#                                 for ref_string in reference_list: # ref string is in following form: 
#                                     references = ref_string.split(",")
#                                     for ref in references:
#                                         ref = ref.lower().strip()

#                                         if ref in reference_dict:
#                                             reference_dict[ref].add(full_path)
#                                         else:
#                                             reference_dict.update({ref: set([full_path,])})            


#                 #     # with open(r"test_req.txt", 'w', encoding='utf8') as f:
#                 #     #     f.write(str(reference_dict.keys()))




#                 # browse all children (req nodes) and update its coverage
#                 self.requirement_file_node.is_covered = 0
#                 for row in range(self.requirement_file_node.rowCount()):
#                     current_req_node = self.requirement_file_node.child(row)
#                     stepanova_picovina = current_req_node.text().replace("DTSyDesign", "DT-SyDesign")
#                     stepanova_picovina_count = 0
#                     # print(stepanova_picovina.lower())
#                     # print(stepanova_picovina, "---->", current_req_node.text())

#                 #     #  in dict is: epb_chrysler_my24_dt-sydesign_6724

#                     if current_req_node.columns_data[0].lower() in reference_dict: 
#                         current_req_node.update_coverage(True)
#                         current_req_node.file_references = reference_dict.get(current_req_node.columns_data[0].lower())
#                         self.requirement_file_node.is_covered += 1
#                     elif stepanova_picovina.lower() in reference_dict:
#                         current_req_node.update_coverage(True)
#                         current_req_node.file_references = reference_dict.get(stepanova_picovina.lower())
#                         self.requirement_file_node.is_covered += 1
#                         stepanova_picovina_count += 1
#                         # print("Stepanova_picovina", stepanova_picovina_count, stepanova_picovina_count)
#                     else:
#                         current_req_node.update_coverage(False)
#                         # self.requirement_file_node.setIcon(QPushButton().style().standardIcon(QStyle.SP_DialogCancelButton))

#                 time_end = time.time()
#                 time_delta = time_end - time_start
#                 print(f'Coverage Check took {time_delta} seconds')      


            
#         except Exception as e:
            
#             print(e)

#         finally:
#             # !!! START COUPLING
#             self.requirement_file_node.data_manager.ui_check_coverage.setEnabled(True)
#             self.requirement_file_node.data_manager.update_data_summary()
#             # !!! END COUPLING

