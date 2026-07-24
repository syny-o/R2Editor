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


def covered_references(coverage):
    return [
        requirement_id
        for requirement_id, script_paths in coverage.items()
        if script_paths
    ]


def uncovered_references(coverage):
    return [
        requirement_id
        for requirement_id, script_paths in coverage.items()
        if not script_paths
    ]


def coverage_counts(coverage):
    return len(covered_references(coverage)), len(coverage)
