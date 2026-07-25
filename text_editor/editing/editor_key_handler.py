from PyQt5.QtCore import Qt

from text_editor.editing import editor_actions


class EditorKeyHandler:
    def __init__(self, editor, completer, completion_controller):
        self.editor = editor
        self.completer = completer
        self.completion_controller = completion_controller

    def handle_basic_editing_key(self, event):
        key = event.key()
        is_enter = key in (Qt.Key_Return, Qt.Key_Enter)

        if key == Qt.Key_Escape:
            cursor = self.editor.textCursor()
            cursor.clearSelection()
            self.editor.setTextCursor(cursor)
            self.completer.popup().hide()
            self.completion_controller.clear_pending_special_char()
            return True

        if is_enter and self.completer.popup().isVisible():
            selected_completion = self.completer.get_selected()
            if selected_completion:
                self.completer.insert_text.emit(selected_completion)
                return True
            self.completer.popup().hide()

        if is_enter:
            editor_actions.add_new_line_indent(self.editor)
            return True

        if key == Qt.Key_Backtab:
            editor_actions.indent_or_dedent(self.editor, 'dedent')
            return True

        if key == Qt.Key_Tab:
            editor_actions.indent_or_dedent(self.editor, 'indent')
            return True

        if event.modifiers() & Qt.ShiftModifier and key == Qt.Key_Home:
            editor_actions.key_home_press(
                self.editor,
                keep_anchor=True,
            )
            return True

        if key == Qt.Key_Home:
            editor_actions.key_home_press(self.editor)
            return True

        if key == Qt.Key_Equal and self.completer.context_name == 'values':
            self.editor.textCursor().insertText('=')
            self.completer.show_popup('')
            return True

        return False
