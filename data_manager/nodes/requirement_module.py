from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem
from components.reduce_path_string import reduce_path_string
from config import constants
from data_manager.requirements.module_tree import (
    append_module_to_project_data,
    create_requirement_node,
    create_tree_from_project_data,
    populate_tree_from_doors,
)
from data_manager.requirements.module_updater import (
    update_module_from_doors,
    validate_doors_output,
)
from data_manager.coverage.filter import (
    matching_references,
    translate_coverage_filter,
)
from data_manager.coverage.data import (
    apply_file_references,
    coverage_counts,
    covered_references,
    ignored_references_outside_coverage,
    normalize_ignored_references,
    normalize_requirement_notes,
    remove_ignored_references,
    toggle_script_reference,
    uncovered_references,
)
from data_manager.requirements.tree_builder import iter_descendants

class RequirementModule(QStandardItem):
    def __init__(self, root_node, path, columns_names, attributes, baseline, coverage_filter, coverage_dict, update_time, ignore_list, notes, current_baseline, column_number_as_identifier):
        super().__init__()
        self.root_node = root_node
        self.data_manager = self.root_node.data(Qt.UserRole)

        icons = self.data_manager.MAIN.ICON_MANAGER
        self.ICON_DOORS = icons.ICON_REQUIREMENT_MODULE
        self.ICON_NOT_COVERED = icons.ICON_REQUIREMENT_NOT_COVERED
        self.ICON_COVERED = icons.ICON_REQUIREMENT_COVERED
        self.ICON_NONE = icons.ICON_REQUIREMENT_NONE
        self.ICON_IGNORED = icons.ICON_REQUIREMENT_IGNORED

        self.path = path
        self.columns_names = columns_names
        self.coverage_filter = coverage_filter        
        self.timestamp = update_time
        self.ignore_list = normalize_ignored_references(ignore_list)

        self.attributes = attributes or []
        self.baseline = baseline or {}
        self.notes = normalize_requirement_notes(notes)
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
        for requirement_node in iter_descendants(self):
            requirement_node.update_icon()




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
            ignored_items_which_does_not_meet_filter = (
                ignored_references_outside_coverage(
                    self.ignore_list,
                    self._coverage_dict,
                )
            )

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
            remove_ignored_references(
                self.ignore_list,
                self.notes,
                ignored_items_which_does_not_meet_filter,
            )


    def remove_coverage_filter(self):
        self._coverage_dict.clear()
        self.coverage_filter = None

        self.update_title_text()
        self.update_icons_according_to_coverage()
        




    ##########################################################################################################################################
    # DOORS DOWNLOADING FINISHED:

    def receive_data_from_doors(self, doors_output, timestamp):
        return update_module_from_doors(self, doors_output, timestamp)


    def validate_doors_output(self, doors_output: str) -> tuple[bool, str]:                   
        return validate_doors_output(self, doors_output)
    
    

    #######################################################################################################################################
    #######################################################################################################################################
    #######################################################################################################################################



    # PRI OTEVIRANI PROJEKTU
    def create_tree_from_requirements_data(self, req_list, timestamp):
        create_tree_from_project_data(self, req_list, timestamp)



    # PRI STAHOVANI DAT Z DOORS A NASLEDNEHO OTEVRENI TXT SOUBORU (doors_output.txt)
    def _txtfile_to_tree(self, doors_string):
        populate_tree_from_doors(self, doors_string)



    def _create_requirement(self, one_requirement_string: str) -> list[dict]:
        return create_requirement_node(self, one_requirement_string)



    # PRI UKLADANI PROJEKTU
    def data_4_project(self, data_from_root):        
        return append_module_to_project_data(self, data_from_root)

