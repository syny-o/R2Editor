from PyQt5.QtWidgets import QMessageBox

from data_manager.coverage.data import (
    apply_file_references,
    ignored_references_outside_coverage,
    remove_ignored_references,
    toggle_script_reference,
)
from data_manager.coverage.filter import (
    matching_references,
    translate_coverage_filter,
)


def clear_coverage(module):
    module._coverage_dict.clear()


def remove_all_script_references(module):
    for script_references in module._coverage_dict.values():
        script_references.clear()


def update_script_reference(module, requirement_id, path):
    changed = toggle_script_reference(
        module._coverage_dict,
        requirement_id,
        path,
    )
    if changed:
        module.update_icons_according_to_coverage()
        module.update_title_text()
        return True


def check_coverage_with_file_pointers(module, reference_dict):
    coverage_before = module.coverage_dict.copy()
    apply_coverage_filter(module)
    apply_file_references(module._coverage_dict, reference_dict)

    module.update_icons_according_to_coverage()
    module.update_title_text()

    if coverage_before != module._coverage_dict:
        return True


def translate_filter(module, filter_string):
    return translate_coverage_filter(filter_string, module.columns_names)


def apply_coverage_filter(module, filter_string=None):
    if filter_string:
        module.coverage_filter = filter_string

    if not module.coverage_filter:
        return

    translated_filter = translate_filter(module, module.coverage_filter)
    module._coverage_dict.clear()
    try:
        references = matching_references(module, translated_filter)
    except Exception as exception:
        module.coverage_filter = None
        raise Exception(str(exception))

    module._coverage_dict.update(
        {reference: [] for reference in references}
    )

    invalid_ignored_references = ignored_references_outside_coverage(
        module.ignore_list,
        module._coverage_dict,
    )
    remove_invalid_ignored_references(
        module,
        invalid_ignored_references,
    )

    for ignored_reference in module.ignore_list:
        module._coverage_dict.pop(ignored_reference, None)

    module.update_icons_according_to_coverage()
    module.update_title_text()


def remove_invalid_ignored_references(module, references):
    if not references:
        return

    answer = QMessageBox.question(
        module.data_manager,
        "Remove ignored items",
        "Following items are in ignore list but do not meet the coverage "
        f"filter:\n\n{references}\n\n"
        "Do you want to remove them from the ignore list?",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No,
    )
    if answer == QMessageBox.Yes:
        remove_ignored_references(
            module.ignore_list,
            module.notes,
            references,
        )


def remove_coverage_filter(module):
    module._coverage_dict.clear()
    module.coverage_filter = None
    module.update_title_text()
    module.update_icons_according_to_coverage()
