import re


def validate_module_output(doors_output, module_path):
    if module_path not in doors_output:
        return {
            'success': False,
            'message': (
                f"Failed to download module:\n {module_path}.\n\n Reason:\n "
                "Connection issues during downloading or invalid module path!"
            ),
            'baselines': None,
            'attributes': None,
        }

    module_text = next(
        block
        for block in doors_output.split("<PATH_START>")
        if module_path in block
    )
    requirements_match = re.search(
        fr"{re.escape(module_path)}(.+?)<REQUIREMENTS_END>",
        module_text,
        re.DOTALL,
    )
    if not requirements_match:
        return {
            'success': False,
            'message': (
                f"Failed to download module:\n {module_path}.\n\n Reason:\n "
                "Invalid column name!"
            ),
            'baselines': extract_baselines(module_text),
            'attributes': extract_attributes(module_text),
        }

    return {
        'success': True,
        'message': "OK",
        'baselines': None,
        'attributes': None,
    }


def parse_module_output(doors_output, module_path):
    module_blocks = re.findall(
        r"<<<MODULE_START>>>(.*?)<<<MODULE_END>>>",
        doors_output,
        re.DOTALL,
    )
    for module_text in module_blocks:
        path_match = re.search(
            r"<PATH_START>(?P<path>.*)<PATH_END>",
            module_text,
            re.DOTALL,
        )
        if path_match and path_match.group("path") == module_path:
            return {
                "baselines": extract_baselines(module_text),
                "attributes": extract_attributes(module_text),
                "requirements": re.findall(
                    r"<REQUIREMENT_START>(.*?)<REQUIREMENT_END>",
                    module_text,
                    re.DOTALL,
                ),
            }
    return None


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
