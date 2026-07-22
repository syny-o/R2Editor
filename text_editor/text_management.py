from PyQt5.QtGui import QTextCursor
import re

from text_editor.text_operations import (
    build_chapter,
    build_command,
    build_testcase,
    graph_variables_before_cursor,
    leading_whitespace,
    normalize_variable_command,
    transform_indentation,
)


class TextFormatter:

    TESTCASE_SEPARATOR = "-TESTCASE-NUMBER-"

    PATTERNS = {
        "FOR_START": re.compile(r"\bFOR\b.+=.+DO", re.IGNORECASE),
        "FOR_END": re.compile(r"\bNEXT\b", re.IGNORECASE),
        
        "IF_START": re.compile(r"\bIF\b", re.IGNORECASE),
        "IF_END": re.compile(r"\bENDIF\b", re.IGNORECASE), 
        "ELSE": re.compile(r"\bELSE\b", re.IGNORECASE), 

        "CHAPTER_END": re.compile(r"\bEND CHAPTER\b", re.IGNORECASE),
        "CHAPTER_START": re.compile(r"\bCHAPTER\b", re.IGNORECASE),
        "TESTCASE": re.compile(r"\bTESTCASE\b.+EXPECTEDRESULT", re.IGNORECASE),
        "COMMAND": re.compile(r"\$COM:", re.IGNORECASE),

        "MONITOR_VAR_CANAPE": re.compile(r'MonitorVariablesCANape\s?=\s?"()"')
    }


    def __init__(self, text_edit) -> None:
        self.text_edit = text_edit
        self.stack_if = []
        self.stack_for = []
        self.scroll_bar = self.text_edit.verticalScrollBar()
        self.scroll_bar_initial_position = self.scroll_bar.sliderPosition() 
        self.text_cursor = self.text_edit.textCursor()
        self.text_cursor_original_position = self.text_cursor.position()
        self.text_content = self.text_edit.toPlainText()
        self.lines = self.text_content.split('\n')


    def run(self):
        # get formated lines, merge them together and send it to text_edit object
        formated_lines = self._format_text()
        new_text = '\n'.join(formated_lines)
        
        temp_cursor = self.text_edit.textCursor()
        temp_cursor.select(QTextCursor.Document)
        temp_cursor.insertText(new_text)
        # self.text_edit.setPlainText(new_text)
        # retrieve original position of cursor
        self.text_cursor.setPosition(self.text_cursor_original_position)
        self.text_edit.setTextCursor(self.text_cursor)
        # retrieve original position of scrollbar
        self.scroll_bar.setSliderPosition(self.scroll_bar_initial_position)   

    def _format_text(self):
        if_level = 0
        for_level = 0
        indent_level = 0

        new_lines = []

        skipped_header = False
        test_case_number = 0

        for line_number in range(len(self.lines)):
            future_indent_level = None
            future_if_level = None
            future_for_level = None
            preceding_empty_lines = 0
            upcoming_empty_lines = 0

            # get previous and current line
            previous_line = ""
            current_line = self.lines[line_number].strip()
            if line_number > 0:
                previous_line = self.lines[line_number-1]

            # skip header of file
            if not skipped_header:
                if current_line != "" and not self.PATTERNS["CHAPTER_START"].search(current_line) and not self.PATTERNS["TESTCASE"].search(current_line) and not self.PATTERNS["FOR_START"].search(current_line):
                    new_lines.append(current_line)
                    continue
                else:
                    skipped_header = True
                    # print(current_line)

            # skip empty lines
            if current_line == "": 
                continue
            # skip non-text lines
            if not re.search("[a-zA-Z]", current_line):
                continue
            # skip automatically added test case numbers (will be added once again below)
            if self.TESTCASE_SEPARATOR in current_line:
                continue
            #append comment lines without futher formatting
            # if current_line.startswith("'"):
            #     new_lines.append(current_line) 
            #     continue
            
            
            # handle syntax --> correcting spaces in MonitorVariables/Graph Variables commands
            current_line = normalize_variable_command(current_line)

            # COMMAND
            if self.PATTERNS["COMMAND"].search(current_line):
                preceding_empty_lines = 1
                indent_level = 1
                future_indent_level = 2

            # TESTCASE
            elif self.PATTERNS["TESTCASE"].search(current_line):
                test_case_number +=1
                # TODO: consider if every test case should be introduced with this string
                new_lines.append(f"""\
      \n\n'###################################################################
        \n'=======================     {self.TESTCASE_SEPARATOR} {test_case_number}     ======================='
        \n'###################################################################
        """)
                indent_level = 0
                future_indent_level = 1

            # CHAPTER
            elif self.PATTERNS["CHAPTER_START"].search(current_line):
                preceding_empty_lines = 2
                indent_level = 0

            # END CHAPTER
            elif self.PATTERNS["CHAPTER_END"].search(current_line):
                preceding_empty_lines = 1
                indent_level = 0
                upcoming_empty_lines = 2

            # IF                
            elif self.PATTERNS["IF_START"].search(current_line):
                preceding_empty_lines = 1
                # upcoming_empty_lines = 1
                future_if_level = if_level + 1

                self.stack_if.append(indent_level)

            # ENDIF
            elif self.PATTERNS["IF_END"].search(current_line):
                if_level -= 1
                if not self.PATTERNS["IF_END"].search(previous_line):
                    preceding_empty_lines = 1
                
                indent_level = self.stack_if.pop()

            # ELSE
            elif self.PATTERNS["ELSE"].search(current_line) and not self.PATTERNS["IF_START"].search(current_line):
                preceding_empty_lines = 1
                if_level -= 1
                future_if_level = if_level + 1
                # upcoming_empty_lines = 1

                indent_level = self.stack_if[-1]
            
            # ELSE IF
            elif self.PATTERNS["ELSE"].search(current_line) and self.PATTERNS["IF"].search(current_line):
                preceding_empty_lines = 1
                if_level -= 1
                future_if_level = if_level + 1
                # upcoming_empty_lines = 1                

                
            
            # FOR
            elif self.PATTERNS["FOR_START"].search(current_line):
                if not self.PATTERNS["FOR_START"].search(previous_line):
                    preceding_empty_lines = 1
                             
                future_for_level = for_level + 1
                upcoming_empty_lines = 0

                
                self.stack_for.append(indent_level)

            # NEXT
            elif self.PATTERNS["FOR_END"].search(current_line):
                if not self.PATTERNS["FOR_END"].search(previous_line):
                    preceding_empty_lines = 1
                
                for_level -= 1
                upcoming_empty_lines = 0

                indent_level = self.stack_for.pop()

            # HIL Reset
            elif re.search(r"Hil?\s=?\sReset", current_line, re.IGNORECASE):
                indent_level = 2
                upcoming_empty_lines = 1

            # EVERYTHING ELSE   
            else:
                # indent_level = 2
                pass


            
            # current_line = str(for_level) + str(indent_level) + '\t' * if_level + '\t' * for_level + indent_level * '\t' + current_line
            current_line = '\t' * if_level + '\t' * for_level + indent_level * '\t' + current_line

            if future_indent_level:
                indent_level = future_indent_level
            
            if future_if_level:
                if_level = future_if_level

            if future_for_level:
                for_level = future_for_level                

            if preceding_empty_lines: 
                new_lines.append("" * preceding_empty_lines)

            new_lines.append(current_line)

            if upcoming_empty_lines:
                new_lines.append("" * upcoming_empty_lines)

            # print("FOR" + str(self.stack_for))
            # print("IF: " + str(self.stack_if))

            # if self.stack_if or self.stack_for:
            #     raise Exception("Syntax Error in FOR cycle or IF statement.")

        return new_lines






def add_new_line_indent(text_edit):
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
    tc = text_edit.textCursor()
    tc_original_pos = tc.position()
    tc.movePosition(QTextCursor.StartOfLine)
    tc_final_pos = tc.position()

    if tc_original_pos == tc_final_pos and tc.block().text() != '':
        # IF CURSOR WAS AT THE BEGINNING OF THE LINE, MOVE IT BEFORE FIRST LETTER
        tc.movePosition(QTextCursor.NextWord)
    text_edit.setTextCursor(tc)


def key_shift_home_press(text_edit):
    tc = text_edit.textCursor()
    tc.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
    text_edit.setTextCursor(tc)


def indent_dedent_comment(text_edit, variant):
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
    tc = text_edit.textCursor()
    tc.select(tc.LineUnderCursor)
    tc.insertText(build_chapter(tc.selectedText()))
    tc.movePosition(QTextCursor.Up)
    tc.movePosition(QTextCursor.EndOfLine)
    text_edit.setTextCursor(tc)






def evaluate_data_4_GraphVariables(text_edit):
    tc = text_edit.textCursor()
    return graph_variables_before_cursor(text_edit.toPlainText(), tc.position())
