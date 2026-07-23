from text_editor.script_formatter import TextFormatter
from text_editor.text_operations import (
    build_chapter,
    build_command,
    build_testcase,
    graph_variables_before_cursor,
    leading_whitespace,
    transform_indentation,
)


def add_new_line_indent(text_edit):
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
    from PyQt5.QtGui import QTextCursor

    scroll_bar = text_edit.verticalScrollBar()
    scroll_position = scroll_bar.sliderPosition()
    cursor = text_edit.textCursor()
    cursor_position = cursor.position()

    formatted_text = TextFormatter(text_edit.toPlainText()).run()
    document_cursor = text_edit.textCursor()
    document_cursor.select(QTextCursor.Document)
    document_cursor.insertText(formatted_text)

    cursor.setPosition(min(cursor_position, len(formatted_text)))
    text_edit.setTextCursor(cursor)
    scroll_bar.setSliderPosition(scroll_position)


def indent_dedent_comment(text_edit, variant):
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
    cursor = text_edit.textCursor()
    cursor.select(cursor.LineUnderCursor)
    cursor.insertText(build_command(cursor.selectedText()))
    text_edit.setTextCursor(cursor)


def insert_testcase(text_edit):
    cursor = text_edit.textCursor()
    cursor.select(cursor.LineUnderCursor)
    cursor.insertText(build_testcase(cursor.selectedText()))
    text_edit.setTextCursor(cursor)


def insert_chapter(text_edit):
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
