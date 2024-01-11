from dialogs.dialog_message import dialog_message
from PyQt5.Qt import QStandardItem, QIcon
from PyQt5.QtWidgets import QPushButton, QStyle
from PyQt5.QtCore import pyqtSlot, Qt
# from PyQt5.QtGui import QIcon
import re
from pathlib import Path
# from data_manager.tooltips_req import tooltips_req
from components.reduce_path_string import reduce_path_string
# from dialogs.dialog_message import dialog_message


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
            r = RequirementFileNode(root_node, path, columns_names, attributes, baseline, coverage_filter, coverage_dict, update_time, ignore_list, notes, current_baseline)
            r.create_tree_from_requirements_data(data, update_time)
            root_node.appendRow(r)  # APPEND NODE AS A CHILD
            r.update_icons_according_to_coverage()
            
        elif not data:
            r = RequirementFileNode(root_node, path, columns_names, attributes, baseline, coverage_filter, coverage_dict, update_time, ignore_list, notes, current_baseline)
            root_node.appendRow(r)  # APPEND NODE AS A CHILD     











class RequirementFileNode(QStandardItem):
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
        self.view_filter = "all"        
        self.columns_names_backup = [*columns_names]          

        self.update_title_text()

        # print("\n".join(coverage_dict.keys()))
 


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






    def clear_coverage_dict(self):
        self._coverage_dict.clear()

    @property
    def coverage_dict(self):
        return self._coverage_dict


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
    



    def apply_coverage_filter(self, filter_string=None):
        if filter_string:
            self.coverage_filter = filter_string            

        if self.coverage_filter:
            def browse_children(parent_node, string):                    
                for row in range(parent_node.rowCount()):
                    item = parent_node.child(row)

                    try:
                        column = item.columns_data
                        evaluation = eval(string)
                        
                    except Exception as ex:
                        self.coverage_filter = None
                        break
    
                    if evaluation:
                        if item.reference not in self.ignore_list:  # IGNORE LIST CHECK
                            self._coverage_dict.update({item.reference.lower() : []})  # UPDATE COVERAGE DICT

                    browse_children(item, string)                
        
            self._coverage_dict.clear()
            browse_children(self, self.coverage_filter)   

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
            dialog_message(self.data_manager, message)
            return False

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
        # self.update_coverage_from_coverage_dict()
        return True


    def validate_doors_output(self, doors_output: str) -> tuple[bool, str]:                   
            if self.path not in doors_output:
                return False, f"Failed to download module:\n {self.path}.\n\n Reason:\n Connection issues during downloading or invalid module path!"

            modules = doors_output.split("<PATH_START>")
            for module in modules:
                if self.path in module:
                    current_module_string = module
            match = re.search(fr"{self.path}(.+?)<REQUIREMENTS_END>", current_module_string, re.DOTALL)
            if not match:
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
                        item = RequirementNode(self, identifier, heading, level, outlinks, inlinks, None, columns)

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


    # NIC --> POUZIVA SE POUZE U COND/A2L/DSPACE Nodu
    def tree_2_file(self):
        pass



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
            "current_baseline"  : self.current_baseline,
            "requirements"      : _create_list_of_requirements_from_module(self),
            }

        requirement_modules.append(my_data)  

        return data_from_root    
        


# PROJEDE VSECHNY REQUIREMENTY V MODULU (VE STROME), VYTVORI Z NEJ SLOVNIK A ULOZI JE DO SEZNAMU --> PRO UKLADANI PROJEKTU
def _create_list_of_requirements_from_module(module: RequirementFileNode, my_list=None) -> list[dict]:
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









class RequirementNode(QStandardItem):


    def __init__(
        self, 
        module: RequirementFileNode,
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




        self.MODULE = module
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

        self.columns_data = columns_data  # list

        if self.heading:
            self.setText(heading)
        else:
            self.setText(reference)  

        self.node_icon = None      



    @property
    def is_covered(self):
        is_covered = self.MODULE._coverage_dict.get(self.reference.lower(), "Not Calculated")
        if is_covered == "Not Calculated":
            return None
        elif is_covered:
            return True
        else:
            return False

    

    def update_icon(self):        
        if self.is_covered == None:
            self.setIcon(self.MODULE.ICON_NONE)
            self.node_icon = None
        elif self.is_covered:
            self.setIcon(self.MODULE.ICON_COVERED)
            self.node_icon = "green"
        else:
            self.setIcon(self.MODULE.ICON_NOT_COVERED)
            self.node_icon = "red"
        self.update_parents_icons()


    def update_parents_icons(self):
        while not isinstance(self, RequirementFileNode):
            parent = self.parent()
            children = []
            green = False
            red = False
            for row in range(parent.rowCount()):
                children.append(parent.child(row))

            for child in children:
                if child.node_icon == "red":
                    red = True
                elif child.node_icon == "green":
                    green = True

            if red:
                self.parent().setIcon(self.MODULE.ICON_NOT_COVERED)
                self.parent().node_icon = "red"
            elif green:
                self.parent().setIcon(self.MODULE.ICON_COVERED)
                self.parent().node_icon = "green"
            else:
                self.parent().setIcon(self.MODULE.ICON_NONE) if isinstance(self.parent(), RequirementNode) else self.parent().setIcon(self.MODULE.ICON_DOORS)
                self.parent().node_icon = None

            self = self.parent()            

        


        
        
        # if is_covered == "Not Calculated":  # if the requirement is not present in coverage dict
        #     self.is_covered = None
        #     self.setIcon(self.MODULE.ICON_NONE)
        #     for _ in range(self.level):
        #         parent = self.parent()
        #         children = []
        #         for row in range(parent.rowCount()):
        #             children.append(parent.child(row))
        #         children_none = True
        #         for child in children:
        #             if child.is_covered is not None:
        #                 children_none =  False

        #         if children_none:
        #             self.parent().setIcon(self.MODULE.ICON_NONE) if isinstance(self.parent(), RequirementNode) else self.parent().setIcon(self.MODULE.ICON_DOORS)
        #             self.parent().is_covered = None
        #         if not isinstance(self, RequirementFileNode):
        #             self = self.parent()   

        # else:
        #     if is_covered:  # if the requirements HAS file references
        #         self.is_covered = True
        #         self.setIcon(self.MODULE.ICON_COVERED)
        #         for _ in range(self.level):
        #             parent = self.parent()
        #             children = []
        #             for row in range(parent.rowCount()):
        #                 children.append(parent.child(row))
        #             children_covered = True
        #             for child in children:
        #                 if child.is_covered == False:
        #                     children_covered =  False

        #             if children_covered:
        #                 self.parent().setIcon(self.MODULE.ICON_COVERED)
        #                 self.parent().is_covered = True
        #             if not isinstance(self, RequirementFileNode):
        #                 self = self.parent()

        #     if not is_covered:  # if the requirements HAS NO file references
        #         self.is_covered = False
        #         self.setIcon(self.MODULE.ICON_NOT_COVERED)
        #         for _ in range(self.level):
        #             self.parent().setIcon(self.MODULE.ICON_NOT_COVERED)
        #             self.parent().is_covered = False
        #             if not isinstance(self, RequirementFileNode):
        #                 self = self.parent()





    @property
    def file_references(self):
        file_references = self.MODULE._coverage_dict.get(self.reference.lower(), [])
        return file_references          







    def add_to_ignore_list(self):
        if not self.hasChildren():  # if it is not Heading
            # self.update_coverage(None)
            self.MODULE._coverage_dict.pop(self.reference.lower())
            self.MODULE.ignore_list.add(self.reference)
            self.update_icon()

    def remove_from_ignore_list(self):
        if not self.hasChildren():  # if it is not Heading
            if self.reference in self.MODULE.ignore_list:            
                # self.update_coverage(False)
                self.MODULE.ignore_list.remove(self.reference)   
                self.MODULE._coverage_dict.update({self.reference.lower() : []})
                self.update_icon()






    # def update_note(self, text):
    #     if text.strip() != "":
    #         self.MODULE.notes.update({self.reference: text})
    #     else:     
    #         self.MODULE.notes.pop(self.reference, None)

    # def get_note(self):
    #     return self.MODULE.notes.get(self.reference, "")

    @property
    def note(self) -> str:
        return self.MODULE.notes.get(self.reference, "")

    @note.setter
    def note(self, text: str) -> None:
        if text.strip() != "":
            self.MODULE.notes.update({self.reference: text})
        else:     
            self.MODULE.notes.pop(self.reference, None)

