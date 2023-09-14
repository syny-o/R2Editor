from PyQt5.QtGui import QTextCursor
import re

PATTERN_MONITOR_VAR =  re.compile(r'(?P<command>MonitorVariables(CANape)?)\s*=\s*"(?P<variables>[\d\w_.\s]+),\s*(?P<time>\d+)\s*,\s*(?P<sample_time>\d+)\s*"', flags=re.IGNORECASE)
PATTERN_GRAPH_VAR =  re.compile(r'GraphVariables\s*=\s*"(?P<variables>[\d\w_.\s]+)"', flags=re.IGNORECASE)

def handle_syntax(string_line):
    # handle MonitorVariables/CANape
    if match := PATTERN_MONITOR_VAR.search(string_line):
        command = match.group("command")
        raw_variables = match.group("variables")
        variables = raw_variables.split()
        variables = [v.strip() for v in variables]
        time = match.group("time")
        sample_time = match.group("sample_time")
        return f'{command} = "{" ".join(variables)},{time},{sample_time}"'
    # handle GraphVariables
    elif match := PATTERN_GRAPH_VAR.search(string_line):
        raw_variables = match.group("variables")
        variables = raw_variables.split()
        variables = [v.strip() for v in variables]
        return f'GraphVariables = "{" ".join(variables)}"'        
    
    else:
        return string_line


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


    stack_if = []
    stack_for = []
    

    def __init__(self, text_edit) -> None:
        self.text_edit = text_edit
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
        self.text_edit.setPlainText(new_text)
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

            # get previous, current and next line
            previous_line = ""
            current_line = self.lines[line_number].strip()
            future_line = ""
            if line_number < len(self.lines)-1:
                future_line = self.lines[line_number+1]
            if line_number > 0:
                previous_line = self.lines[line_number-1]

            # skip header of file
            if not skipped_header:
                if current_line != "" and not self.PATTERNS["CHAPTER_START"].search(current_line) and not self.PATTERNS["TESTCASE"].search(current_line) and not self.PATTERNS["FOR_START"].search(current_line):
                    new_lines.append(current_line)
                    continue
                else:
                    skipped_header = True
                    print(current_line)

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
            current_line = handle_syntax(current_line)

            # COMMAND
            if self.PATTERNS["COMMAND"].search(current_line):
                preceding_empty_lines = 1
                indent_level = 1
                future_indent_level = 2

            # TESTCASE
            elif self.PATTERNS["TESTCASE"].search(current_line):
                test_case_number +=1
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






def go_2_next_testcase(text_edit):
    pass

def add_new_line_indent(text_edit):
    tc = text_edit.textCursor()
    line_text = tc.block().text()
    stripped_line_text = line_text.lstrip()
    difference = len(line_text) - len(stripped_line_text)
    whitespace = line_text[:difference]
    print(whitespace)
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

    # text = text.replace('\u2029', '\n')
    lines = text.split('\u2029')
    if len(lines) == 0:
        lines.append(text)

    lines2 = []
    for line in lines:
        if variant == 'indent':
            line = '\t' + line
        elif variant == 'comment':
            if line.strip().startswith("'"):
                line = line.replace("'", "", 1)
            else:
                line = "'" + line
        else:
            if line.startswith('\t'):
                line = line.replace('\t', '', 1)
            elif line.startswith('  '):
                line = line.replace('  ', '', 1)
        lines2.append(line)

    text2 = '\u2029'.join(lines2)

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



def format_text(text_edit):
    scroll_bar = text_edit.verticalScrollBar()
    slider_pos = scroll_bar.sliderPosition()


    tc = text_edit.textCursor()
    cursor_original_pos = tc.position()

    text = text_edit.toPlainText()
    lines = text.split('\n')

    if_level = 0
    for_level = 0
    indent_level = 0

    new_lines = []

    skipped_header = False
    test_case_number = 0

    TESTCASE_SEPARATOR = "-TESTCASE-NUMBER-"

    for line in lines:
        # skip header of file
        if not skipped_header:

            if line.strip() != "" and "testcase" not in line.lower() and "chapter" not in line.lower():
                # print(line)
                new_lines.append(line)
                continue
            else:
                skipped_header = True

        # skip empty lines
        if line.strip() == "": continue
        # skip non-text lines
        if not re.search("[a-zA-Z]", line):
            continue

        if TESTCASE_SEPARATOR in line:
            continue

        # remove all whitespaces from left
        current_line = line.lstrip()

        if current_line.startswith('$COM'):
            new_lines.append("") # append 1 empty line
            indent_level = 1
            current_line = '\t' * if_level +'\t' * for_level + indent_level * '\t' + current_line
        # consider which indent level is required
        elif current_line.startswith('TESTCASE'):
                test_case_number +=1
                # if test_case_number == 1: 
                #     new_lines.append(f"'##########     TESTCASE NUMBER {test_case_number}     ##########'\n")
                # else:
                #     new_lines.append(f"\n\n\n'##########     TESTCASE NUMBER {test_case_number}     ##########'\n")

                new_lines.append(f"""\
\n\n\n'###################################################################
    \n'=======================     {TESTCASE_SEPARATOR} {test_case_number}     ======================='
    \n'###################################################################
    """)
                indent_level = 0
                current_line = '\t' * if_level +'\t' * for_level + indent_level * '\t' + current_line
        elif current_line.startswith('CHAPTER'):
                new_lines.append("\n\n") # append 3 empty lines
                indent_level = 0
                current_line = '\t' * if_level +'\t' * for_level + indent_level * '\t' + current_line
        elif current_line.startswith('END CHAPTER'):
                new_lines.append("") # append 1 empty line
                indent_level = 0
                current_line = '\t' * if_level +'\t' * for_level + indent_level * '\t' + current_line                
        elif current_line.startswith("'"):
                # indent_level = 0
                current_line = '\t' * if_level +'\t' * for_level + indent_level * '\t' + current_line                
        elif current_line.startswith(tuple(['IF' 'ELSE IF'])) and 'ENDIF' not in current_line:
            # indent_level = 2
            new_lines.append("") # append 1 empty line
            current_line = '\t' * if_level +'\t' * for_level + indent_level * '\t' + current_line
            if_level += 1
        elif current_line.startswith('ENDIF'):
            if_level -= 1
            current_line = '\t' * if_level+'\t' * for_level  + indent_level * '\t' + current_line
            new_lines.append("") # append 1 empty line
        elif current_line.startswith('ELSE'):
            new_lines.append("") # append 1 empty line
            if_level -= 1
            current_line = '\t' * if_level +'\t' * for_level + indent_level * '\t' + current_line
            if_level += 1
            new_lines.append("") # append 1 empty line
        elif current_line.startswith('FOR'):
            new_lines.append("") # append 1 empty line
            # indent_level = 1
            current_line = '\t' * if_level +'\t' * for_level + indent_level * '\t' + current_line
            for_level += 1
        elif current_line.startswith('NEXT'):
            new_lines.append("") # append 1 empty line
            for_level -= 1
            # indent_level = 1
            current_line = '\t' * if_level +'\t' * for_level + indent_level * '\t' + current_line
        elif ("hil", "reset") in current_line.lower():
            current_line = '\t' * if_level +'\t' * for_level + indent_level * '\t' + current_line

        else:
            indent_level = 2
            current_line = '\t' * if_level +'\t' * for_level + indent_level * '\t' + current_line



        # add current line to new list
        new_lines.append(current_line)

    new_text = '\n'.join(new_lines)
    text_edit.setPlainText(new_text)

    tc.setPosition(cursor_original_pos)
    text_edit.setTextCursor(tc)

    # text_edit.verticalScrollBar().setSliderPosition(slider_pos)
    scroll_bar.setSliderPosition(slider_pos)



def insert_command(text_edit):
    tc = text_edit.textCursor()
    command_name = tc.block().text()
    intend_split = re.split(r'[a-zA-Z0-9$]', command_name)
    intend = intend_split[0]

    if len(intend) > 0:
        command_name = command_name.split(intend)
        command_name = command_name[1]
    tc.select(tc.LineUnderCursor)
    tc.removeSelectedText()
    text_edit.insertPlainText(intend + '$COM: "' + command_name + '" $')


def insert_testcase(text_edit):
    tc = text_edit.textCursor()
    command_name = tc.block().text()
    intend_split = re.split(r'[a-zA-Z0-9$]', command_name)
    intend = intend_split[0]

    if len(intend) > 0:
        command_name = command_name.split(intend)
        command_name = command_name[1]
    tc.select(tc.LineUnderCursor)
    tc.removeSelectedText()
    text_edit.insertPlainText(intend + 'TESTCASE "' + command_name + '" ID "" REFERENCE "" EXPECTEDRESULT 1')


def insert_chapter(text_edit):
    tc = text_edit.textCursor()
    command_name = tc.block().text()
    intend_split = re.split(r'[a-zA-Z0-9$]', command_name)
    intend = intend_split[0]

    if len(intend) > 0:
        command_name = command_name.split(intend)
        command_name = command_name[1]
    tc.select(tc.LineUnderCursor)
    tc.removeSelectedText()
    text_edit.insertPlainText(intend + 'CHAPTER "' + command_name + '"' + '\n' + intend + '\n' + intend + 'END CHAPTER' )
    tc.movePosition(QTextCursor.Up)
    tc.movePosition(QTextCursor.EndOfLine)
    text_edit.setTextCursor(tc)






def evaluate_data_4_GraphVariables(text_edit):

    tc = text_edit.textCursor()
    cursor_pos = tc.position()

    whole_text = text_edit.toPlainText()
    text_to_evaluate = whole_text[:cursor_pos].split('TESTCASE')[-1]

    matches = re.finditer(r'MonitorVariables[A-Za-z]*\s?=\s?"([^,]+)', text_to_evaluate, re.IGNORECASE)


    # print(text_to_evaluate)
    variables = []
    for match in matches:
        results_list = match.group(1).split()
        variables.extend(results_list)

    return variables




















def transform_testcase_2_2box(text_edit):

    def duplicate(text, command_list, device_name):
        final_text_lines = []
        text_lines = text.splitlines()
        for line_index in range(len(text_lines)):
            line_text = text_lines[line_index]
            if 'HIL'.lower() in line_text.lower():
                hil_init_line = adjust_hil_init(line_text, device_name)
                final_text_lines.append(hil_init_line)
                continue
            final_text_lines.append(line_text)
            for command in command_list:
                if command.lower() in line_text.lower():
                    new_line = create_duplicated_line(line_text, device_name)
                    if new_line != line_text:
                        final_text_lines.append(new_line)

        new_text = '\n'.join(final_text_lines)

        return new_text

    def adjust_hil_init(line_text, device_name):
        pattern = r'pbc[^,; ]+'
        matches = re.findall(pattern, line_text, re.IGNORECASE)
        if matches:
            slave_matches = [(device_name + ':' + match) for match in matches]
            line_text = 'HIL = Init;' + ';'.join(matches) + ';' + ';'.join(slave_matches)
        return line_text

    def create_duplicated_line(line_text, device_name):

        pattern = r'pbc[^,; ]+'
        matches = re.finditer(pattern, line_text, re.IGNORECASE)
        reversed_matches = reversed(list(matches))

        for match in reversed_matches:
            start, end = match.span()
            line_text = line_text[:start] + device_name + ':' + line_text[start:]

        return line_text


    device_name = 'Xpeng_E28A_Slave'
    commands = ['MonitorVariablesCANape', 'GraphVariables', 'VariableSequence', 'CANapeCommand']
    text = text_edit.toPlainText()

    new_text = duplicate(text, commands, device_name)
    text_edit.setPlainText(new_text)



