from pathlib import Path

from PyQt5.QtWidgets import QInputDialog, QLineEdit, QMessageBox

from dialogs.dialog_message import dialog_message
from file_browser.file_operations import (
    create_document,
    delete_path,
    duplicate_file,
    rename_path,
)


class FileBrowserActions:
    def __init__(self, browser):
        self.browser = browser

    def delete(self):
        browser = self.browser
        index = browser.tree.currentIndex()
        file_path = Path(index.model().filePath(index))
        popup = QMessageBox(browser)
        popup.setIcon(QMessageBox.Question)
        popup.setWindowTitle('Delete File')
        popup.setText(f'Do you really want to delete {file_path}?')
        popup.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        popup.setDefaultButton(QMessageBox.Yes)
        if popup.exec_() == QMessageBox.No:
            return

        try:
            delete_path(file_path)
            for path, (text_edit, tabs) in (
                browser.MAIN.tab_manager.opened_files().items()
            ):
                if path == file_path or file_path in path.parents:
                    tabs.removeTab(tabs.indexOf(text_edit))
        except Exception as exception:
            dialog_message(browser, str(exception))

    def create_folder(self, index):
        name, accepted = QInputDialog.getText(
            self.browser,
            'Create Folder',
            'Name:',
        )
        if accepted and name:
            try:
                self.browser.model.mkdir(index, name)
            except Exception as exception:
                dialog_message(self.browser, str(exception))

    def duplicate_script(self, path):
        try:
            duplicate_path = duplicate_file(path)
            index = self.browser.model.index(str(duplicate_path))
            self.browser.tree.setCurrentIndex(index)
            self.browser.send_file_path.emit(duplicate_path)
        except Exception as exception:
            dialog_message(self.browser, str(exception))

    def rename(self):
        browser = self.browser
        index = browser.tree.currentIndex()
        path = Path(index.model().filePath(index))
        new_name, accepted = QInputDialog.getText(
            browser,
            'Rename',
            'New Name:',
            QLineEdit.Normal,
            path.stem,
        )
        new_name = new_name.strip()
        if not accepted or not new_name:
            return

        try:
            new_path = rename_path(path, new_name)
            browser.tree.setCurrentIndex(browser.model.index(str(new_path)))
            self._update_opened_file_paths(path, new_path)
        except Exception as exception:
            dialog_message(browser, str(exception))

    def create_file(self, index):
        browser = self.browser
        if browser.model.isDir(index):
            parent = browser.model.filePath(index)
            name, accepted = QInputDialog.getText(
                browser,
                'Create File',
                'Name:',
            )
        else:
            parent = browser.model.filePath(index.parent())
            name, accepted = QInputDialog.getText(
                browser,
                'Create File',
                'Name:',
                QLineEdit.Normal,
                index.data(),
            )
        if not accepted or not name:
            return

        candidate = Path(parent) / name
        if not str(candidate).endswith(('.par', '.txt', '.py')):
            candidate = Path(f'{candidate}.par')
        if candidate.exists():
            dialog_message(browser, 'File exists!')
            return

        try:
            file_path = create_document(parent, name)
            browser.tree.setCurrentIndex(browser.model.index(str(file_path)))
            browser.send_file_path.emit(file_path)
            browser.refresh_root_path()
        except Exception as exception:
            dialog_message(browser, f'Error: {exception}')

    def _update_opened_file_paths(self, original_path, renamed_path):
        browser = self.browser
        opened_files = browser.MAIN.tab_manager.opened_files()
        if original_path in opened_files:
            text_edit, tabs = opened_files[original_path]
            text_edit.file_path = renamed_path
            tabs.setTabText(tabs.indexOf(text_edit), renamed_path.name)
            return

        for file_path, (text_edit, _) in opened_files.items():
            if original_path not in file_path.parents:
                continue
            relative_path = file_path.relative_to(original_path)
            text_edit.file_path = renamed_path / relative_path
            browser.MAIN.update_actual_information()
