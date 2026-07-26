from data_manager.doors.output_parser import validate_module_output
from data_manager.requirements.serialization import (
    requirement_tree_to_list,
    requirements_to_dict,
)


def update_module_from_doors(module, doors_output, timestamp):
    columns_changed = module.columns_names_backup != module.columns_names

    success, message = validate_doors_output(module, doors_output)
    if not success:
        return False, message

    original_module_data = requirements_to_dict(
        requirement_tree_to_list(module)
    )

    module.timestamp = timestamp
    module.removeRows(0, module.rowCount())
    module._txtfile_to_tree(doors_output)
    module.columns_names_backup = [*module.columns_names]
    module.current_baseline_backup = module.current_baseline

    new_module_data = (
        requirements_to_dict(requirement_tree_to_list(module))
        if original_module_data
        else {}
    )

    module.apply_coverage_filter()

    if (
        not columns_changed
        and original_module_data
        and original_module_data != new_module_data
    ):
        return True, (
            module.columns_names,
            original_module_data,
            new_module_data,
        )

    return True, None


def validate_doors_output(module, doors_output):
    result = validate_module_output(doors_output, module.path)
    if result["baselines"] is not None:
        module.baseline = result["baselines"]
    if result["attributes"] is not None:
        module.attributes = result["attributes"]
    return result["success"], result["message"]
