from text_editor.script_formatter import TextFormatter
from text_editor.command_actions import (
    complete_special_command,
    format_assignment_at_cursor,
    graph_variables_at_cursor,
    insert_chapter,
    insert_command,
    insert_testcase,
)
from text_editor.text_operations import (
    cursor_column_after_transform,
    cursor_position_after_format,
    leading_whitespace,
    smart_home_column,
    transform_indentation,
)


def _is_read_only(text_edit):
    return text_edit.isReadOnly()


def add_new_line_indent(text_edit):
    if _is_read_only(text_edit):
        return

    from PyQt5.QtGui import QTextCursor

    cursor = text_edit.textCursor()
    whitespace = leading_whitespace(cursor.block().text())
    cursor.insertText("\r")
    if cursor.block().text().strip() == "":
        cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
    cursor.insertText(whitespace)
    text_edit.setTextCursor(cursor)

def key_home_press(text_edit, keep_anchor=False):
    from PyQt5.QtGui import QTextCursor

    cursor = text_edit.textCursor()
    target_column = smart_home_column(
        cursor.block().text(),
        cursor.positionInBlock(),
    )
    move_mode = QTextCursor.KeepAnchor if keep_anchor else QTextCursor.MoveAnchor
    cursor.movePosition(QTextCursor.StartOfLine, move_mode)
    cursor.movePosition(QTextCursor.Right, move_mode, target_column)
    text_edit.setTextCursor(cursor)


def format_text_edit(text_edit):
    if _is_read_only(text_edit):
        return

    original_text = text_edit.toPlainText()
    formatted_text = TextFormatter(original_text).run()
    if formatted_text == original_text:
        return

    from PyQt5.QtGui import QTextCursor

    scroll_bar = text_edit.verticalScrollBar()
    scroll_position = scroll_bar.sliderPosition()
    cursor = text_edit.textCursor()
    cursor_position = cursor.position()
    cursor_anchor = cursor.anchor()

    formatted_cursor_position = cursor_position_after_format(
        original_text,
        formatted_text,
        cursor_position,
    )
    formatted_cursor_anchor = cursor_position_after_format(
        original_text,
        formatted_text,
        cursor_anchor,
    )
    document_cursor = text_edit.textCursor()
    document_cursor.select(QTextCursor.Document)
    document_cursor.insertText(formatted_text)

    cursor.setPosition(formatted_cursor_anchor)
    if formatted_cursor_position != formatted_cursor_anchor:
        cursor.setPosition(formatted_cursor_position, QTextCursor.KeepAnchor)
    text_edit.setTextCursor(cursor)
    scroll_bar.setSliderPosition(scroll_position)


def indent_or_dedent(text_edit, operation):
    _transform_lines(text_edit, operation)


def toggle_comment(text_edit):
    _transform_lines(text_edit, 'comment')


def _transform_lines(text_edit, operation):
    if _is_read_only(text_edit):
        return

    from PyQt5.QtGui import QTextCursor

    cursor = text_edit.textCursor()
    original_position = cursor.position()
    has_selection = bool(cursor.selectedText())

    if not has_selection and operation == 'indent':
        cursor.insertText('\t')
        text_edit.setTextCursor(cursor)
        return

    if not has_selection:
        cursor.movePosition(QTextCursor.EndOfLine)
        cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)

    selection_start = cursor.selectionStart()
    text = cursor.selectedText()
    transformed_text = transform_indentation(text, operation)
    cursor.insertText(transformed_text)

    if not has_selection:
        original_column = original_position - selection_start
        transformed_column = cursor_column_after_transform(
            text,
            transformed_text,
            original_column,
        )
        cursor.setPosition(selection_start + transformed_column)
    elif original_position == selection_start:
        cursor.setPosition(original_position, QTextCursor.KeepAnchor)
    else:
        cursor.setPosition(selection_start)
        cursor.setPosition(
            original_position - (len(text) - len(transformed_text)),
            QTextCursor.KeepAnchor,
        )

    text_edit.setTextCursor(cursor)
