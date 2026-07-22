import re


PARAGRAPH_SEPARATOR = '\u2029'

MONITOR_VARIABLES_PATTERN = re.compile(
    r'''(?<!')(?P<command>MonitorVariables(CANape)?)\s*=\s*"'''
    r'''(?P<variables>[\d\w_.\s]+),\s*(?P<time>\d+)\s*,'''
    r'''\s*(?P<sample_time>\d+)\s*"''',
    flags=re.IGNORECASE,
)
GRAPH_VARIABLES_PATTERN = re.compile(
    r'''(?<!')GraphVariables\s*=\s*"(?P<variables>[\d\w_.\s]+)"''',
    flags=re.IGNORECASE,
)


def leading_whitespace(text):
    return text[:len(text) - len(text.lstrip())]


def split_indentation(text):
    indentation = leading_whitespace(text)
    return indentation, text[len(indentation):]


def build_command(text):
    indentation, name = split_indentation(text)
    return f'{indentation}$COM: "{name}" $'


def build_testcase(text):
    indentation, name = split_indentation(text)
    return f'{indentation}TESTCASE "{name}" ID "" REFERENCE "" EXPECTEDRESULT 1'


def build_chapter(text):
    indentation, name = split_indentation(text)
    return (
        f'{indentation}CHAPTER "{name}"\n'
        f'{indentation}\n'
        f'{indentation}END CHAPTER'
    )


def graph_variables_before_cursor(text, cursor_position):
    current_testcase = text[:cursor_position].split('TESTCASE')[-1]
    matches = re.finditer(
        r'MonitorVariables[A-Za-z]*\s?=\s?"([^,]+)',
        current_testcase,
        re.IGNORECASE,
    )

    variables = []
    for match in matches:
        variables.extend(match.group(1).split())
    return variables


def completion_context(line_text, position_in_line, has_selection=False):
    if has_selection:
        return ''
    text_before_cursor = line_text[:position_in_line]
    return text_before_cursor.partition('=')[0].strip()


def format_first_assignment(line_text, excluded_prefixes=()):
    stripped_end = line_text.rstrip()
    if '=' not in stripped_end:
        return line_text
    if stripped_end.strip().startswith(tuple(excluded_prefixes)):
        return line_text

    left_side, _, right_side = stripped_end.partition('=')
    return f'{left_side.rstrip()} = {right_side.strip()}'


def normalize_variable_command(line_text):
    if line_text.strip().startswith("'"):
        return line_text

    monitor_match = MONITOR_VARIABLES_PATTERN.search(line_text)
    if monitor_match:
        variables = monitor_match.group('variables').split()
        return (
            f'{monitor_match.group("command")} = '
            f'"{" ".join(variables)},{monitor_match.group("time")},'
            f'{monitor_match.group("sample_time")}"'
        )

    graph_match = GRAPH_VARIABLES_PATTERN.search(line_text)
    if graph_match:
        variables = graph_match.group('variables').split()
        return f'GraphVariables = "{" ".join(variables)}"'

    return line_text


def transform_indentation(text, operation):
    lines = text.split(PARAGRAPH_SEPARATOR)
    transformed_lines = [
        transform_line_indentation(line, operation)
        for line in lines
    ]
    return PARAGRAPH_SEPARATOR.join(transformed_lines)


def transform_line_indentation(line, operation):
    if operation == 'indent':
        return '\t' + line
    if operation == 'comment':
        if line.strip().startswith("'"):
            return line.replace("'", '', 1)
        return "'" + line
    if operation == 'dedent':
        if line.startswith('\t'):
            return line[1:]
        if line.startswith('  '):
            return line[2:]
        return line

    raise ValueError(f'Unsupported indentation operation: {operation}')
