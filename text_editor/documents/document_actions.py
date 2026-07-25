from pathlib import Path

from PyQt5.QtWidgets import QFileDialog

from components.syntax_highlighter import python_highlighter, rapit_two_highlighter
from components.template_test_case import TemplateTestCase
from config.icon_manager import IconManager
from data_manager.requirement_references import changed_requirement_references
from dialogs.dialog_message import dialog_message
from text_editor.documents.file_access import (
    is_supported_document,
    read_text_file,
    set_file_read_only,
    write_text_file,
)


SCRIPT_FILE_FILTER = 'RapitTwo Script (*.par)'


class DocumentActions:
    def __init__(self, main_window):
        self.main_window = main_window

    def open_from_dialog(self):
        path, _ = QFileDialog.getOpenFileName(
            parent=self.main_window,
            caption='Open Script',
            directory=self.main_window.tree_file_browser.current_path,
            filter=SCRIPT_FILE_FILTER,
        )
        if path:
            self.open_path(Path(path))

    def open_path(self, file_path):
        file_path = Path(file_path)
        try:
            if not is_supported_document(file_path):
                return

            opened_files = self.main_window.tab_manager.opened_files()
            if file_path in opened_files:
                text_edit, tabs = opened_files[file_path]
                tabs.setCurrentWidget(text_edit)
                self.main_window.actual_tabs = tabs
                self.main_window.actual_text_edit = text_edit
                self.main_window.update_actual_information()
                return

            text = read_text_file(file_path)
            syntax_highlighter = (
                python_highlighter.PythonHighlighter
                if file_path.suffix.lower() == '.py'
                else rapit_two_highlighter.RapitTwoHighlighter
            )
            text_edit = self.main_window.tab_manager.create_text_edit(
                text,
                file_path,
                syntax_highlighter,
            )
            self.main_window.left_tabs.addTab(
                text_edit,
                IconManager.editor_document_icon("saved"),
                file_path.name,
            )
        except Exception as exception:
            dialog_message(self.main_window, str(exception))

    def save(self):
        text_edit = self.main_window.actual_text_edit
        if text_edit is None:
            return False

        if (
            self.main_window.app_settings.format_code_when_save
            and text_edit.file_path is not None
            and Path(text_edit.file_path).suffix.lower() in ('.par', '.txt')
        ):
            self.main_window.editor_controller.format_code()

        if text_edit.file_path is None:
            return self.save_as()

        try:
            text_to_save = text_edit.toPlainText()
            write_text_file(text_edit.file_path, text_to_save)
            self._emit_changed_references(
                text_edit.original_file_content,
                text_to_save,
                text_edit.file_path,
            )
            text_edit.original_file_content = text_to_save
            text_edit.document().setModified(False)
            self.main_window.update_actual_information()
            return True
        except Exception as exception:
            dialog_message(self.main_window, str(exception))
            return False

    def save_as(self):
        text_edit = self.main_window.actual_text_edit
        if text_edit is None:
            return False

        path, _ = QFileDialog.getSaveFileName(
            parent=self.main_window,
            caption='Save Script',
            directory=self.main_window.tree_file_browser.current_path,
            filter=SCRIPT_FILE_FILTER,
        )
        if not path:
            return False

        try:
            text_to_save = text_edit.toPlainText()
            write_text_file(path, text_to_save)
            self._emit_changed_references(
                text_edit.original_file_content,
                text_to_save,
                path,
            )
            text_edit.original_file_content = text_to_save
            text_edit.document().setModified(False)
            text_edit.file_path = Path(path)
            text_edit.setReadOnly(False)

            tabs = self.main_window.actual_tabs
            tab_index = tabs.indexOf(text_edit)
            tabs.setTabText(tab_index, Path(path).name)
            self.main_window.update_actual_information()
            return True
        except Exception as exception:
            dialog_message(self.main_window, str(exception))
            return False

    def new(self):
        text = TemplateTestCase().generate_tc_template()
        text_edit = self.main_window.tab_manager.create_text_edit(
            '',
            None,
            rapit_two_highlighter.RapitTwoHighlighter,
        )
        self.main_window.left_tabs.addTab(
            text_edit,
            IconManager.editor_document_icon("modified"),
            'Untitled',
        )
        self.main_window.actual_text_edit.setFocus()
        cursor = self.main_window.actual_text_edit.textCursor()
        cursor.insertText(text)
        self.main_window.actual_text_edit.selectAll()

    def toggle_read_only(self):
        text_edit = self.main_window.actual_text_edit
        if text_edit is None:
            return

        try:
            read_only = not text_edit.isReadOnly()
            set_file_read_only(text_edit.file_path, read_only)
            text_edit.setReadOnly(read_only)
            icon = (
                IconManager().ICON_FILE_LOCKED
                if read_only
                else IconManager().ICON_FILE_UNLOCKED
            )
            self.main_window.btn_lock_unlock.setIcon(icon)
        except TypeError as exception:
            dialog_message(
                self.main_window,
                f'File is not saved! Save the file first. {exception}.',
            )
            text_edit.setFocus()

    def _emit_changed_references(
        self,
        original_text,
        updated_text,
        file_path,
    ):
        references = changed_requirement_references(original_text, updated_text)
        self.main_window.script_requirement_reference_changed.emit(
            references,
            str(Path(file_path)),
        )
