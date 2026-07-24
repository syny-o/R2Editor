import re


def extract_attributes(text):
    return re.findall(
        r'<ATTRIBUTE_START>(.*?)<ATTRIBUTE_END>',
        text,
        re.DOTALL,
    )


def extract_baselines(text):
    baselines = {}
    baseline_blocks = re.findall(
        r'<BASELINE_START>(.*?)<BASELINE_END>',
        text,
        re.DOTALL,
    )
    for block in baseline_blocks:
        version = _required_value(block, 'VERSION')
        user = _required_value(block, 'USER')
        date = _required_value(block, 'DATE')
        annotation = _optional_value(block, 'ANNOTATION', dotall=True)
        baselines[version] = [user, date, annotation]
    return baselines


def parse_requirement(text, column_number_as_identifier=None):
    columns = re.findall(
        r'<COLUMN_START>(.*?)<COLUMN_END>',
        text,
        re.DOTALL,
    )
    identifier = _required_value(text, 'ID')
    if column_number_as_identifier is not None:
        identifier = columns[column_number_as_identifier]

    return {
        'identifier': identifier,
        'level': int(_required_value(text, 'LEVEL')),
        'heading': _optional_value(text, 'HEADING'),
        'columns': columns,
        'outlinks': re.findall(
            r'<OUTLINK_START>(.*?)<OUTLINK_END>',
            text,
            re.DOTALL,
        ),
        'inlinks': re.findall(
            r'<INLINK_START>(.*?)<INLINK_END>',
            text,
            re.DOTALL,
        ),
    }


def _required_value(text, tag):
    match = re.search(
        fr'<{tag}_START>(?P<value>.*)<{tag}_END>',
        text,
    )
    return match.group('value')


def _optional_value(text, tag, dotall=False):
    flags = re.DOTALL if dotall else 0
    match = re.search(
        fr'<{tag}_START>(?P<value>.*)<{tag}_END>',
        text,
        flags,
    )
    return match.group('value') if match else ''
