from components.pyqt_find_text_widget.findReplaceTextWidget import (
    FindReplaceTextWidget,
)
from config.font import font
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
from text_editor.editing import editor_actions


class EditorController:
    def __init__(self, main_window):
        self.main_window = main_window
        self.find_box = None

    def connect_actions(self, document_actions):
        window = self.main_window

        window.btn_script_new.clicked.connect(document_actions.new)
        window.btn_script_new.setShortcut('Ctrl+n')
        window.btn_script_open.clicked.connect(document_actions.open_from_dialog)
        window.btn_script_save.clicked.connect(document_actions.save)
        window.btn_script_save.setShortcut('Ctrl+s')
        window.btn_script_save_as.clicked.connect(document_actions.save_as)
        window.btn_lock_unlock.clicked.connect(
            document_actions.toggle_read_only
        )

        editor_buttons = (
            (
                window.btn_insert_chapter,
                self.insert_chapter,
                'Ctrl+Shift+a',
                'Chapter (Ctrl+Shift+A)',
            ),
            (
                window.btn_insert_testcase,
                self.insert_testcase,
                'Ctrl+Shift+t',
                'Testcase (Ctrl+Shift+T)',
            ),
            (
                window.btn_insert_command,
                self.insert_command,
                'Ctrl+Shift+c',
                'Command (Ctrl+Shift+C)',
            ),
            (
                window.btn_comment_uncomment,
                self.toggle_comment,
                'Ctrl+/',
                '(Un)Comment (Ctrl+"/")',
            ),
            (
                window.btn_format_code,
                self.format_code,
                'Ctrl+Shift+f',
                'Format Code (Ctrl+Shift+F)',
            ),
        )
        for button, action, shortcut, tooltip in editor_buttons:
            button.clicked.connect(action)
            button.setShortcut(shortcut)
            button.setToolTip(tooltip)

        zoom_buttons = (
            (
                window.btn_zoom_in,
                self.font_increase,
                QKeySequence(Qt.CTRL + Qt.Key_Plus),
                'Zoom In (Ctrl+Plus)',
            ),
            (
                window.btn_zoom_out,
                self.font_decrease,
                QKeySequence(Qt.CTRL + Qt.Key_Minus),
                'Zoom Out (Ctrl+Minus)',
            ),
            (
                window.btn_zoom_default,
                self.font_reset,
                QKeySequence(Qt.CTRL + Qt.Key_0),
                'Reset Zoom (Ctrl+0)',
            ),
        )
        for button, action, shortcut, tooltip in zoom_buttons:
            button.clicked.connect(action)
            button.setShortcut(shortcut)
            button.setToolTip(tooltip)

        QShortcut('Ctrl+f', window).activated.connect(
            lambda: self.show_find_replace(only_find=True)
        )
        QShortcut('Ctrl+h', window).activated.connect(
            lambda: self.show_find_replace(only_find=False)
        )

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
