from PyQt5.QtGui import QTextCursor

from components.text_functions import get_word_under_cursor
from text_editor.editing import command_actions
from text_editor.completion.rules import completion_model_name
from text_editor.editing.text_operations import completion_context


class CompletionController:
    def __init__(self, editor, completer):
        self.editor = editor
        self.completer = completer
        self.delete_special_char_after_completion = False

    def clear_pending_special_char(self):
        self.delete_special_char_after_completion = False

    def update_context(self):
        cursor = self.editor.textCursor()
        actual_text = completion_context(
            cursor.block().text(),
            cursor.positionInBlock(),
            cursor.hasSelection(),
        )
        condition_names = (
            self.completer.cond_dict
            if self.completer.cond_model
            else ()
        )
        model_name = completion_model_name(
            actual_text,
            condition_names,
        )
        graph_variables = ()
        if model_name == 'graph_variables':
            graph_variables = command_actions.graph_variables_at_cursor(
                self.editor
            )

        self.completer.set_context_model(
            model_name,
            actual_text=actual_text,
            graph_variables=graph_variables,
        )

    def show_for_cursor(self, cursor, empty_prefix_models):
        selected_text = cursor.selectedText()
        if (
            not selected_text
            and (
                not cursor.block().text().strip()
                or self.completer.context_name in empty_prefix_models
            )
        ):
            self.completer.show_popup("")
            return

        special_prefixes = {
            '"': (' "', 2),
            ',': (' ,', 2),
            ')': (' )"', 3),
        }
        for prefix, (replacement, move_left) in special_prefixes.items():
            if selected_text.startswith(prefix):
                self.delete_special_char_after_completion = True
                cursor.insertText(replacement)
                cursor.movePosition(
                    QTextCursor.Left,
                    QTextCursor.MoveAnchor,
                    move_left,
                )
                self.editor.setTextCursor(cursor)
                cursor.select(QTextCursor.WordUnderCursor)
                self.completer.show_popup(cursor.selectedText())
                return

        if selected_text:
            self.completer.show_popup(selected_text)
        else:
            self.completer.popup().hide()

    def insert(self, completion):
        cursor = self.editor.textCursor()
        get_word_under_cursor(cursor)
        cursor.insertText(completion)

        if self.delete_special_char_after_completion:
            self.delete_special_char_after_completion = False
            cursor.deleteChar()
        self.editor.setTextCursor(cursor)

        command_actions.format_assignment_at_cursor(self.editor)
        command_actions.complete_special_command(self.editor)
        self.completer.popup().hide()
