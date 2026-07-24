from PyQt5.QtWidgets import QPushButton, QStyle, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QStandardItem
from data_manager.nodes.requirement_node import RequirementNode
from components.reduce_path_string import reduce_path_string
from config import constants
from data_manager.doors_output_parser import (
    parse_module_output,
    parse_requirement,
    validate_module_output,
)
from data_manager.requirement_serialization import (
    requirement_module_to_dict,
    requirement_tree_to_list,
    requirements_to_dict,
)
from data_manager.coverage_filter import (
    matching_references,
    translate_coverage_filter,
)
from data_manager.coverage_data import (
    apply_file_references,
    coverage_counts,
    covered_references,
    toggle_script_reference,
    uncovered_references,
)
from data_manager.requirement_tree_builder import append_nodes_by_level

import qtawesome as qta

class RequirementModule(QStandardItem):
    def __init__(self, root_node, path, columns_names, attributes, baseline, coverage_filter, coverage_dict, update_time, ignore_list, notes, current_baseline, column_number_as_identifier):
        super().__init__()
        self.root_node = root_node
        self.data_manager = self.root_node.data(Qt.UserRole)

        self.ICON_DOORS = QIcon(u"ui/icons/doors.png")
        # self.ICON_NOT_COVERED = QIcon(u"ui/icons/cross.png")
        self.ICON_NOT_COVERED = QPushButton().style().standardIcon(QStyle.SP_DialogCancelButton)
        self.ICON_COVERED = QIcon(u"ui/icons/check.png")
        self.ICON_NONE = QIcon()  
        self.ICON_IGNORED = qta.icon('fa5s.eye-slash', color='orange', scale_factor=0.8)

        self.path = path
        self.columns_names = columns_names
        self.coverage_filter = coverage_filter        
        self.timestamp = update_time
        self.ignore_list = set(ignore_list) if ignore_list else set()

        # TODO: Double Check
        self.ignore_list = [item.lower() for item in self.ignore_list]
        self.ignore_list.sort()

        self.attributes = attributes or []
        self.baseline = baseline or {}
        self.notes = notes or {}
        self.notes = {k.lower(): v for k, v in self.notes.items()}
        self._coverage_dict = coverage_dict or {}
        self.current_baseline = current_baseline        
        
        self.setIcon(self.ICON_DOORS)
        self.setText(reduce_path_string(self.path))
        self.setEditable(False)
        self.view_filter = constants.ViewCoverageFilter.ALL    
        self.columns_names_backup = [*columns_names] 
        self.current_baseline_backup = current_baseline

        self.column_number_as_identifier = column_number_as_identifier
        

        self.update_title_text()




    @property
    def number_of_covered_requirements(self):
        covered_count, _ = coverage_counts(self._coverage_dict)
        return covered_count


    @property
    def number_of_calculated_requirements(self):
        _, calculated_count = coverage_counts(self._coverage_dict)
        return calculated_count

    
    @property
    def number_of_ignored_requirements(self):
        return len(self.ignore_list)
    

    @property
    def covered_requirements(self):
        return covered_references(self._coverage_dict)
    
    @property
    def not_covered_requirements(self):
        return uncovered_references(self._coverage_dict)
    
    @property
    def ignored_requirements(self):
        return list(self.ignore_list).sort()
    


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
        changed = toggle_script_reference(
            self._coverage_dict,
            req_id,
            path,
        )
        if changed:
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
        apply_file_references(self._coverage_dict, reference_dict)

        
        self.update_icons_according_to_coverage()
        self.update_title_text()

        if coverage_dict_before != self._coverage_dict:
            return True
    


    ##########################################################################################################################################
    # COVERAGE FILTER:

    def translate_filter(self, filter_string):
        return translate_coverage_filter(filter_string, self.columns_names)


    def apply_coverage_filter(self, filter_string=None):
        if filter_string:
            self.coverage_filter = filter_string            

        if self.coverage_filter:

            translated_filter_string = self.translate_filter(self.coverage_filter)
            self._coverage_dict.clear()
            try:
                references = matching_references(
                    self,
                    translated_filter_string,
                )
            except Exception as ex:
                self.coverage_filter = None
                raise Exception(str(ex))
            self._coverage_dict.update(
                {reference: [] for reference in references}
            )

            # HANDLE IGNORED ITEMS
            # 1a. GATHER ALL IGNORED ITEMS FROM IGNORE LIST WHICH ARE NOT IN COVERAGE DICT (so the filter is not valid anymore for them)
            ignored_items_which_does_not_meet_filter = []
            for ignored_item in self.ignore_list:
                if ignored_item not in self._coverage_dict:
                    ignored_items_which_does_not_meet_filter.append(ignored_item)

            # 1b ASK FOR ITEM REMOVAL
            self.remove_ignored_items_which_does_not_meet_filter(ignored_items_which_does_not_meet_filter)
                    
            # 2. REMOVE IGNORED ITEMS FROM COVERAGE DICT
            for ignored_item in self.ignore_list:
                if ignored_item in self._coverage_dict:
                    self._coverage_dict.pop(ignored_item)


            self.update_icons_according_to_coverage()
            self.update_title_text() 



    def remove_ignored_items_which_does_not_meet_filter(self, ignored_items_which_does_not_meet_filter: list[str]):
        if not ignored_items_which_does_not_meet_filter:
            return
        
        remove_answer = QMessageBox.question(self.data_manager, "Remove ignored items", f"Following items are in ignore list but does not meet coverage filter: \
                                             \n\n{ignored_items_which_does_not_meet_filter}\n\nDo you want to remove them from ignore list?", 
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if remove_answer == QMessageBox.Yes:
            for ignored_item in ignored_items_which_does_not_meet_filter:
                if ignored_item in self.ignore_list:
                    self.ignore_list.remove(ignored_item)
                if ignored_item in self.notes:
                    self.notes.pop(ignored_item)


    def remove_coverage_filter(self):
        self._coverage_dict.clear()
        self.coverage_filter = None

        self.update_title_text()
        self.update_icons_according_to_coverage()
        




    ##########################################################################################################################################
    # DOORS DOWNLOADING FINISHED:

    def receive_data_from_doors(self, doors_output, timestamp):

        columns_changed = self.columns_names_backup != self.columns_names
            
        success, message = self.validate_doors_output(doors_output)

        if not success: 
            return False, message

        # save original data for future comparison
        ORIGINAL_MODULE_DATA = requirements_to_dict(
            requirement_tree_to_list(self)
        )

        self.timestamp = timestamp
        # delete all children
        self.removeRows(0, self.rowCount())
        # create new children from received data
        self._txtfile_to_tree(doors_output)
        # once succefull update is performed, update backup columns / baseline
        self.columns_names_backup = [*self.columns_names] 
        self.current_baseline_backup = self.current_baseline 
        

        # save new data for future comparison
        if ORIGINAL_MODULE_DATA:
            NEW_MODULE_DATA = requirements_to_dict(
                requirement_tree_to_list(self)
            )
        else:
            NEW_MODULE_DATA = {}


        # APPLY FILTER WHICH HAS BEEN APPLIED BEFORE DOWNLOADING
        self.apply_coverage_filter()
        
        if not columns_changed and ORIGINAL_MODULE_DATA and (ORIGINAL_MODULE_DATA != NEW_MODULE_DATA):

            return True, (self.columns_names, ORIGINAL_MODULE_DATA, NEW_MODULE_DATA)
        
        return True, None


    def validate_doors_output(self, doors_output: str) -> tuple[bool, str]:                   
        result = validate_module_output(doors_output, self.path)
        if result['baselines'] is not None:
            self.baseline = result['baselines']
        if result['attributes'] is not None:
            self.attributes = result['attributes']
        return result['success'], result['message']
    
    

    #######################################################################################################################################
    #######################################################################################################################################
    #######################################################################################################################################



    # PRI OTEVIRANI PROJEKTU
    def create_tree_from_requirements_data(self, req_list, timestamp):
        self.timestamp = timestamp

        nodes = []
        for requirement_data in req_list:
            reference = requirement_data.get("reference")
            heading = requirement_data.get("heading")
            file_references = requirement_data.get("file_references")
            is_covered = requirement_data.get("is_covered")

            if is_covered is not None and not heading:
                self._coverage_dict.update(
                    {reference.lower(): file_references}
                )

            nodes.append(
                RequirementNode(
                    self,
                    reference,
                    heading,
                    int(requirement_data.get("level")),
                    requirement_data.get("outlinks"),
                    requirement_data.get("inlinks"),
                    file_references,
                    requirement_data.get("columns_data"),
                    is_covered,
                )
            )

        append_nodes_by_level(self, nodes)



    # PRI STAHOVANI DAT Z DOORS A NASLEDNEHO OTEVRENI TXT SOUBORU (doors_output.txt)
    def _txtfile_to_tree(self, doors_string):
        module_data = parse_module_output(doors_string, self.path)
        if module_data is None:
            return

        self.baseline = module_data["baselines"]
        self.attributes = module_data["attributes"]

        nodes = [
            self._create_requirement(requirement_text)
            for requirement_text in module_data["requirements"]
        ]
        append_nodes_by_level(self, nodes)



    def _create_requirement(self, one_requirement_string: str) -> list[dict]:
        parsed = parse_requirement(
            one_requirement_string,
            self.column_number_as_identifier,
        )
        return RequirementNode(
            self,
            parsed['identifier'],
            parsed['heading'],
            parsed['level'],
            parsed['outlinks'],
            parsed['inlinks'],
            None,
            parsed['columns'],
        )



    # PRI UKLADANI PROJEKTU
    def data_4_project(self, data_from_root):        
        requirement_modules = data_from_root.get("REQUIREMENT MODULES")
        requirement_modules.append(requirement_module_to_dict(self))

        return data_from_root

