import re

from text_editor.text_operations import normalize_variable_command


class TextFormatter:
    """Format the editor's script text without depending on PyQt."""

    TESTCASE_SEPARATOR = "-TESTCASE-NUMBER-"

    PATTERNS = {
        "FOR_START": re.compile(r"^FOR\b.+=.+DO", re.IGNORECASE),
        "FOR_END": re.compile(r"^NEXT\b", re.IGNORECASE),
        "ELSE_IF": re.compile(r"^ELSE\s+IF\b", re.IGNORECASE),
        "IF_START": re.compile(r"^IF\b", re.IGNORECASE),
        "IF_END": re.compile(r"^ENDIF\b", re.IGNORECASE),
        "ELSE": re.compile(r"^ELSE\b", re.IGNORECASE),
        "CHAPTER_END": re.compile(r"^END CHAPTER\b", re.IGNORECASE),
        "CHAPTER_START": re.compile(r"^CHAPTER\b", re.IGNORECASE),
        "TESTCASE": re.compile(r"^TESTCASE\b.+EXPECTEDRESULT", re.IGNORECASE),
        "COMMAND": re.compile(r"^\$COM:", re.IGNORECASE),
        "HIL_RESET": re.compile(r"^HIL\s*=\s*RESET\b", re.IGNORECASE),
    }

    def __init__(self, text_content: str) -> None:
        self.stack_if = []
        self.stack_for = []
        self.lines = text_content.split("\n")

    def run(self):
        return "\n".join(self._format_text())

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
            add_blank_line_before = False
            add_blank_line_after = False

            previous_line = ""
            current_line = self.lines[line_number].strip()
            if line_number > 0:
                previous_line = self.lines[line_number - 1].strip()

            if not skipped_header:
                if (
                    current_line != ""
                    and not self.PATTERNS["CHAPTER_START"].search(current_line)
                    and not self.PATTERNS["TESTCASE"].search(current_line)
                    and not self.PATTERNS["FOR_START"].search(current_line)
                ):
                    new_lines.append(current_line)
                    continue
                skipped_header = True

            if current_line == "":
                continue
            if not re.search("[a-zA-Z]", current_line):
                continue
            if self.TESTCASE_SEPARATOR in current_line:
                continue

            current_line = normalize_variable_command(current_line)

            if self.PATTERNS["COMMAND"].search(current_line):
                add_blank_line_before = True
                indent_level = 1
                future_indent_level = 2
            elif self.PATTERNS["TESTCASE"].search(current_line):
                test_case_number += 1
                new_lines.append(
                    f"""      \n\n'###################################################################
        \n'=======================     {self.TESTCASE_SEPARATOR} {test_case_number}     ======================='
        \n'###################################################################
        """
                )
                indent_level = 0
                future_indent_level = 1
            elif self.PATTERNS["CHAPTER_END"].search(current_line):
                add_blank_line_before = True
                indent_level = 0
            elif self.PATTERNS["CHAPTER_START"].search(current_line):
                add_blank_line_before = True
                indent_level = 0
            elif self.PATTERNS["ELSE_IF"].search(current_line):
                add_blank_line_before = True
                future_if_level = if_level + 1
                self.stack_if.append(indent_level)
            elif self.PATTERNS["IF_START"].search(current_line):
                add_blank_line_before = True
                future_if_level = if_level + 1
                self.stack_if.append(indent_level)
            elif self.PATTERNS["IF_END"].search(current_line):
                if not self.PATTERNS["IF_END"].search(previous_line):
                    add_blank_line_before = True
                if self.stack_if:
                    if_level = max(0, if_level - 1)
                    indent_level = self.stack_if.pop()
            elif self.PATTERNS["ELSE"].search(current_line):
                add_blank_line_before = True
                if self.stack_if:
                    if_level = max(0, if_level - 1)
                    future_if_level = if_level + 1
                    indent_level = self.stack_if[-1]
            elif self.PATTERNS["FOR_START"].search(current_line):
                if not self.PATTERNS["FOR_START"].search(previous_line):
                    add_blank_line_before = True
                future_for_level = for_level + 1
                self.stack_for.append(indent_level)
            elif self.PATTERNS["FOR_END"].search(current_line):
                if not self.PATTERNS["FOR_END"].search(previous_line):
                    add_blank_line_before = True
                if self.stack_for:
                    for_level = max(0, for_level - 1)
                    indent_level = self.stack_for.pop()
            elif self.PATTERNS["HIL_RESET"].search(current_line):
                indent_level = 2
                add_blank_line_after = True

            current_line = (
                "\t" * if_level
                + "\t" * for_level
                + indent_level * "\t"
                + current_line
            )

            if future_indent_level:
                indent_level = future_indent_level
            if future_if_level:
                if_level = future_if_level
            if future_for_level:
                for_level = future_for_level
            if add_blank_line_before:
                new_lines.append("")

            new_lines.append(current_line)

            if add_blank_line_after:
                new_lines.append("")

        return new_lines
