from components.pyqt_find_text_widget.findReplaceTextWidget import (
    FindReplaceTextWidget,
)
from config.font import font
from text_editor import editor_actions


class EditorController:
    def __init__(self, main_window):
        self.main_window = main_window
        self.find_box = None

    def insert_command(self):
        self._run_editor_action(editor_actions.insert_command)

    def insert_testcase(self):
        self._run_editor_action(editor_actions.insert_testcase)

    def insert_chapter(self):
        self._run_editor_action(editor_actions.insert_chapter)

    def toggle_comment(self):
        self._run_editor_action(editor_actions.toggle_comment)

    def format_code(self):
        text_edit = self.main_window.actual_text_edit
        if not text_edit:
            return
        try:
            editor_actions.format_text_edit(text_edit)
            text_edit.setFocus()
        except Exception as exception:
            print(str(exception))

    def update_find_replace(self):
        if self.main_window.ui_hLayout_findReplace.count():
            self.show_find_replace(self.find_box.only_find_widget)

    def show_find_replace(self, only_find):
        text_edit = self.main_window.actual_text_edit
        if not text_edit:
            return

        if self.find_box:
            self.main_window.ui_hLayout_findReplace.removeWidget(self.find_box)

        self.find_box = FindReplaceTextWidget(text_edit)
        self.main_window.ui_hLayout_findReplace.addWidget(self.find_box)
        self.find_box.setFocus()
        self.find_box.setOnlyFindTextWidget(only_find)

    def close_find_replace(self):
        if self.find_box:
            self.main_window.ui_hLayout_findReplace.removeWidget(self.find_box)
        text_edit = self.main_window.actual_text_edit
        if text_edit:
            text_edit.setFocus()

    def font_increase(self):
        self.set_font_size(min(font.pointSize() + 1, 20))

    def font_decrease(self):
        self.set_font_size(max(font.pointSize() - 1, 6))

    def font_reset(self):
        self.set_font_size(10)

    def set_font_size(self, point_size):
        font.setPointSize(point_size)
        for text_edit, _ in self.main_window.tab_manager.iter_text_edits():
            text_edit.setFont(font)

    def _run_editor_action(self, action):
        text_edit = self.main_window.actual_text_edit
        if text_edit:
            action(text_edit)
            text_edit.setFocus()
