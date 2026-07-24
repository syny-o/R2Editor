from data_manager.forms.form_a2l_norm_report import A2lNormReport
from data_manager.nodes.a2l_nodes import A2lFileNode


class A2lActions:
    def __init__(self, manager):
        self.manager = manager
        self.report_form = None

    def normalize_selected_file(self):
        selected_index = self.manager.TREE.currentIndex()
        selected_item = self.manager.MODEL.itemFromIndex(selected_index)
        if not isinstance(selected_item, A2lFileNode):
            return

        selected_item.normalise_file()
        self.manager.send_data_2_completer()
        self.manager.set_project_saved(True)

    def show_normalization_report(
        self,
        report_data,
        missing_signals,
        duplicated_signals,
    ):
        self.report_form = A2lNormReport(
            report_data,
            missing_signals,
            duplicated_signals,
        )
        self.report_form.show()
