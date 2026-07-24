from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

from data_manager import tree_walker


class ReferenceNavigator:
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def tooltip_from_link(self, link):
        module_path, identifier = self._split_link(link)
        for row in range(self.data_manager.ROOT.rowCount()):
            module = self.data_manager.ROOT.child(row)
            if module.path == module_path and module.hasChildren():
                first_reference = module.child(0).reference
                prefix = first_reference.split('_')[:-1]
                reference = f'{"_".join(prefix)}_{identifier}'
                found_node = tree_walker.find_node_by_identifier(
                    module,
                    reference,
                )
                return (
                    '\n'.join(found_node.columns_data)
                    if found_node
                    else ''
                )

    def set_item_tooltip(self, item):
        manager = self.data_manager
        identifier = item.data(Qt.UserRole)
        module = manager.MODEL.itemFromIndex(manager.TREE.currentIndex())
        found_node = tree_walker.find_node_by_identifier(module, identifier)
        item.setToolTip(
            '\n'.join(found_node.columns_data) if found_node else ''
        )

    def go_to_identifier(self, item):
        manager = self.data_manager
        module = manager.MODEL.itemFromIndex(manager.TREE.currentIndex())
        identifier = item.data(Qt.UserRole)
        found_node = tree_walker.find_node_by_identifier(module, identifier)
        if found_node:
            self._show_node(found_node)

    def follow_outlink(self, outlink_item):
        manager = self.data_manager
        module_path, reference = self._split_link(
            outlink_item.data(Qt.UserRole)
        )
        if not tree_walker.is_module_present(manager.ROOT, module_path):
            answer = QMessageBox.question(
                manager,
                'Module is missing.',
                f'Module {module_path} is N/A.\n\nDo you want to add it?',
                QMessageBox.Yes | QMessageBox.No,
            )
            if answer == QMessageBox.Yes:
                manager.receive_data_from_add_req_module_dialog(
                    module_path,
                    [],
                )
            return

        found_node = None
        for row in range(manager.ROOT.rowCount()):
            module = manager.ROOT.child(row)
            if module.path == module_path and module.hasChildren():
                full_reference = self._full_reference(module, reference)
                found_node = tree_walker.find_node_by_identifier(
                    module,
                    full_reference,
                )
                break

        if found_node:
            self._show_node(found_node)
        else:
            manager.MAIN.show_notification(
                f'{reference} is not present in {module_path}.'
            )

    def open_script_reference(self, list_item):
        manager = self.data_manager
        file_path = Path(list_item.data(Qt.UserRole))
        manager.send_file_path.emit(file_path)
        manager.MAIN.manage_right_menu(
            manager.MAIN.tabs_splitter,
            manager.MAIN.ui_btn_text_editor,
        )

    def _show_node(self, node):
        tree = self.data_manager.TREE
        tree.setCurrentIndex(node.index())
        tree.scrollTo(node.index())

    @staticmethod
    def _split_link(link):
        parts = link.split(':')
        return parts[0], parts[1]

    @staticmethod
    def _full_reference(module, identifier):
        first_reference = module.child(0).reference
        if '_' not in first_reference:
            return identifier
        prefix = first_reference.split('_')[:-1]
        return f'{"_".join(prefix)}_{identifier}'
