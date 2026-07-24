from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog

from data_manager import model_manager
from data_manager.nodes import (
    a2l_nodes,
    condition_file,
    dspace_nodes,
)
from data_manager import requirement_module_loader
from data_manager.nodes.condition_file import ConditionFileNode
from data_manager.nodes.dspace_nodes import DspaceFileNode
from dialogs.dialog_message import dialog_message


class ProjectDataController:
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def import_files(self, data):
        manager = self.data_manager
        condition_file.initialise(data, manager.ROOT)
        dspace_nodes.initialise(data, manager.ROOT)
        a2l_nodes.initialise(data, manager.ROOT)
        manager.MAIN.show_notification('Data Updated')
        manager.send_data_2_completer()
        self._select_first_root_item()

    def choose_project_path(self):
        manager = self.data_manager
        folder = QFileDialog.getExistingDirectory(
            manager,
            'Set Project Path',
            '',
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
        )
        if not folder:
            return False

        manager.PROJECT_MANAGER.receive_parameters_from_listeners(
            {'disk_project_path': folder}
        )
        return True

    def set_project_saved(self, is_saved):
        self.data_manager.PROJECT_MANAGER.receive_parameters_from_listeners(
            {'is_project_saved': is_saved}
        )

    def receive_project_data(self, data):
        manager = self.data_manager
        manager.ROOT.removeRows(0, manager.ROOT.rowCount())
        condition_file.initialise(data, manager.ROOT)
        dspace_nodes.initialise(data, manager.ROOT)
        a2l_nodes.initialise(data, manager.ROOT)
        requirement_module_loader.initialise(data, manager.ROOT)
        self._select_first_root_item()
        manager._update_data_summary()
        manager.send_data_2_completer()
        self.set_project_saved(True)

    def receive_project_parameters(self, parameters):
        self.data_manager.ui_lab_project_path.setText(
            parameters['disk_project_path']
        )

    def provide_project_data(self):
        manager = self.data_manager
        data = {
            'Conditions Files': [],
            'DSpace Files': [],
            'A2L Files': [],
            'REQUIREMENT MODULES': [],
        }
        for row in range(manager.ROOT.rowCount()):
            current_node = manager.ROOT.child(row)
            data.update(current_node.data_4_project(data))
            if (
                isinstance(current_node, (ConditionFileNode, DspaceFileNode))
                and current_node.is_modified
            ):
                success, message = model_manager.export_file(current_node)
                if not success:
                    dialog_message(manager, message)
        return data

    def _select_first_root_item(self):
        manager = self.data_manager
        first_item = manager.ROOT.child(0)
        manager.TREE.setCurrentIndex(manager.MODEL.indexFromItem(first_item))
