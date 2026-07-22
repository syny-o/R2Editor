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

    tc = text_edit.textCursor()
    line_text = tc.block().text()
    whitespace = leading_whitespace(line_text)
    tc.insertText('\r')
    line_text = tc.block().text()
    if line_text.strip() == '':
        tc.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
    tc.insertText(whitespace)

    # # 8/10/2022 REMOVE SPACES AT THE END OF PREVIOUS ROW
    # tc.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
    # text_take_with_to_next_row = tc.selectedText()
    # tc.removeSelectedText()
    # tc.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
    # t = tc.selectedText()
    #
    # tc.insertText(t.rstrip())
    #
    # intend_split = re.split(r"""\S""", line_text)
    #
    # intend = intend_split[0]
    # tc.insertText('\r' + intend + text_take_with_to_next_row)





def key_home_press(text_edit):
    from PyQt5.QtGui import QTextCursor

    tc = text_edit.textCursor()
    tc_original_pos = tc.position()
    tc.movePosition(QTextCursor.StartOfLine)
    tc_final_pos = tc.position()

    if tc_original_pos == tc_final_pos and tc.block().text() != '':
        # IF CURSOR WAS AT THE BEGINNING OF THE LINE, MOVE IT BEFORE FIRST LETTER
        tc.movePosition(QTextCursor.NextWord)
    text_edit.setTextCursor(tc)


def key_shift_home_press(text_edit):
    from PyQt5.QtGui import QTextCursor

    tc = text_edit.textCursor()
    tc.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
    text_edit.setTextCursor(tc)


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

    tc = text_edit.textCursor()
    cursor_original_pos = tc.position()

    one_line = False if len(tc.selectedText()) > 0 else True

    if one_line:
        tc.movePosition(QTextCursor.EndOfLine)
        tc.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)

    selection_start = tc.selectionStart()
    text = tc.selectedText()

    text2 = transform_indentation(text, variant)

    tc.insertText(text2)

    if one_line:
        tc.setPosition(cursor_original_pos-(len(text) - len(text2)))
    else:
        if cursor_original_pos == selection_start:
            tc.setPosition(cursor_original_pos, QTextCursor.KeepAnchor)
        else:
            tc.setPosition(selection_start)
            tc.setPosition(cursor_original_pos-(len(text) - len(text2)), QTextCursor.KeepAnchor)

    text_edit.setTextCursor(tc)



def insert_command(text_edit):
    tc = text_edit.textCursor()
    tc.select(tc.LineUnderCursor)
    tc.insertText(build_command(tc.selectedText()))
    text_edit.setTextCursor(tc)


def insert_testcase(text_edit):
    tc = text_edit.textCursor()
    tc.select(tc.LineUnderCursor)
    tc.insertText(build_testcase(tc.selectedText()))
    text_edit.setTextCursor(tc)


def insert_chapter(text_edit):
    from PyQt5.QtGui import QTextCursor

    tc = text_edit.textCursor()
    tc.select(tc.LineUnderCursor)
    tc.insertText(build_chapter(tc.selectedText()))
    tc.movePosition(QTextCursor.Up)
    tc.movePosition(QTextCursor.EndOfLine)
    text_edit.setTextCursor(tc)






def evaluate_data_4_GraphVariables(text_edit):
    tc = text_edit.textCursor()
    return graph_variables_before_cursor(text_edit.toPlainText(), tc.position())
