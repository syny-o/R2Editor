from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem

from components.reduce_path_string import reduce_path_string
from config import constants
from data_manager.coverage.data import (
    coverage_counts,
    covered_references,
    normalize_ignored_references,
    normalize_requirement_notes,
    uncovered_references,
)
from data_manager.requirements import (
    module_coverage,
    module_tree,
    module_updater,
)
from data_manager.requirements.tree_builder import iter_descendants


class RequirementModule(QStandardItem):
    def __init__(
        self,
        root_node,
        path,
        columns_names,
        attributes,
        baseline,
        coverage_filter,
        coverage_dict,
        update_time,
        ignore_list,
        notes,
        current_baseline,
        column_number_as_identifier,
    ):
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
        module_coverage.clear_coverage(self)

    def remove_all_scripts_from_coverage_dict(self):
        module_coverage.remove_all_script_references(self)

    def update_script_in_coverage_dict(self, req_id: str, path: str):
        return module_coverage.update_script_reference(self, req_id, path)



    ##########################################################################################################################################
    # PHYSICAL COVERAGE UPDATE ACCORDING TO HDD FILES:

    # UDPATUJE SVUJ COVERAGE SLOVNIK O SEZNAMY SKRIPTU VE KTERYCH JSOU ODKAZY NA REQ ID
    def check_coverage_with_file_pointers(self, reference_dict: dict[str, set]):
        return module_coverage.check_coverage_with_file_pointers(
            self,
            reference_dict,
        )
    


    ##########################################################################################################################################
    # COVERAGE FILTER:

    def translate_filter(self, filter_string):
        return module_coverage.translate_filter(self, filter_string)


    def apply_coverage_filter(self, filter_string=None):
        return module_coverage.apply_coverage_filter(self, filter_string)



    def remove_ignored_items_which_does_not_meet_filter(
        self,
        ignored_items_which_does_not_meet_filter: list[str],
    ):
        return module_coverage.remove_invalid_ignored_references(
            self,
            ignored_items_which_does_not_meet_filter,
        )


    def remove_coverage_filter(self):
        module_coverage.remove_coverage_filter(self)
        




    ##########################################################################################################################################
    # DOORS DOWNLOADING FINISHED:

    def receive_data_from_doors(self, doors_output, timestamp):
        return module_updater.update_module_from_doors(
            self,
            doors_output,
            timestamp,
        )


    def validate_doors_output(self, doors_output: str) -> tuple[bool, str]:                   
        return module_updater.validate_doors_output(self, doors_output)
    
    

    #######################################################################################################################################
    #######################################################################################################################################
    #######################################################################################################################################



    # PRI OTEVIRANI PROJEKTU
    def create_tree_from_requirements_data(self, req_list, timestamp):
        module_tree.create_tree_from_project_data(self, req_list, timestamp)



    # PRI STAHOVANI DAT Z DOORS A NASLEDNEHO OTEVRENI TXT SOUBORU (doors_output.txt)
    def _txtfile_to_tree(self, doors_string):
        module_tree.populate_tree_from_doors(self, doors_string)



    def _create_requirement(self, one_requirement_string: str) -> list[dict]:
        return module_tree.create_requirement_node(
            self,
            one_requirement_string,
        )



    # PRI UKLADANI PROJEKTU
    def data_4_project(self, data_from_root):        
        return module_tree.append_module_to_project_data(
            self,
            data_from_root,
        )

