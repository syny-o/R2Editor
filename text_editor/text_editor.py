from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QPlainTextEdit
from components.syntax_highlighter.i_syntax_highlighter import ISyntaxHighlighter
from components.text_functions import get_word_under_cursor
from config.font import font
from text_editor.code_editor import CodeEditor
from text_editor.completion.completer import Completer
from text_editor.completion.controller import CompletionController
from text_editor.editor_key_handler import EditorKeyHandler
from text_editor.documents.file_access import is_file_read_only


class TextEdit(CodeEditor):
    signal_clicked_on_text_edit = pyqtSignal(object)
    signal_modified_file_content = pyqtSignal(object, bool)
    signal_scroll_position_changed = pyqtSignal(object, int)

    def __init__(
        self,
        text,
        file_path,
        syntax_highlighter: ISyntaxHighlighter,
        dark_mode=False,
    ):
        super().__init__(text)

        slider = self.verticalScrollBar()
        slider.valueChanged.connect(
            lambda value: self.signal_scroll_position_changed.emit(self, value)
        )

        palette = QPalette()
        palette.setColor(QPalette.HighlightedText, QColor("white"))
        palette.setColor(QPalette.Highlight, QColor("blue"))
        self.setPalette(palette)

        self.file_path = file_path
        self.original_file_content = text

        self.update_syntax_highlighter(syntax_highlighter, dark_mode)
        self.setFont(font)

        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.setReadOnly(is_file_read_only(self.file_path))

        self.document().modificationChanged.connect(self._on_modification_changed)
        self.document().setModified(False)

        self.completer = Completer(self)
        self.completer.setWidget(self)
        self.completion_controller = CompletionController(
            self,
            self.completer,
        )
        self.key_handler = EditorKeyHandler(
            self,
            self.completer,
            self.completion_controller,
        )
        self.completer.insert_text.connect(self.insert_completion)
        self.completer.popup_hidden.connect(self._clear_pending_special_char)

    def _clear_pending_special_char(self):
        self.completion_controller.clear_pending_special_char()

    def update_syntax_highlighter(
        self,
        syntax_highlighter: ISyntaxHighlighter,
        dark_mode,
    ):
        self.syntax_highlighter = syntax_highlighter(
            self.document(), dark_mode=dark_mode
        )

    def mouseReleaseEvent(self, event):
        self.signal_clicked_on_text_edit.emit(self)
        self.completer.completer_tooltip.hide_tooltip()
        return super().mouseReleaseEvent(event)

    def is_modified(self):
        return self.document().isModified()

    def _on_modification_changed(self, is_modified):
        self.signal_modified_file_content.emit(self, is_modified)

    def update_completion_context(self):
        self.completion_controller.update_context()

    def keyReleaseEvent(self, event):
        self.signal_clicked_on_text_edit.emit(self)
        self.update_completion_context()
        if event.key() not in (Qt.Key_Up, Qt.Key_Down):
            self.completer.completer_tooltip.hide_tooltip()
        return super().keyReleaseEvent(event)

    def _handle_basic_editing_key(self, event):
        return self.key_handler.handle_basic_editing_key(event)

    def _show_completion_for_cursor(self, cursor, empty_prefix_models):
        self.completion_controller.show_for_cursor(
            cursor,
            empty_prefix_models,
        )

    def _handle_visible_completion(self, event):
        if not self.completer.popup().isVisible():
            return False
        if event.key() in (Qt.Key_Return, Qt.Key_Equal, Qt.Key_Alt):
            return False

        cursor = self.textCursor()
        super().keyPressEvent(event)
        get_word_under_cursor(cursor)
        self._show_completion_for_cursor(cursor, {"values", "pbc_variables"})
        return True

    def _handle_alt_completion(self, event):
        if event.key() != Qt.Key_Alt:
            return False

        if self.completer.popup().isVisible():
            self.completer.popup().hide()
            return False

        cursor = self.textCursor()
        get_word_under_cursor(cursor)
        self._show_completion_for_cursor(
            cursor, {"values", "pbc_variables", "dspace_variables"}
        )
        return True

    def keyPressEvent(self, event):
        if self.isReadOnly():
            self.completer.popup().hide()
            super().keyPressEvent(event)
            return

        if self._handle_basic_editing_key(event):
            return
        if self._handle_visible_completion(event):
            return
        if self._handle_alt_completion(event):
            return

        if event.key() not in (
            Qt.Key_Up,
            Qt.Key_Down,
            Qt.Key_Return,
            Qt.Key_Enter,
        ):
            self.completer.popup().hide()

        super().keyPressEvent(event)

    def insert_completion(self, completion):
        self.completion_controller.insert(completion)
