from pathlib import Path

from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import QMenu


class FileBrowserContextMenu:
    def __init__(self, browser):
        self.browser = browser

    def show(self, point):
        browser = self.browser
        index = browser.tree.indexAt(point)
        if not index.isValid():
            return

        file_path = index.model().filePath(index)
        suffix = Path(file_path).suffix.lower()
        is_directory = index.model().isDir(index)
        menu = QMenu()

        if is_directory:
            self._add_creation_actions(menu, index)

        rename_action = menu.addAction(
            QIcon('ui/icons/16x16/cil-description.png'),
            'Rename..',
        )
        rename_action.triggered.connect(browser.actions.rename)
        rename_action.setShortcut('F2')

        if is_directory:
            self._add_directory_actions(menu, file_path)

        if suffix in ('.par', '.txt'):
            duplicate_action = menu.addAction(
                QIcon('ui/icons/20x20/cil-copy.png'),
                'Create Copy',
            )
            duplicate_action.triggered.connect(
                lambda: browser.actions.duplicate_script(file_path)
            )

        if suffix in ('.con', '.xml', '.a2l', '.py'):
            menu.addSeparator()
            add_to_model_action = menu.addAction(
                QIcon('ui/icons/16x16/cil-dialpad.png'),
                'Add to Model',
            )
            add_to_model_action.triggered.connect(
                lambda: browser._send_file_to_model(file_path)
            )

        if suffix in ('.par', '.txt') or is_directory:
            menu.addSeparator()
            normalise_action = menu.addAction(
                QIcon('ui/icons/16x16/cil-chart-line.png'),
                'Normalise Script(s)',
            )
            normalise_action.triggered.connect(
                lambda: browser._normalise_script(file_path)
            )

        menu.addSeparator()
        delete_action = menu.addAction(
            QIcon('ui/icons/20x20/cil-trash.png'),
            'Delete',
        )
        delete_action.triggered.connect(browser.actions.delete)
        menu.exec_(QCursor.pos())

    def _add_creation_actions(self, menu, index):
        new_file_action = menu.addAction(
            QIcon('ui/icons/file-new.png'),
            'New File',
        )
        new_file_action.triggered.connect(
            lambda: self.browser.actions.create_file(index)
        )
        new_folder_action = menu.addAction(
            QIcon('ui/icons/folder-new.png'),
            'New Folder',
        )
        new_folder_action.triggered.connect(
            lambda: self.browser.actions.create_folder(index)
        )
        menu.addSeparator()

    def _add_directory_actions(self, menu, file_path):
        menu.addSeparator()
        find_action = menu.addAction(
            QIcon('ui/icons/16x16/cil-magnifying-glass.png'),
            'Find and Replace in Folder',
        )
        find_action.triggered.connect(
            lambda: self.browser._open_find_replace_dialog(file_path)
        )
        menu.addSeparator()
        location_action = menu.addAction(
            QIcon('ui/icons/16x16/cil-layers.png'),
            'Set as Project Location',
        )
        location_action.triggered.connect(
            lambda: self.browser._user_connected_path(file_path)
        )
