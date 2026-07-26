from data_manager.forms.form_add_module import FormAddModule
from data_manager.nodes.requirement_module import RequirementModule


class RequirementModuleActions:
    def __init__(self, manager):
        self.manager = manager
        self.add_module_form = None

    def open_add_form(self):
        self.add_module_form = FormAddModule(self.manager)
        self.add_module_form.show()

    def add_module(self, module_path, column_names):
        module = RequirementModule(
            self.manager.ROOT,
            module_path,
            column_names,
            attributes=[],
            baseline={},
            coverage_filter=None,
            coverage_dict=None,
            update_time=None,
            ignore_list=None,
            notes=None,
            current_baseline=None,
            column_number_as_identifier=None,
        )
        self.manager.ROOT.appendRow(module)
