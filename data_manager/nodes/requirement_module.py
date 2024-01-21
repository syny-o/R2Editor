import re
from PyQt5.QtWidgets import QPushButton, QStyle
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QIcon, QColor, QStandardItem
from data_manager.nodes.requirement_node import RequirementNode
from components.reduce_path_string import reduce_path_string
from data_manager import constants

# PATTERN_REQ_REFERENCE = re.compile(r"""(?:REFERENCE|\$REF:)\s*"(?P<req_reference>[\w\d,/\s\(\)-]+)"\s*""", re.IGNORECASE)
# PATTERN_REQ_REFERENCE = re.compile(r'(?:REFERENCE|\$REF:)\s*"(?P<req_reference>.+)"\s*\$', re.IGNORECASE)
# PATTERN_REQ_DETERMINE = re.compile(r"the (component|safety mechanism) shall determine '(?P<keyword>[\w]+)'", re.IGNORECASE)
# PATTERN_CONSTANT = re.compile(r"^[A-Z0-9_]+$")

# from my_logging import logger
# logger.debug(f"{__name__} --> Init")


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
            r = RequirementModule(root_node, path, columns_names, attributes, baseline, coverage_filter, coverage_dict, update_time, ignore_list, notes, current_baseline)
            r.create_tree_from_requirements_data(data, update_time)
            root_node.appendRow(r)  # APPEND NODE AS A CHILD
            r.update_icons_according_to_coverage()
            
        elif not data:
            r = RequirementModule(root_node, path, columns_names, attributes, baseline, coverage_filter, coverage_dict, update_time, ignore_list, notes, current_baseline)
            root_node.appendRow(r)  # APPEND NODE AS A CHILD     



# Helper functions for extracting data from doors_output.txt
def extract_attributes(string: str) -> list[str]:
    return re.findall(r"<ATTRIBUTE_START>(.*?)<ATTRIBUTE_END>", string, re.DOTALL)

def extract_baselines(string: str) -> dict[str, list[str, str, str]]:
    baselines = {}
    baselines_string = re.findall(r"<BASELINE_START>(.*?)<BASELINE_END>", string, re.DOTALL)
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
    return baselines   # { "1.0" : ["user", "date", "annotation"] }


  




class RequirementModule(QStandardItem):
    def __init__(self, root_node, path, columns_names, attributes, baseline, coverage_filter, coverage_dict, update_time, ignore_list, notes, current_baseline):
        super().__init__()
        self.root_node = root_node
        self.data_manager = self.root_node.data(Qt.UserRole)

        self.ICON_DOORS = QIcon(u"ui/icons/doors.png")
        # self.ICON_NOT_COVERED = QIcon(u"ui/icons/cross.png")
        self.ICON_NOT_COVERED = QPushButton().style().standardIcon(QStyle.SP_DialogCancelButton)
        self.ICON_COVERED = QIcon(u"ui/icons/check.png")
        self.ICON_NONE = QIcon()  

        self.path = path
        self.columns_names = columns_names
        self.coverage_filter = coverage_filter        
        self.timestamp = update_time
        self.ignore_list = set(ignore_list) if ignore_list else set()
        self.attributes = attributes or []
        self.baseline = baseline or {}
        self.notes = notes or {}
        self._coverage_dict = coverage_dict or {}
        self.current_baseline = current_baseline        
        
        self.setIcon(self.ICON_DOORS)
        self.setText(reduce_path_string(self.path))
        self.setEditable(False)
        self.setForeground(QColor(200, 200, 200)) 
        self.view_filter = constants.ViewCoverageFilter.ALL    
        self.columns_names_backup = [*columns_names] 
        self.current_baseline_backup = current_baseline

        self.update_title_text()

 


    @property
    def number_of_covered_requirements(self):
        count = 0
        for v in self._coverage_dict.values():
            if v:
                count += 1
        return count


    @property
    def number_of_calculated_requirements(self):
        return len(self._coverage_dict)

    
    @property
    def number_of_ignored_requirements(self):
        return len(self.ignore_list)
    

    @property
    def covered_requirements(self):
        return [k for k, v in self._coverage_dict.items() if v]
    
    @property
    def not_covered_requirements(self):
        return [k for k, v in self._coverage_dict.items() if not v]
    
    @property
    def ignored_requirements(self):
        return list(self.ignore_list)
    


    # VEZME INFORMACE Z COVERAGE SLOVNIKU A DLE NEHO ZOBRAZI TEXT MODULU: POCET POKRYTYCH REQ/CELKOVY POCET REQ (POCITANYCH)
    def update_title_text(self):
        if self.coverage_filter:            
            self.setText(reduce_path_string(self.path) + f" ({self.number_of_covered_requirements}/{self.number_of_calculated_requirements})")
        else:
            self.setText(reduce_path_string(self.path))


    # PROJDE VSECHNY REQUIREMENTY VE STROME A UPDATUJE JEJICH IKONU DLE COVERAGE SLOVNIKU
    def update_icons_according_to_coverage(self):
        def browse_children(parent_node):                
            for row in range(parent_node.rowCount()):
                requirement_node = parent_node.child(row)
                requirement_node.update_icon()                
                browse_children(requirement_node)                
        browse_children(self)    




    ##########################################################################################################################################
    # COVERAGE DICTIONARY:


    @property
    def coverage_dict(self):
        return self._coverage_dict

    def clear_coverage_dict(self):
        self._coverage_dict.clear()

    def remove_all_scripts_from_coverage_dict(self):
        for v in self._coverage_dict.values():
            v.clear()          

    def update_script_in_coverage_dict(self, req_id: str, path: str):
        if req_id.lower() in self._coverage_dict:
            paths = self._coverage_dict[req_id.lower()]

            before = len(paths)

            if path in paths:
                paths.remove(path)
            else:
                paths.append(path)

            after = len(paths)



            if before != after:
                self.update_icons_according_to_coverage()
                self.update_title_text()
                
                return True






    ##########################################################################################################################################
    # PHYSICAL COVERAGE UPDATE ACCORDING TO HDD FILES:

    # UDPATUJE SVUJ COVERAGE SLOVNIK O SEZNAMY SKRIPTU VE KTERYCH JSOU ODKAZY NA REQ ID
    def check_coverage_with_file_pointers(self, reference_dict: dict[str, set]):
        "{ 'epbi-ford-ge2_my24sydesign_7534' : { 'C:/!!! Projects/Ford_GE2_MY24/test.par', 'C:/!!! Projects/Ford_GE2_MY24/test2.par' } }"

        coverage_dict_before = self.coverage_dict.copy()
        # 0. vytvorit znovu slovnik na zaklade Coverage Filtru
        self.apply_coverage_filter()  # !TODO Validate if it is ok
        # 1. odebrat vsechny skripty ze slovniku
        # self.remove_all_scripts_from_coverage_dict()
        # 2. znovu naplnit slovnik skriptama dle aktualni situace na disku
        for req_identifier, set_of_script_paths in reference_dict.items():
            typo = req_identifier.replace("sydesign", "-sydesign")  # TYPO = WRONGLY WRITTEN REQ IDENTIFIER IN DOORS (MISSING DASH)
            if req_identifier in self._coverage_dict:
                self._coverage_dict[req_identifier] = list(set_of_script_paths)
            if typo in self._coverage_dict:
                self._coverage_dict[typo] = list(set_of_script_paths)

        
        self.update_icons_according_to_coverage()
        self.update_title_text()

        if coverage_dict_before != self._coverage_dict:
            return True
    


    ##########################################################################################################################################
    # COVERAGE FILTER:

    def translate_filter(self, filter_string):
        """ Translates filter string to python code """
        filter_string = filter_string.strip()
        for i in range(len(self.columns_names)):
            filter_string = filter_string.replace(self.columns_names[i], f"column[{i}]")
        return filter_string



    def apply_coverage_filter(self, filter_string=None):
        if filter_string:
            self.coverage_filter = filter_string            

        if self.coverage_filter:

            translated_filter_string = self.translate_filter(self.coverage_filter)

            def browse_children(parent_node, string):                    
                for row in range(parent_node.rowCount()):
                    item = parent_node.child(row)

                    try:
                        column = item.columns_data
                        evaluation = eval(string)
                        
                    except Exception as ex:
                        self.coverage_filter = None
                        raise Exception(f"Wrong Filter: {ex}")

    
                    if evaluation:
                        if item.reference not in self.ignore_list:  # IGNORE LIST CHECK
                            self._coverage_dict.update({item.reference.lower() : []})  # UPDATE COVERAGE DICT

                    browse_children(item, string)                
        
            self._coverage_dict.clear()
            browse_children(self, translated_filter_string)   

            self.update_icons_according_to_coverage()
            self.update_title_text() 



    def remove_coverage_filter(self):
        self._coverage_dict.clear()
        self.coverage_filter = None

        self.update_title_text()
        self.update_icons_according_to_coverage()
        




    ##########################################################################################################################################
    # DOORS DOWNLOADING FINISHED:

    # @pyqtSlot(object)
    def receive_data_from_doors(self, doors_output, timestamp):

        success, message = self.validate_doors_output(doors_output)

        if not success: 
            return False, message

        self.timestamp = timestamp
        # delete all children
        self.removeRows(0, self.rowCount())
        # create new children from received data
        # self.create_tree_from_requirements_data(req_list, timestamp)
        self._txtfile_to_tree(doors_output)
        # once succefull update is performed, update backup columns
        self.columns_names_backup = [*self.columns_names] 
        self.current_baseline_backup = self.current_baseline 
        
        # APPLY FILTER WHICH HAS BEEN APPLIED BEFORE DOWNLOADING
        self.apply_coverage_filter()
        # UPDATE ACCORDING TO COVERAGE DICT WHICH IS STORED IN REQUIREMENT MODULE INDEPENDETLY TO REQUIREMETS NODES
        # self.update_coverage_from_coverage_dict()
        print("REQUIREMENT MODULE UPDATED", self.path)
        return True, ""


    def validate_doors_output(self, doors_output: str) -> tuple[bool, str]:                   
            if self.path not in doors_output:
                return False, f"Failed to download module:\n {self.path}.\n\n Reason:\n Connection issues during downloading or invalid module path!"

            modules = doors_output.split("<PATH_START>")
            for module in modules:
                if self.path in module:
                    current_module_string = module
            match = re.search(fr"{self.path}(.+?)<REQUIREMENTS_END>", current_module_string, re.DOTALL)
            if not match:
                # GET AT LEAST BASELINES and ATTRIBUTES 
                self.baseline = extract_baselines(current_module_string)
                self.attributes = extract_attributes(current_module_string)
                return False, f"Failed to download module:\n {self.path}.\n\n Reason:\n Invalid column name!"
            
            return True, "OK"
    
    


    #######################################################################################################################################
    #######################################################################################################################################
    #######################################################################################################################################
    #######################################################################################################################################
    #######################################################################################################################################



    # PRI OTEVIRANI PROJEKTU
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
                self._coverage_dict.update({reference.lower(): file_references})     

            # CREATE REQUIREMENT NODE
            item = RequirementNode(self, reference, heading, level, outlinks, inlinks, file_references, columns_data, is_covered)
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



    # PRI STAHOVANI DAT Z DOORS A NASLEDNEHO OTEVRENI TXT SOUBORU (doors_output.txt)
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
                
                if path == self.path:
                    # MODULE BASELINES
                    self.baseline = extract_baselines(one_module_string)
                    # MODULE ATTRIBUTES NAMES
                    self.attributes = extract_attributes(one_module_string)
                    # REQUIREMENTS DATA
                    all_requiremets_string = re.findall(r"<REQUIREMENT_START>(.*?)<REQUIREMENT_END>", one_module_string, re.DOTALL)
                    
                    for one_requirement_string in all_requiremets_string:
                        requirement_node = self._create_requirement(one_requirement_string)

                        # APPEND TO MODEL
                        if requirement_node.level == last_level:
                            parents[-1].appendRow(requirement_node)

                        elif requirement_node.level > last_level:
                            parents.append(last_item)
                            parents[-1].appendRow(requirement_node)

                        else:
                            dif = last_level - requirement_node.level
                            for _ in range(dif):
                                parents.pop()
                            parents[-1].appendRow(requirement_node)

                        last_level = int(requirement_node.level)   
                        last_item = requirement_node



    def _create_requirement(self, one_requirement_string: str) -> list[dict]:
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
        return RequirementNode(self, identifier, heading, level, outlinks, inlinks, None, columns)                          



    # PRI UKLADANI PROJEKTU
    def data_4_project(self, data_from_root):        
        requirement_modules = data_from_root.get("REQUIREMENT MODULES")
        my_data = {
            "path"              : self.path,
            "columns"           : self.columns_names_backup,
            "attributes"        : self.attributes,
            "baseline"          : self.baseline,
            "update_time"       : self.timestamp,  
            "coverage_filter"   : self.coverage_filter,    
            "coverage_dict"     : self._coverage_dict,
            "ignore_list"       : list(self.ignore_list),
            "notes"             : self.notes,
            "current_baseline"  : self.current_baseline_backup,
            "requirements"      : _create_list_of_requirements_from_module(self),
            }

        requirement_modules.append(my_data)  

        return data_from_root    
        


# PROJEDE VSECHNY REQUIREMENTY V MODULU (VE STROME), VYTVORI Z NEJ SLOVNIK A ULOZI JE DO SEZNAMU --> PRO UKLADANI PROJEKTU
def _create_list_of_requirements_from_module(module: RequirementModule, my_list=None) -> list[dict]:
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

