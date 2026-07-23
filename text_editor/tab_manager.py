from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox

from text_editor.text_editor import TextEdit


class EditorTabManager:
    def __init__(self, main_window, left_tabs, right_tabs):
        self.main_window = main_window
        self.left_tabs = left_tabs
        self.right_tabs = right_tabs

    def connect_signals(self):
        self.left_tabs.tabCloseRequested.connect(self.left_tab_close_request)
        self.left_tabs.currentChanged.connect(self.left_tab_was_changed)
        self.left_tabs.tabBarClicked.connect(self.left_tab_was_changed)

        self.right_tabs.tabCloseRequested.connect(self.right_tab_close_request)
        self.right_tabs.currentChanged.connect(self.right_tab_was_changed)
        self.right_tabs.tabBarClicked.connect(self.right_tab_was_changed)

    def clicked_on_text_edit(self, text_edit):
        self.main_window.actual_text_edit = text_edit
        self.main_window.actual_tabs = (
            self.right_tabs
            if self.left_tabs.indexOf(text_edit) == -1
            else self.left_tabs
        )
        self.main_window.update_actual_information()

    def left_tab_was_changed(self, tab_index):
        if self.left_tabs.count() > 0:
            self.main_window.actual_tabs = self.left_tabs
            self.main_window.actual_text_edit = self.left_tabs.widget(tab_index)
            self.main_window.actual_text_edit.setFocus()
        self.main_window.update_actual_information()

    def left_tab_close_without_saving(self, tab_index):
        self.left_tabs.removeTab(tab_index)
        if self.left_tabs.count() == 0 and not self.right_tabs.isVisible():
            self.main_window.actual_tabs = None
            self.main_window.actual_text_edit = None
        elif self.left_tabs.count() == 0 and self.right_tabs.isVisible():
            self.main_window.actual_tabs = self.right_tabs
            self.main_window.actual_text_edit = self.right_tabs.currentWidget()
        self.main_window.update_actual_information()

    def left_tab_close_request(self, tab_index):
        self._tab_close_request(
            self.left_tabs,
            tab_index,
            self.left_tab_close_without_saving,
        )

    def right_tab_was_changed(self, tab_index):
        if self.right_tabs.count() > 0:
            self.main_window.actual_tabs = self.right_tabs
            self.main_window.actual_text_edit = self.right_tabs.widget(tab_index)
            self.main_window.actual_text_edit.setFocus()
        self.main_window.update_actual_information()

    def right_tab_close_without_saving(self, tab_index):
        self.right_tabs.removeTab(tab_index)
        if self.right_tabs.count() == 0:
            self.right_tabs.setVisible(False)
            if self.left_tabs.count() > 0:
                self.main_window.actual_text_edit = self.left_tabs.currentWidget()
                self.main_window.actual_tabs = self.left_tabs
            else:
                self.main_window.actual_tabs = None
                self.main_window.actual_text_edit = None

    def right_tab_close_request(self, tab_index):
        self._tab_close_request(
            self.right_tabs,
            tab_index,
            self.right_tab_close_without_saving,
        )

    def _tab_close_request(self, tabs, tab_index, close_tab):
        text_edit = tabs.widget(tab_index)
        if not text_edit.is_modified():
            close_tab(tab_index)
            self.main_window.update_actual_information()
            return

        answer = QMessageBox.question(
            self.main_window,
            'R2 Editor',
            'The file has been modified.\n\nDo you want to save your changes?',
            QMessageBox.Save | QMessageBox.Cancel | QMessageBox.Discard,
            QMessageBox.Save,
        )

        if answer == QMessageBox.Discard:
            close_tab(tab_index)
        elif answer == QMessageBox.Save:
            previous_text_edit = self.main_window.actual_text_edit
            previous_tabs = self.main_window.actual_tabs
            self.main_window.actual_text_edit = text_edit
            self.main_window.actual_tabs = tabs
            was_saved = self.main_window.document_actions.save()
            self.main_window.actual_text_edit = previous_text_edit
            self.main_window.actual_tabs = previous_tabs
            if was_saved:
                close_tab(tab_index)

        self.main_window.update_actual_information()

    def set_tab_modified_icon(self, text_edit, is_modified):
        tabs = self.left_tabs
        tab_index = tabs.indexOf(text_edit)
        if tab_index == -1:
            tabs = self.right_tabs
            tab_index = tabs.indexOf(text_edit)
        if tab_index == -1:
            return

        icon_path = (
            'ui/icons/16x16/cil-description.png'
            if is_modified
            else 'ui/icons/16x16/cil-file.png'
        )
        tabs.setTabIcon(tab_index, QIcon(icon_path))

    def opened_files(self):
        opened_files = {}
        for text_edit, tabs in self.iter_text_edits():
            if text_edit.file_path is not None:
                opened_files[text_edit.file_path] = [text_edit, tabs]
        return opened_files

    def iter_text_edits(self):
        for tabs in (self.left_tabs, self.right_tabs):
            for tab_index in range(tabs.count()):
                yield tabs.widget(tab_index), tabs

    def create_text_edit(self, text, file_path, syntax_highlighter):
        text_edit = TextEdit(
            text,
            file_path,
            syntax_highlighter,
            dark_mode=self.main_window.app_settings.theme == 'Dark',
        )
        text_edit.signal_clicked_on_text_edit.connect(self.clicked_on_text_edit)
        text_edit.signal_modified_file_content.connect(self.set_tab_modified_icon)
        text_edit.signal_scroll_position_changed.connect(
            self.main_window.outline_controller.update_selected_by_scrollbar
        )
        return text_edit
