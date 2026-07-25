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


def ignored_references_outside_coverage(ignored_references, coverage):
    return [
        reference
        for reference in ignored_references
        if reference not in coverage
    ]


def remove_ignored_references(ignored_references, notes, references_to_remove):
    for reference in references_to_remove:
        if reference in ignored_references:
            ignored_references.remove(reference)
        notes.pop(reference, None)


def normalize_ignored_references(ignored_references):
    return sorted({
        reference.lower()
        for reference in (ignored_references or [])
    })


def normalize_requirement_notes(notes):
    return {
        reference.lower(): note
        for reference, note in (notes or {}).items()
    }


def add_reference_to_ignore(coverage, ignored_references, reference):
    normalized_reference = reference.lower()
    if (
        normalized_reference in ignored_references
        or reference in ignored_references
    ):
        return False

    coverage.pop(normalized_reference)
    ignored_references.append(normalized_reference)
    return True


def remove_reference_from_ignore(
    coverage,
    ignored_references,
    notes,
    reference,
    remove_note=False,
):
    normalized_reference = reference.lower()
    if (
        normalized_reference not in ignored_references
        and reference not in ignored_references
    ):
        return False

    try:
        ignored_references.remove(reference)
    except ValueError:
        ignored_references.remove(normalized_reference)

    coverage[normalized_reference] = []
    if remove_note:
        notes.pop(normalized_reference, None)
    return True
