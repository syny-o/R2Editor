from text_editor.completion.rules import (
    EQUAL_SPACING_EXCLUDED_COMMANDS,
    SPECIAL_COMMAND_TEMPLATES,
)
from text_editor.editing.text_operations import (
    build_chapter,
    build_command,
    build_testcase,
    format_first_assignment,
    graph_variables_before_cursor,
)


def _is_read_only(text_edit):
    return text_edit.isReadOnly()


def insert_command(text_edit):
    cursor = _replace_current_line(text_edit, build_command)
    if cursor is not None:
        text_edit.setTextCursor(cursor)


def insert_testcase(text_edit):
    cursor = _replace_current_line(text_edit, build_testcase)
    if cursor is not None:
        text_edit.setTextCursor(cursor)


def insert_chapter(text_edit):
    cursor = _replace_current_line(text_edit, build_chapter)
    if cursor is None:
        return

    from PyQt5.QtGui import QTextCursor

    cursor.movePosition(QTextCursor.Up)
    cursor.movePosition(QTextCursor.EndOfLine)
    text_edit.setTextCursor(cursor)


def _replace_current_line(text_edit, transform):
    if _is_read_only(text_edit):
        return None

    cursor = text_edit.textCursor()
    cursor.select(cursor.LineUnderCursor)
    cursor.insertText(transform(cursor.selectedText()))
    return cursor


def graph_variables_at_cursor(text_edit):
    cursor = text_edit.textCursor()
    return graph_variables_before_cursor(
        text_edit.toPlainText(),
        cursor.position(),
    )


def format_assignment_at_cursor(text_edit):
    if _is_read_only(text_edit):
        return

    from PyQt5.QtGui import QTextCursor

    cursor = text_edit.textCursor()
    line_text = cursor.block().text()
    formatted_line = format_first_assignment(
        line_text,
        EQUAL_SPACING_EXCLUDED_COMMANDS,
    )
    if formatted_line == line_text:
        return

    cursor.select(QTextCursor.LineUnderCursor)
    cursor.insertText(formatted_line)
    text_edit.setTextCursor(cursor)


def complete_special_command(text_edit):
    if _is_read_only(text_edit):
        return

    from PyQt5.QtGui import QTextCursor

    cursor = text_edit.textCursor()
    line_text = cursor.block().text()
    template = SPECIAL_COMMAND_TEMPLATES.get(line_text.strip())
    if template is None:
        return

    suffix, cursor_offset = template
    cursor.select(QTextCursor.LineUnderCursor)
    cursor.insertText(line_text + suffix)
    cursor.movePosition(
        QTextCursor.Left,
        QTextCursor.MoveAnchor,
        cursor_offset,
    )
    text_edit.setTextCursor(cursor)
