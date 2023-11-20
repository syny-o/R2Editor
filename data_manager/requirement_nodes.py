from PyQt5.Qt import QStandardItem, QColor, QFont, QIcon
from PyQt5.QtCore import pyqtSlot, Qt, QRunnable, QThreadPool
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyle, QPushButton
import re, os

import time
from data_manager.tooltips_req import tooltips_req
from components.reduce_path_string import reduce_path_string
from dialogs.dialog_message import dialog_message


# PATTERN_REQ_REFERENCE = re.compile(r'EPB[\d\w_-]+(?:syDesign|funcDesign|techDesign|syRS)[_-]\d+', re.IGNORECASE)

# PATTERN_REQ_REFERENCE = re.compile(r'\$REF:\s*"(?P<req_reference>[\w\d,\s\(\)-]+)"\s*\$', re.IGNORECASE)

# PATTERN_REQ_REFERENCE = re.compile(r'\$REF:\s*"(?P<req_reference>[\w\d,/\s\(\)-]+)"\s*\$', re.IGNORECASE)




PATTERN_REQ_REFERENCE = re.compile(r"""(?:REFERENCE|\$REF:)\s*"(?P<req_reference>[\w\d,/\s\(\)-]+)"\s*""", re.IGNORECASE)




# PATTERN_REQ_REFERENCE = re.compile(r'REFERENCE "(?P<req_reference>.+)"', re.IGNORECASE)

# EPBi-STLA-KM/KX-SyDesign_3538

# REFERENCE "EPBi-Ford-GE2_MY24SyDesign_4700"

# PATTERN_REQ_DETERMINE = re.compile(r"\d\d\d\d - Determine \w*'(?P<keyword>[\w]+)'.[^\s]+", re.IGNORECASE)
PATTERN_REQ_DETERMINE = re.compile(r"the (component|safety mechanism) shall determine '(?P<keyword>[\w]+)'", re.IGNORECASE)


PATTERN_CONSTANT = re.compile(r"^[A-Z0-9_]+$")

def initialise(data: dict, root_node):

    requirement_modules = data.get('REQUIREMENT MODULES')

    for requirement_module in requirement_modules:
        path = requirement_module.get("path")
        update_time = requirement_module.get("update_time")
        columns_names = requirement_module.get("columns")
        attributes = requirement_module.get("attributes")
        baseline = requirement_module.get("baseline")
        coverage_filter = requirement_module.get("coverage_filter")
        coverage_dict = requirement_module.get("coverage_dict")
        ignore_list = requirement_module.get("ignore_list")
        notes = requirement_module.get("notes")
        data = requirement_module.get("requirements")

        if path and data:
            r = RequirementFileNode(root_node, path, columns_names, attributes, baseline, coverage_filter, coverage_dict, update_time, ignore_list, notes)
            r.create_tree_from_requirements_data(data, update_time)
            r.file_2_tree()
            r.update_icons_according_to_coverage()
            
            # r.check_coverage(self.disk_project_path)
        elif not data:
            r = RequirementFileNode(root_node, path, columns_names, attributes, baseline, coverage_filter, coverage_dict, update_time, ignore_list, notes)
            r.file_2_tree()       




def _create_list_of_requirements_from_module(module, my_list=None) -> list[dict]:
    if my_list is None:
        requirement_list = []
    else:
        requirement_list = my_list
    
    for row in range(module.rowCount()):
        one_requirement_node = module.child(row)
        
        one_requirement_data = {
            "reference": one_requirement_node.reference,
            "heading": one_requirement_node.heading,
            "level": one_requirement_node.level,
            "outlinks": one_requirement_node.outlinks,
            "inlinks": one_requirement_node.inlinks,
            "file_references": list(one_requirement_node.file_references),
            "is_covered" : one_requirement_node.is_covered,            
            "columns_data": one_requirement_node.columns_data,
        }

        requirement_list.append(one_requirement_data)
        _create_list_of_requirements_from_module(one_requirement_node, requirement_list)
    
    return requirement_list












class RequirementFileNode(QStandardItem):
    def __init__(self, root_node, path, columns_names, attributes, baseline, coverage_filter, coverage_dict, update_time, ignore_list, notes):
        super().__init__()
        self.root_node = root_node
        self.data_manager = self.root_node.data(Qt.UserRole)
        # print(root_node.data(Qt.UserRole))
        self.path = path
        self.columns_names = columns_names
        # backup original column names, when column names are edited, these backuped columns are used for displying until new Updtate Req is performed
        self.columns_names_backup = [*columns_names]  
        

        self.timestamp = update_time

        self.setIcon(QIcon(u"ui/icons/doors.png"))

        self.setText(reduce_path_string(self.path))

        self.setEditable(False)

        self.coverage_filter = coverage_filter

        # self.show_only_coverage = False
        # self.show_only_not_covered = False

        self.view_filter = "all"

        if self.coverage_filter: 
            self.coverage_check = True
            # self.apply_coverage_filter()
            
        else:
            self.coverage_check = False

        self.is_covered = 0

        self.ignore_list = set(ignore_list) if ignore_list else set()

        self.attributes = attributes or []

        self.baseline = baseline or {}

        self.notes = notes or {}

        self.coverage_dict = coverage_dict or {}

        self.update_title_text()




        # self.threadpool = QThreadPool()
        # self.threadpool.setMaxThreadCount(1)



    def update_title_text(self):
        if self.coverage_check:
            number_of_covered_requirements = 0
            number_of_calculated_requirements = 0
            for k, v in self.coverage_dict.items():
                number_of_calculated_requirements += 1
                if v:
                    number_of_covered_requirements += 1
            
            self.setText(reduce_path_string(self.path) + f" ({number_of_covered_requirements}/{number_of_calculated_requirements})")



    def file_2_tree(self):
        self.root_node.appendRow(self)  # APPEND NODE AS A CHILD


        




    def create_tree_from_requirements_data(self, req_list, timestamp):
        self.timestamp = timestamp
        
        last_level = 0
        parents = []
        last_item = self

        for one_requirement in req_list:  # requirements => list, requirement => dict            
            # REFERENCE
            reference = one_requirement.get("reference")
            # COLUMNS
            columns_data = one_requirement.get("columns_data")                
            # LEVEL
            level = one_requirement.get("level")
            level = int(level)
            # HEADING
            heading = one_requirement.get("heading")

            # INLINKS
            inlinks = one_requirement.get("inlinks")            
            # OUTLINKS
            outlinks = one_requirement.get("outlinks")
            # FILE REFERENCES
            file_references = one_requirement.get("file_references")              
            # is_covered
            is_covered = one_requirement.get("is_covered")   

            # UPDATE COVERAGE DICT
            if is_covered is not None and not heading:
                self.update_coverage_dict(reference, file_references)       

            # CREATE REQUIREMENT NODE
            item = RequirementNode(reference, heading, level, outlinks, inlinks, file_references, columns_data, is_covered)
            # APPEND TO MODEL
            if level == last_level:
                parents[-1].appendRow(item)

            elif level > last_level:
                parents.append(last_item)
                parents[-1].appendRow(item)

            else:
                dif = last_level - level
                for _ in range(dif):
                    parents.pop()
                parents[-1].appendRow(item)

            last_level = int(level)   
            last_item = item 


    
    def update_coverage_dict(self, reference, file_references):
        self.coverage_dict.update({reference: file_references})

        









    def tree_2_file(self):
        pass


    
    def update_icons_according_to_coverage(self):
        def browse_children(parent_node, string):                
            for row in range(parent_node.rowCount()):
                requirement_node = parent_node.child(row)
                
                if requirement_node.is_covered is not None:
                    requirement_node.update_coverage(requirement_node.is_covered)

                browse_children(requirement_node, string)                
        browse_children(self, self.coverage_filter)                 



    def check_coverage_with_file_pointers(self, project_path, reference_dict):

        if project_path and self.coverage_check:
            time_start = time.time()
            # reference_dict = self.create_reference_dict(project_path)

            # CLEAR COVERAGE DICT
            self.coverage_dict.clear()

            def browse_children(parent_node):
                # nonlocal reference_dict
                for row in range(parent_node.rowCount()):
                    current_req_node = parent_node.child(row)  

                    stepanova_picovina = current_req_node.text().replace("SyDesign", "-SyDesign")
                    stepanova_picovina_count = 0
                    # print(stepanova_picovina.lower())
                    # print(stepanova_picovina, "---->", current_req_node.text())

                    #  in dict is: epb_chrysler_my24_dt-sydesign_6724

                    if current_req_node.is_covered is not None and not current_req_node.heading:
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
                            current_req_node.file_references.clear()
                            # self.setIcon(QPushButton().style().standardIcon(QStyle.SP_DialogCancelButton)) 

                        # UPDATE COVERAGE DICT
                        self.coverage_dict.update({current_req_node.reference: list(current_req_node.file_references)})

                    else:
                        current_req_node.file_references.clear()
                        # self.coverage_dict.pop(current_req_node.reference, None)

                    browse_children(current_req_node)


            # browse all children (req nodes) and update its coverage
            self.is_covered = 0

            browse_children(self)

            time_end = time.time()
            time_delta = time_end - time_start
            print(f'Coverage Check took {time_delta} seconds')            


            
    def create_reference_dict(self, project_path): 
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

        return reference_dict         






            








    def data_4_project(self, data_from_root):        
        requirement_modules = data_from_root.get("REQUIREMENT MODULES")
        my_data = {
            "path"              : self.path,
            "columns"           : self.columns_names_backup,
            "attributes"        : self.attributes,
            "baseline"          : self.baseline,
            "update_time"       : self.timestamp,  
            "coverage_filter"   : self.coverage_filter,    
            "coverage_dict"     : self.coverage_dict,
            "ignore_list"       : list(self.ignore_list),
            "notes"             : self.notes,
            "requirements"      : _create_list_of_requirements_from_module(self),
            }
        requirement_modules.append(my_data)  


        return data_from_root      
           



    # @pyqtSlot(object)
    def receive_data_from_doors(self, doors_output, timestamp):
        self.timestamp = timestamp
        # delete all children
        self.removeRows(0, self.rowCount())
        # create new children from received data
        # self.create_tree_from_requirements_data(req_list, timestamp)
        self._txtfile_to_tree(doors_output)
        # once succefull update is performed, update backup columns
        self.columns_names_backup = [*self.columns_names]  
        
        # APPLY FILTER WHICH HAS BEEN APPLIED BEFORE DOWNLOADING
        self.apply_coverage_filter()
        # UPDATE ACCORDING TO COVERAGE DICT WHICH IS STORED IN REQUIREMENT MODULE INDEPENDETLY TO REQUIREMETS NODES
        self.update_coverage_from_coverage_dict()



    def update_coverage_from_coverage_dict(self):
        def browse_children(parent_node, string):                
            for row in range(parent_node.rowCount()):
                requirement_node = parent_node.child(row)
                
                if requirement_node.reference in self.coverage_dict:
                    file_references = self.coverage_dict[requirement_node.reference]
                    if file_references:
                        requirement_node.update_coverage(True)
                        requirement_node.file_references = file_references
                    else:
                        requirement_node.update_coverage(False)
                        requirement_node.file_references = set()
                # else:
                #     requirement_node.update_coverage(None)
                #     requirement_node.file_references = set()

                browse_children(requirement_node, string)                
        browse_children(self, self.coverage_filter)             
        



    def _txtfile_to_tree(self, doors_string):

            last_level = 0

            parents = []

            modules = doors_string.split("<<<MODULE>>>")[1:]

            for module in modules:
                
                # MODULE PATH
                path = re.search(r"<<<PATH>>>(.+?)<<<", module)
                # path = path.group(1)

                if path and path.group(1) == self.path:

                    print("MODULE", self.path)

                    # BASELINE INFO
                    # out << "<<<BASELINE>>><<<VERSION>>>"(major b)"."(minor b)""(suffix b)"<<<USER>>>" (user b) "<<<DATE>>>" (dateOf b)"<<<ANNOTATION>>>"(annotation b)""
                    baseline = {}
                    baseline_match = re.search(r"<<<BASELINE>>>(.+?)<<<ATTRIBUTE>>>", module, re.DOTALL)
                    baseline_string = baseline_match.group(1)
                    
                    baseline_version = re.search(r"<<<VERSION>>>(.+?)<<<", baseline_string)
                    baseline_user = re.search(r"<<<USER>>>(.+?)<<<", baseline_string)
                    baseline_date = re.search(r"<<<DATE>>>(.+?)<<<", baseline_string)
                    baseline_annotation = re.search(r"<<<ANNOTATION>>>(.+)", baseline_string, re.DOTALL)

                    baseline["version"] = baseline_version.group(1)
                    baseline["user"] = baseline_user.group(1)
                    baseline["date"] = baseline_date.group(1)
                    baseline["annotation"] = baseline_annotation.group(1)

                    if self.baseline:
                        if self.baseline != baseline:
                            dialog_message(
                                self.data_manager, 
                                f"Baseline for {self.path} has been updated to version {baseline['version']}.\n\nUpdated on: {baseline['date']}\n\nUpdated by: {baseline['user']}\n\nDetails:\n{baseline['annotation']}\n\n",
                                f"Baseline Update"
                            )

                    self.baseline = baseline

                    # print(baseline)

                    # ATTRIBUTES
                    attributes = re.findall(r"<<<ATTRIBUTE>>>(.+?)<<<", module)
                    if attributes:
                        self.attributes = attributes

                    last_item = self
                    
                    requirements = module.split("<<<REQUIREMENT>>>")[1:]

                    for requirement in requirements:
                        
                        # REFERENCE
                        reference = re.search(r"<<<ID>>>(.+?)<<<", requirement)
                        reference = reference.group(1)

                        # COLUMNS
                        columns = requirement.split("<<<COLUMN>>>")[1:]
                            
                        # LEVEL
                        level = re.search(r"<<<LEVEL>>>(.+?)<<<", requirement)
                        level = level.group(1)
                        level = int(level)

                        # HEADING
                        heading = re.search(r"<<<HEADING>>>(.*?)<<<", requirement)
                        if heading and len(heading.group(1)) > 1:
                            heading = heading.group(1)
                        else:
                            heading = ""

                        # INLINKS
                        if len(columns) > 0:
                            links_string = columns[-1]
                        else:
                            links_string = requirement

                        if "<<<INLINK>>>" in links_string:
                            inlinks = links_string.split("<<<INLINK>>>")[1:]
                            if len(columns) > 0:
                                columns[-1] = columns[-1].split("<<<INLINK>>>")[0]
                        else:
                            inlinks = []  
 
                        # OUTLINKS
                        if "<<<OUTLINK>>>" in links_string:
                            links_string = links_string.split("<<<INLINK>>>")[0]
                            outlinks = links_string.split("<<<OUTLINK>>>")[1:]
                            
                            if len(columns) > 0:
                                columns[-1] = columns[-1].split("<<<OUTLINK>>>")[0]
                        else:
                            outlinks = []

                           

                        
                        # CREATE REQUIREMENT NODE
                        item = RequirementNode(reference, heading, level, outlinks, inlinks, None, columns)

                        # APPEND TO MODEL
                        if level == last_level:
                            parents[-1].appendRow(item)

                        elif level > last_level:
                            parents.append(last_item)
                            parents[-1].appendRow(item)

                        else:
                            dif = last_level - level
                            for _ in range(dif):
                                parents.pop()
                            parents[-1].appendRow(item)

                        last_level = int(level)   
                        last_item = item  



    def apply_coverage_filter(self):

        if self.coverage_filter:

            def browse_children(parent_node, string):
                    
                for row in range(parent_node.rowCount()):
                    item = parent_node.child(row)

                    try:
                        column = item.columns_data
                        evaluation = eval(string)
                        
                    except Exception as ex:
                        self.coverage_check = False
                        self.coverage_filter = None
                        break

    
                    if evaluation:
                        if item.reference not in self.ignore_list:  # IGNORE LIST CHECK
                            item.update_coverage(False)
                        else:
                            item.update_coverage(None)
                    
                    else:
                        item.update_coverage(None)

                    browse_children(item, string)
                
        
            browse_children(self, self.coverage_filter)    


    def remove_coverage_filter(self):
        self.coverage_filter = None
        self.coverage_check = False
        
        def browse_children(parent_node):
                
            for row in range(parent_node.rowCount()):
                item = parent_node.child(row)

                item.update_coverage(None)                    

                browse_children(item)            
    
        browse_children(self)           
        self.setIcon(QIcon(u"ui/icons/doors.png"))




class RequirementNode(QStandardItem):
    def __init__(
        self, 
        reference: str, 
        heading: str, 
        level: int,
        outlinks: list[str],
        inlinks: list[str],        
        file_references: list[str],
        columns_data: list[str],
        is_covered = None,        
        ):

        super().__init__()
        self.setEditable(False)

        self.reference = reference
        self.heading = heading
        self.level = level
        
        if outlinks:
            self.outlinks = [o.strip() for o in outlinks]
        else:
            self.outlinks = []
        if inlinks:
            self.inlinks = [i.strip() for i in inlinks]
        else:
            self.inlinks = []
        self.is_covered = is_covered
        self.columns_data = columns_data  # list

        if self.heading:
            self.setText(heading)
        else:
            self.setText(reference)        

        # FILE REFERENCES
        if file_references:
            self.file_references = set(file_references)
        else:
            self.file_references = set()




    def update_coverage(self, is_covered):

        self.is_covered = is_covered

        if is_covered == True:

            self.setIcon(QIcon(u"ui/icons/check.png"))
            for _ in range(self.level):
                parent = self.parent()
                children = []
                for row in range(parent.rowCount()):
                    children.append(parent.child(row))
                children_covered = True
                for child in children:
                    if child.is_covered == False:
                        children_covered =  False

                if children_covered:
                    self.parent().setIcon(QIcon(u"ui/icons/check.png"))
                    self.parent().is_covered = True
                if not isinstance(self, RequirementFileNode):
                    self = self.parent()
        
        elif is_covered == False:
            self.setIcon(QIcon(u"ui/icons/cross.png"))
            
            for _ in range(self.level):
                self.parent().setIcon(QIcon(u"ui/icons/cross.png"))
                self.parent().is_covered = False
                if not isinstance(self, RequirementFileNode):
                    self = self.parent()

        else: 
            self.setIcon(QIcon())
            for _ in range(self.level):
                parent = self.parent()
                children = []
                for row in range(parent.rowCount()):
                    children.append(parent.child(row))
                children_none = True
                for child in children:
                    if child.is_covered is not None:
                        children_none =  False

                if children_none:
                    self.parent().setIcon(QIcon()) if isinstance(self.parent(), RequirementNode) else self.parent().setIcon(QIcon(u"ui/icons/doors.png"))
                    self.parent().is_covered = None
                if not isinstance(self, RequirementFileNode):
                    self = self.parent()    



        

    
    def get_requirement_module(self):
        item = self
        while isinstance(item, RequirementNode):
            item = item.parent()
        return item     


    def add_to_ignore_list(self):
        if not self.hasChildren():  # if it is not Heading
            self.update_coverage(None)
            my_module = self.get_requirement_module()
            my_module.ignore_list.add(self.reference)


    def remove_from_ignore_list(self):
        my_module = self.get_requirement_module()
        if not self.hasChildren():  # if it is not Heading
            if self.reference in my_module.ignore_list:            
                self.update_coverage(False)
                my_module.ignore_list.remove(self.reference)   


    def update_note(self, text):
        if text.strip() != "":
            self.get_requirement_module().notes.update({self.reference: text})
        else:     
            self.get_requirement_module().notes.pop(self.reference, None)


    def get_note(self):
        if self.reference in self.get_requirement_module().notes:
       
            return self.get_requirement_module().notes[self.reference]
        return ""

