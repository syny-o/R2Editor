def toggle_script_reference(coverage, requirement_id, script_path):
    key = requirement_id.lower()
    if key not in coverage:
        return False

    paths = coverage[key]
    if script_path in paths:
        paths.remove(script_path)
    else:
        paths.append(script_path)
    return True


def apply_file_references(coverage, references_by_file):
    for requirement_id, script_paths in references_by_file.items():
        if requirement_id in coverage:
            coverage[requirement_id] = list(script_paths)

        corrected_id = requirement_id.replace(
            'sydesign',
            '-sydesign',
        )
        if corrected_id in coverage:
            coverage[corrected_id] = list(script_paths)
