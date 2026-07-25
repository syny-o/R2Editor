from PyQt5.QtWidgets import QMessageBox

from data_manager import tree_walker
from data_manager.coverage.worker import CoverageWorker
from data_manager.nodes.requirement_module import (
    RequirementModule,
    RequirementNode,
)
from dialogs.dialog_message import dialog_message


class CoverageController:
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def script_references_changed(self, references, script_path):
        manager = self.data_manager
        if not manager.PROJECT_MANAGER.disk_project_path():
            return

        for reference in references:
            for row in range(manager.ROOT.rowCount()):
                module = manager.ROOT.child(row)
                if not (
                    isinstance(module, RequirementModule)
                    and module.coverage_filter
                ):
                    continue
                if module.update_script_in_coverage_dict(
                    reference,
                    script_path,
                ):
                    self.update_summary()
                    manager.set_project_saved(False)
                    manager.MAIN.show_notification('Coverage Updated.')

    def start_physical_check(self):
        manager = self.data_manager
        if not tree_walker.at_least_one_module_with_coverage_is_present(
            manager.ROOT
        ):
            dialog_message(
                manager,
                'There are no Requirement Modules with Coverage Filter. '
                'Add at least one.',
            )
            return

        if (
            manager.PROJECT_MANAGER.disk_project_path() is None
            and not manager._set_project_path()
        ):
            return

        manager.uiBtnCheckCoverage.setEnabled(False)
        manager.threadpool.start(CoverageWorker(manager))

    def apply_physical_check(self, file_content_dict):
        manager = self.data_manager
        if not manager.PROJECT_MANAGER.disk_project_path():
            return

        for row in range(manager.ROOT.rowCount()):
            module = manager.ROOT.child(row)
            if (
                isinstance(module, RequirementModule)
                and module.check_coverage_with_file_pointers(
                    file_content_dict
                )
            ):
                manager.set_project_saved(False)
        self.update_summary()
        manager.uiBtnCheckCoverage.setEnabled(True)

    def update_summary(self):
        manager = self.data_manager
        calculated_number = 0
        covered_number = 0
        for row in range(manager.ROOT.rowCount()):
            module = manager.ROOT.child(row)
            if (
                isinstance(module, RequirementModule)
                and module.coverage_filter
            ):
                calculated_number += module.number_of_calculated_requirements
                covered_number += module.number_of_covered_requirements

        manager.ui_lab_req_total.setText(str(calculated_number))
        manager.ui_lab_req_covered.setText(str(covered_number))
        manager.ui_lab_req_not_covered.setText(
            str(calculated_number - covered_number)
        )
        manager.VIEW._update_view()
        manager.widget_chart.set_value(covered_number, calculated_number)

    def add_selected_to_ignore_list(self):
        manager = self.data_manager
        selected_item = manager.MODEL.itemFromIndex(
            manager.TREE.currentIndex()
        )
        if isinstance(selected_item, RequirementNode):
            selected_item.add_to_ignore_list()
            self.update_summary()
            manager.set_project_saved(False)

    def remove_selected_from_ignore_list(self):
        manager = self.data_manager
        selected_item = manager.MODEL.itemFromIndex(
            manager.TREE.currentIndex()
        )
        if not isinstance(selected_item, RequirementNode):
            return

        if selected_item.note:
            answer = QMessageBox.question(
                manager,
                'Remove Note',
                'Do you want to remove note?',
                QMessageBox.Yes | QMessageBox.No,
            )
            selected_item.remove_from_ignore_list(
                answer == QMessageBox.Yes
            )
        else:
            selected_item.remove_from_ignore_list()
        self.update_summary()
        manager.set_project_saved(False)
