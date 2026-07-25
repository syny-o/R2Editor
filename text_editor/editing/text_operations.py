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
WORD_PATTERN = re.compile(r'[\w.]+')


def leading_whitespace(text):
    return text[:len(text) - len(text.lstrip())]


def smart_home_column(line_text, current_column):
    first_text_column = len(leading_whitespace(line_text))
    if current_column == first_text_column:
        return 0
    return first_text_column


def cursor_column_after_transform(original_text, transformed_text, original_column):
    original_column = max(0, min(original_column, len(original_text)))
    change_column = 0
    for original_char, transformed_char in zip(original_text, transformed_text):
        if original_char != transformed_char:
            break
        change_column += 1

    length_change = len(transformed_text) - len(original_text)
    if length_change > 0 and original_column >= change_column:
        return original_column + length_change
    if length_change < 0 and original_column > change_column:
        return max(change_column, original_column + length_change)
    return original_column


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


def cursor_position_after_format(original_text, formatted_text, original_position):
    original_position = max(0, min(original_position, len(original_text)))
    original_lines = original_text.split('\n')
    formatted_lines = formatted_text.split('\n')

    line_start = original_text.rfind('\n', 0, original_position) + 1
    line_index = original_text.count('\n', 0, original_position)
    original_line = original_lines[line_index]
    original_column = original_position - line_start
    normalized_line = normalize_variable_command(original_line.strip())

    occurrence = sum(
        normalize_variable_command(line.strip()) == normalized_line
        for line in original_lines[:line_index + 1]
    )
    matching_lines = [
        index
        for index, line in enumerate(formatted_lines)
        if line.strip() == normalized_line
    ]
    if occurrence == 0 or occurrence > len(matching_lines):
        return min(original_position, len(formatted_text))

    formatted_line_index = matching_lines[occurrence - 1]
    formatted_line = formatted_lines[formatted_line_index]
    original_content = original_line.strip()
    formatted_content = formatted_line.strip()
    content_column = max(
        0,
        min(
            original_column - len(leading_whitespace(original_line)),
            len(original_content),
        ),
    )

    original_words = list(WORD_PATTERN.finditer(original_content))
    current_word = next(
        (
            match
            for match in original_words
            if match.start() <= content_column <= match.end()
        ),
        None,
    )
    if current_word is not None:
        word_occurrence = sum(
            match.group() == current_word.group()
            for match in original_words
            if match.start() <= current_word.start()
        )
        formatted_words = [
            match
            for match in WORD_PATTERN.finditer(formatted_content)
            if match.group() == current_word.group()
        ]
        if word_occurrence <= len(formatted_words):
            formatted_word = formatted_words[word_occurrence - 1]
            offset_in_word = min(
                content_column - current_word.start(),
                len(formatted_word.group()),
            )
            content_column = formatted_word.start() + offset_in_word

    formatted_column = (
        len(leading_whitespace(formatted_line))
        + min(content_column, len(formatted_content))
    )
    return (
        sum(len(line) + 1 for line in formatted_lines[:formatted_line_index])
        + formatted_column
    )


def transform_indentation(text, operation):
    ends_at_next_line_start = text.endswith(PARAGRAPH_SEPARATOR)
    lines = text.split(PARAGRAPH_SEPARATOR)
    if ends_at_next_line_start:
        lines = lines[:-1]

    if operation == 'comment':
        transformed_lines = toggle_line_comments(lines)
    else:
        transformed_lines = [
            transform_line_indentation(line, operation)
            for line in lines
        ]
    transformed_text = PARAGRAPH_SEPARATOR.join(transformed_lines)
    if ends_at_next_line_start:
        transformed_text += PARAGRAPH_SEPARATOR
    return transformed_text


def toggle_line_comments(lines):
    nonempty_lines = [line for line in lines if line.strip()]
    uncomment = bool(nonempty_lines) and all(
        line.lstrip().startswith("'")
        for line in nonempty_lines
    )

    transformed_lines = []
    for line in lines:
        if not line.strip():
            transformed_lines.append(line)
            continue

        indentation, content = split_indentation(line)
        if uncomment:
            content = content[1:] if content.startswith("'") else content
        elif not content.startswith("'"):
            content = "'" + content
        transformed_lines.append(indentation + content)

    return transformed_lines


def transform_line_indentation(line, operation):
    if operation == 'indent':
        return '\t' + line
    if operation == 'dedent':
        if line.startswith('\t'):
            return line[1:]
        if line.startswith('  '):
            return line[2:]
        return line

    raise ValueError(f'Unsupported indentation operation: {operation}')
