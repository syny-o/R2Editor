from pathlib import Path

from PyQt5.QtWidgets import QFileDialog

from data_manager import tree_walker
from data_manager.forms.form_validate_html_report import (
    FormValidatedHTMLReport,
)
from data_manager.html_report_checker import classify_references
from data_manager.nodes.requirement_module import RequirementModule
from dialogs.dialog_message import dialog_message


class HtmlReportController:
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def check_report(self):
        manager = self.data_manager
        path, _ = QFileDialog.getOpenFileName(
            parent=manager,
            caption='Open HTML Report',
            directory=manager.PROJECT_MANAGER.disk_project_path(),
            filter='*.html',
        )
        if not path:
            return

        try:
            html_report = Path(path).read_text()
        except Exception as exception:
            dialog_message(manager, str(exception))
            return

        references = []
        for row in range(manager.ROOT.rowCount()):
            module = manager.ROOT.child(row)
            if (
                isinstance(module, RequirementModule)
                and module.coverage_filter
            ):
                references.extend(module.coverage_dict.keys())

        missing_requirements, _ = classify_references(
            html_report,
            references,
        )
        manager.form = FormValidatedHTMLReport(
            manager,
            missing_requirements,
        )

    def go_to_requirement(self, identifier):
        manager = self.data_manager
        for row in range(manager.ROOT.rowCount()):
            module = manager.ROOT.child(row)
            if not (
                isinstance(module, RequirementModule)
                and module.coverage_filter
            ):
                continue
            found_node = tree_walker.find_node_by_identifier(
                module,
                identifier,
            )
            if found_node:
                manager.TREE.setCurrentIndex(found_node.index())
                manager.TREE.scrollTo(found_node.index())
                return
