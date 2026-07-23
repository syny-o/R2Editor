from text_editor.script_formatter import TextFormatter
from text_editor.completion_rules import (
    EQUAL_SPACING_EXCLUDED_COMMANDS,
    SPECIAL_COMMAND_TEMPLATES,
)
from text_editor.text_operations import (
    build_chapter,
    build_command,
    build_testcase,
    cursor_position_after_format,
    graph_variables_before_cursor,
    format_first_assignment,
    leading_whitespace,
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


def key_home_press(text_edit):
    from PyQt5.QtGui import QTextCursor

    cursor = text_edit.textCursor()
    original_position = cursor.position()
    cursor.movePosition(QTextCursor.StartOfLine)

    if original_position == cursor.position() and cursor.block().text() != "":
        cursor.movePosition(QTextCursor.NextWord)
    text_edit.setTextCursor(cursor)


def key_shift_home_press(text_edit):
    from PyQt5.QtGui import QTextCursor

    cursor = text_edit.textCursor()
    cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
    text_edit.setTextCursor(cursor)


def format_text_edit(text_edit):
    if _is_read_only(text_edit):
        return

    from PyQt5.QtGui import QTextCursor

    scroll_bar = text_edit.verticalScrollBar()
    scroll_position = scroll_bar.sliderPosition()
    cursor = text_edit.textCursor()
    cursor_position = cursor.position()
    cursor_anchor = cursor.anchor()

    original_text = text_edit.toPlainText()
    formatted_text = TextFormatter(original_text).run()
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


def indent_dedent_comment(text_edit, variant):
    if _is_read_only(text_edit):
        return

    from PyQt5.QtGui import QTextCursor

    cursor = text_edit.textCursor()
    original_position = cursor.position()
    one_line = len(cursor.selectedText()) == 0

    if one_line:
        cursor.movePosition(QTextCursor.EndOfLine)
        cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)

    selection_start = cursor.selectionStart()
    text = cursor.selectedText()
    transformed_text = transform_indentation(text, variant)
    cursor.insertText(transformed_text)

    if one_line:
        cursor.setPosition(original_position - (len(text) - len(transformed_text)))
    elif original_position == selection_start:
        cursor.setPosition(original_position, QTextCursor.KeepAnchor)
    else:
        cursor.setPosition(selection_start)
        cursor.setPosition(
            original_position - (len(text) - len(transformed_text)),
            QTextCursor.KeepAnchor,
        )

    text_edit.setTextCursor(cursor)


def insert_command(text_edit):
    if _is_read_only(text_edit):
        return

    cursor = text_edit.textCursor()
    cursor.select(cursor.LineUnderCursor)
    cursor.insertText(build_command(cursor.selectedText()))
    text_edit.setTextCursor(cursor)


def insert_testcase(text_edit):
    if _is_read_only(text_edit):
        return

    cursor = text_edit.textCursor()
    cursor.select(cursor.LineUnderCursor)
    cursor.insertText(build_testcase(cursor.selectedText()))
    text_edit.setTextCursor(cursor)


def insert_chapter(text_edit):
    if _is_read_only(text_edit):
        return

    from PyQt5.QtGui import QTextCursor

    cursor = text_edit.textCursor()
    cursor.select(cursor.LineUnderCursor)
    cursor.insertText(build_chapter(cursor.selectedText()))
    cursor.movePosition(QTextCursor.Up)
    cursor.movePosition(QTextCursor.EndOfLine)
    text_edit.setTextCursor(cursor)


def graph_variables_at_cursor(text_edit):
    cursor = text_edit.textCursor()
    return graph_variables_before_cursor(text_edit.toPlainText(), cursor.position())


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
        return False

    from PyQt5.QtGui import QTextCursor

    cursor = text_edit.textCursor()
    line_text = cursor.block().text()
    template = SPECIAL_COMMAND_TEMPLATES.get(line_text.strip())
    if template is None:
        return False

    suffix, cursor_offset = template
    cursor.select(QTextCursor.LineUnderCursor)
    cursor.insertText(line_text + suffix)
    cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, cursor_offset)
    text_edit.setTextCursor(cursor)
    return True
