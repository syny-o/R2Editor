from PyQt5.QtWidgets import QPlainTextEdit, QToolTip

from text_editor.code_editor import CodeEditor
from text_editor import editor_actions

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QTextCursor, QPalette, QColor


from config.font import font

from text_editor.completer import Completer
from text_editor.completion_rules import completion_model_name
from text_editor.file_access import is_file_read_only
from components.text_functions import get_word_under_cursor
from text_editor.text_operations import completion_context

from components.syntax_highlighter.i_syntax_highlighter import ISyntaxHighlighter

class TextEdit(CodeEditor):

    # SIGNAL FOR HANDLING PRESSING MOUSE AT TEXTEDIT
    signal_clicked_on_text_edit = pyqtSignal(object)
    signal_modified_file_content = pyqtSignal(object, bool)
    signal_scroll_position_changed = pyqtSignal(object, int)

    
    def __init__(self, text, file_path, syntax_highlighter: ISyntaxHighlighter, dark_mode=False):
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
        


        # DEFINE TEXT EDIT BEHAVIOR
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.setTabStopDistance(14)
        self.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.setReadOnly(is_file_read_only(self.file_path))


        self.document().modificationChanged.connect(self._on_modification_changed)
        self.document().setModified(False)
        # CONNECT COMPLETER - INSTANCE CONFIGURATION
        self.completer = Completer(self)
        self.completer.setWidget(self)
        self.completer.insert_text.connect(self.insert_completion)
        self.current_model = None




        self.remember_special_char = False


    def update_syntax_highlighter(self, syntax_highlighter: ISyntaxHighlighter, dark_mode):
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
        cursor = self.textCursor()
        actual_text = completion_context(
            cursor.block().text(),
            cursor.positionInBlock(),
            cursor.hasSelection(),
        )
        condition_names = self.completer.cond_dict if self.completer.cond_model else ()
        model_name = completion_model_name(actual_text, condition_names)
        graph_variables = ()
        if model_name == 'graph_variables':
            graph_variables = editor_actions.graph_variables_at_cursor(self)

        self.current_model = self.completer.set_context_model(
            model_name,
            actual_text=actual_text,
            graph_variables=graph_variables,
        )

########################################################################################################################
# KEYS MANAGEMENT
########################################################################################################################

    def keyReleaseEvent(self, event):
        self.signal_clicked_on_text_edit.emit(self)
        self.update_completion_context()
        if event.key() not in (Qt.Key_Up, Qt.Key_Down):
            self.completer.completer_tooltip.hide_tooltip()
        return super().keyReleaseEvent(event)

    def _handle_basic_editing_key(self, event):
        key = event.key()

        if key == Qt.Key_Escape:
            cursor = self.textCursor()
            cursor.clearSelection()
            self.setTextCursor(cursor)

        if key == Qt.Key_Return and self.completer.popup().isVisible():
            self.completer.insert_text.emit(self.completer.get_selected())
            return True

        if key == Qt.Key_Return:
            editor_actions.add_new_line_indent(self)
            return True

        if key == Qt.Key_Backtab:
            editor_actions.indent_dedent_comment(self, variant='dedent')
            return True

        if key == Qt.Key_Tab:
            editor_actions.indent_dedent_comment(self, variant='indent')
            return True

        if event.modifiers() & Qt.ShiftModifier and key == Qt.Key_Home:
            editor_actions.key_shift_home_press(self)
            return True

        if key == Qt.Key_Home:
            editor_actions.key_home_press(self)
            return True

        if key == Qt.Key_Equal and self.current_model == 'values':
            self.textCursor().insertText('=')
            self.show_popup('')
            return True

        return False

    def _show_completion_for_cursor(self, cursor, empty_prefix_models):
        selected_text = cursor.selectedText()
        if (
            not selected_text
            and (
                not cursor.block().text().strip()
                or self.current_model in empty_prefix_models
            )
        ):
            self.show_popup("")
            return

        special_prefixes = {
            '"': (' "', 2),
            ',': (' ,', 2),
            ')': (' )"', 3),
        }
        for prefix, (replacement, move_left) in special_prefixes.items():
            if selected_text.startswith(prefix):
                self.remember_special_char = True
                cursor.insertText(replacement)
                cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, move_left)
                self.setTextCursor(cursor)
                cursor.select(QTextCursor.WordUnderCursor)
                self.show_popup(cursor.selectedText())
                return

        if selected_text:
            self.show_popup(selected_text)
        else:
            self.completer.popup().hide()

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
        QToolTip.hideText()

        if self._handle_basic_editing_key(event):
            return
        if self._handle_visible_completion(event):
            return
        if self._handle_alt_completion(event):
            return

        if event.key() not in (Qt.Key_Up, Qt.Key_Down, Qt.Key_Return):
            self.completer.popup().hide()

        super().keyPressEvent(event)



########################################################################################################################
# COMPLETION MANAGEMENT
########################################################################################################################


    def insert_completion(self, completion):
        tc = self.textCursor()
        get_word_under_cursor(tc)
        tc.insertText(completion)

        if self.remember_special_char:
            self.remember_special_char = False
            tc.deleteChar()
        self.setTextCursor(tc)

        editor_actions.format_assignment_at_cursor(self)
        if editor_actions.complete_special_command(self):
            self.completer.popup().hide()
        if not QToolTip.isVisible():
            self.completer.popup().hide()



    def show_popup(self, completion_prefix):
        self.completer.setCompletionPrefix(completion_prefix)
        cr = self.cursorRect()
        self.completer.popup().setCurrentIndex(self.completer.completionModel().index(0, 0)) # automatically select first popup item
        cr.setWidth(self.completer.popup().sizeHintForColumn(0)
                    + self.completer.popup().verticalScrollBar().sizeHint().width() + 20)
        self.completer.complete(cr)
