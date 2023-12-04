from PyQt5.Qt import QStandardItem, QColor, QFont, QIcon
from PyQt5.QtCore import pyqtSlot, Qt, QRunnable, QThreadPool
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyle, QPushButton
import re, os

import time
from data_manager.tooltips_req import tooltips_req
from components.reduce_path_string import reduce_path_string
from dialogs.dialog_message import dialog_message


PATTERN_REQ_REFERENCE = re.compile(r"""(?:REFERENCE|\$REF:)\s*"(?P<req_reference>[\w\d,/\s\(\)-]+)"\s*""", re.IGNORECASE)

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
        current_baseline = requirement_module.get("current_baseline")

        if path and data:
            r = RequirementFileNode(root_node, path, columns_names, attributes, baseline, coverage_filter, coverage_dict, update_time, ignore_list, notes, current_baseline)
            r.create_tree_from_requirements_data(data, update_time)
            root_node.appendRow(r)  # APPEND NODE AS A CHILD
            r.update_icons_according_to_coverage()
            
        elif not data:
            r = RequirementFileNode(root_node, path, columns_names, attributes, baseline, coverage_filter, coverage_dict, update_time, ignore_list, notes, current_baseline)
            root_node.appendRow(r)  # APPEND NODE AS A CHILD     



# PROJEDE VSECHNY REQUIREMENTY V MODULU (VE STROME), VYTVORI Z NEJ SLOVNIK A ULOZI JE DO SEZNAMU 
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
    def __init__(self, root_node, path, columns_names, attributes, baseline, coverage_filter, coverage_dict, update_time, ignore_list, notes, current_baseline):
        super().__init__()
        self.root_node = root_node
        self.data_manager = self.root_node.data(Qt.UserRole)

        self.path = path
        self.columns_names = columns_names
        # backup original column names, when column names are edited, these backuped columns are used for displying until new Updtate Req is performed
        self.columns_names_backup = [*columns_names]  

        self.timestamp = update_time

        self.setIcon(QIcon(u"ui/icons/doors.png"))

        self.setText(reduce_path_string(self.path))

        self.setEditable(False)

        self.coverage_filter = coverage_filter

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

        self.current_baseline = current_baseline

        self.update_title_text()



    # def file_2_tree(self):
    #     self.root_node.appendRow(self)  # APPEND NODE AS A CHILD
    
    # def update_coverage_dict(self, reference, file_references):
    #     self.coverage_dict.update({reference: file_references})

        


    # VEZME INFORMACE Z COVERAGE SLOVNIKU A DLE NEHO ZOBRAZI TEXT MODULU: POCET POKRYTYCH REQ/CELKOVY POCET REQ (POCITANYCH)
    def update_title_text(self):
        if self.coverage_check:
            number_of_covered_requirements = 0
            number_of_calculated_requirements = 0
            for k, v in self.coverage_dict.items():
                number_of_calculated_requirements += 1
                if v:
                    number_of_covered_requirements += 1
            
            self.setText(reduce_path_string(self.path) + f" ({number_of_covered_requirements}/{number_of_calculated_requirements})")


    # VEZME INFORMACE Z COVERAGE SLOVNIKU A DLE NEHO UPDATUJE JEDNOTLIVE REQUIREMETY
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



    # PROJDE VSECHNY REQUIREMENTY VE STROME A SPUSTI JEJICH METODU UPDATE_COVERAGE (NUTNE POKUD SE OTEVRE PROJEKT !TODO Dat to Initu Requirementu)  
    def update_icons_according_to_coverage(self):
        def browse_children(parent_node, string):                
            for row in range(parent_node.rowCount()):
                requirement_node = parent_node.child(row)
                
                if requirement_node.is_covered is not None:
                    requirement_node.update_coverage(requirement_node.is_covered)

                browse_children(requirement_node, string)                
        browse_children(self, self.coverage_filter)                 




    # NA ZAKLADE SVEHO ARGUMENTU=SLOVNIKU UPDATUJE JEDNOTLIVE REQUIREMENTY VE STROME
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


            

    # FYZICKY PROZKOUMA SOUBORY NA DISKU VYTVORI SLOVNIK KTERY VRATI:       EPBi-Saic-AS23-SyDesign273 : [C:/Path/test.par, C:/Path/test2.par]
    # def create_reference_dict(self, project_path): 
    #     reference_dict = {}       
    #     for root, dirs, files in os.walk(project_path):
    #         for filename in files:
    #             if filename.endswith((".par", ".txt")):
    #                 full_path = (root + '\\' + filename)
    #                 full_path = full_path.replace("\\", "/")
    #                 with open(full_path, 'r') as f:
    #                     text = f.read()

    #                 reference_list = PATTERN_REQ_REFERENCE.findall(text)

    #                 for ref_string in reference_list:
    #                     references = ref_string.split(",")
    #                     for ref in references:
    #                         ref = ref.lower().strip()

    #                         if ref in reference_dict:
    #                             reference_dict[ref].add(full_path)
    #                         else:
    #                             reference_dict.update({ref: set([full_path,])})   

    #     return reference_dict         






         
        







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
            self.update_title_text() 


    def remove_coverage_filter(self):
        self.coverage_dict.clear()
        def browse_children(parent_node):                
            for row in range(parent_node.rowCount()):
                item = parent_node.child(row)
                item.update_coverage(None)                    
                browse_children(item)            
    
        browse_children(self)           
        self.setIcon(QIcon(u"ui/icons/doors.png"))
        self.update_title_text()
        self.coverage_filter = None
        self.coverage_check = False




    ##########################################################################################################################################
    # DOORS DOWNLOADING FINISHED:

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


    #######################################################################################################################################
    #######################################################################################################################################
    #######################################################################################################################################
    #######################################################################################################################################
    #######################################################################################################################################





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
            "current_baseline"  : self.current_baseline,
            "requirements"      : _create_list_of_requirements_from_module(self),
            }

        requirement_modules.append(my_data)  

        return data_from_root      
           


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
                self.coverage_dict.update({reference: file_references})     

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




    def _txtfile_to_tree(self, doors_string):

            last_level = 0

            parents = []

            last_item = self

            # ALL MODULES
            modules_string = re.findall(r"<<<MODULE_START>>>(.*?)<<<MODULE_END>>>", doors_string, re.DOTALL)

            # ONE MODULE
            for one_module_string in modules_string:
                
                # MODULE PATH
                path_match = re.search(r"<PATH_START>(?P<my_group>.*)<PATH_END>", one_module_string, re.DOTALL)
                path = path_match.group("my_group")
                # print(f" MODULE PATH: {path}")
                
                if path == self.path:

                    # MODULE BASELINES
                    baselines = {}
                    baselines_string = re.findall(r"<BASELINE_START>(.*?)<BASELINE_END>", one_module_string, re.DOTALL)
                    for one_baseline_string in baselines_string:
                        # baseline version
                        version_match =  re.search(r"<VERSION_START>(?P<my_group>.*)<VERSION_END>", one_baseline_string)
                        version = version_match.group("my_group")
                        # baseline user
                        user_match =  re.search(r"<USER_START>(?P<my_group>.*)<USER_END>", one_baseline_string)
                        user = user_match.group("my_group")   
                        # baseline date
                        date_match =  re.search(r"<DATE_START>(?P<my_group>.*)<DATE_END>", one_baseline_string)
                        date = date_match.group("my_group")
                        # baseline annotation
                        annotation_match =  re.search(r"<ANNOTATION_START>(?P<my_group>.*)<ANNOTATION_END>", one_baseline_string, re.DOTALL)
                        if annotation_match:
                            annotation = annotation_match.group("my_group")
                        else:
                            annotation = ""

                        baselines.update({version : [user, date, annotation]})

                    # MODULE ATTRIBUTES NAMES
                    attributes = re.findall(r"<ATTRIBUTE_START>(.*?)<ATTRIBUTE_END>", one_module_string, re.DOTALL)
                    # print(attributes)

                    # REQUIREMENTS DATA
                    all_requiremets_string = re.findall(r"<REQUIREMENT_START>(.*?)<REQUIREMENT_END>", one_module_string, re.DOTALL)
                    
                    for one_requirement_string in all_requiremets_string:
                        # requirement identifier
                        identifier_match =  re.search(r"<ID_START>(?P<my_group>.*)<ID_END>", one_requirement_string)
                        identifier = identifier_match.group("my_group")
                        # requirement level
                        level_match =  re.search(r"<LEVEL_START>(?P<my_group>.*)<LEVEL_END>", one_requirement_string)
                        level = int(level_match.group("my_group"))
                        # requirement heading
                        heading_match =  re.search(r"<HEADING_START>(?P<my_group>.*)<HEADING_END>", one_requirement_string)
                        if heading_match:
                            heading = heading_match.group("my_group")
                        else:
                            heading = "" 
                        # requirement columns values
                        columns = re.findall(r"<COLUMN_START>(.*?)<COLUMN_END>", one_requirement_string, re.DOTALL)
                        # requirement outlinks
                        outlinks = re.findall(r"<OUTLINK_START>(.*?)<OUTLINK_END>", one_requirement_string, re.DOTALL)      
                        # requirement inlinks
                        inlinks = re.findall(r"<INLINK_START>(.*?)<INLINK_END>", one_requirement_string, re.DOTALL)  

                        
                        
                        # CREATE REQUIREMENT NODE
                        item = RequirementNode(identifier, heading, level, outlinks, inlinks, None, columns)

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

                        # UPDATE CURRENT REQUIREMENT MODULE
                        self.attributes = attributes 
                        self.baseline = baselines  # TODO: rename to self.baselines



    def tree_2_file(self):
        pass




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

