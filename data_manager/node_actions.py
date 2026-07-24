from PyQt5.QtWidgets import QMessageBox

from data_manager import model_manager
from data_manager.forms.form_edit_node import FormEditNode
from data_manager.forms.form_export_module import FormExportModule
from data_manager.nodes.a2l_nodes import A2lFileNode, A2lNode
from data_manager.nodes.condition_file import ConditionFileNode
from data_manager.nodes.dspace_nodes import (
    DspaceDefinitionNode,
    DspaceFileNode,
)
from data_manager.nodes.requirement_module import RequirementModule
from dialogs.dialog_message import dialog_message


class NodeActions:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.copied_node = None

    def export(self):
        manager = self.data_manager
        selected_item = self._selected_item()
        if isinstance(selected_item, RequirementModule):
            manager.form_export_module = FormExportModule(
                selected_item,
                manager.TREE,
                manager.MODEL,
            )
            manager.form_export_module.show()
            return

        success, message = model_manager.export_file(selected_item)
        if success:
            manager.MAIN.show_notification('File Exported.')
        else:
            dialog_message(manager, message)

    def remove(self):
        manager = self.data_manager
        answer = QMessageBox.question(
            manager,
            'Remove Item',
            'Do you want to remove selected item?',
            QMessageBox.Yes | QMessageBox.No,
        )
        if answer != QMessageBox.Yes:
            return

        result = model_manager.remove_node(manager.TREE, manager.MODEL)
        message = 'Item Removed' if result else 'Item can not be Removed'
        manager.MAIN.show_notification(message)
        manager.send_data_2_completer()
        manager._update_data_summary()
        manager.TREE.setFocus()

    def duplicate(self):
        manager = self.data_manager
        if model_manager.duplicate_node(manager.TREE, manager.MODEL):
            manager.MAIN.show_notification('Item was duplicated.')
            manager.TREE.setFocus()

    def copy(self):
        manager = self.data_manager
        self.copied_node = model_manager.copy_node(
            manager.TREE,
            manager.MODEL,
        )
        if self.copied_node:
            manager.MAIN.show_notification('Item was copied to Clipboard.')
            manager.TREE.setFocus()
            manager.VIEW.action_paste.setEnabled(True)

    def paste(self):
        manager = self.data_manager
        success = model_manager.paste_node(
            manager.TREE,
            manager.MODEL,
            self.copied_node,
        )
        if success:
            manager.MAIN.show_notification(
                f'Item {self.copied_node.text()} was inserted.'
            )
            self.copied_node = None
            manager.send_data_2_completer()
            manager.TREE.setFocus()
            manager.VIEW.action_paste.setEnabled(False)

    def request_edit(self):
        manager = self.data_manager
        selected_item = self._selected_item()
        non_editable_types = (
            ConditionFileNode,
            A2lFileNode,
            A2lNode,
            DspaceFileNode,
            DspaceDefinitionNode,
        )
        if not selected_item or isinstance(selected_item, non_editable_types):
            manager.MAIN.show_notification('Item is not Editable!')
            return

        if (
            isinstance(selected_item, RequirementModule)
            and selected_item in manager._module_locker.locked_modules
        ):
            manager.MAIN.show_notification(
                'Module is being downloaded from Doors. Please wait...'
            )
            return

        manager.form_edit_node = FormEditNode(selected_item, manager)

    def edit_response(self):
        manager = self.data_manager
        manager.MAIN.show_notification('Data Updated')
        manager._update_data_summary()
        manager.set_project_saved(False)
        manager.send_data_2_completer()
        manager.TREE.setFocus()

    def move(self, direction):
        manager = self.data_manager
        model_manager.move_node(manager.TREE, manager.MODEL, direction)
        manager.send_data_2_completer()
        manager.set_project_saved(False)
        manager.TREE.setFocus()

    def _selected_item(self):
        manager = self.data_manager
        return manager.MODEL.itemFromIndex(manager.TREE.currentIndex())
