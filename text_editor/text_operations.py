PARAGRAPH_SEPARATOR = '\u2029'


def leading_whitespace(text):
    return text[:len(text) - len(text.lstrip())]


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
