from data_manager.requirement_tree_builder import iter_descendants


def requirement_tree_to_list(module):
    return [
        {
            'reference': node.reference,
            'heading': node.heading,
            'level': node.level,
            'outlinks': node.outlinks,
            'inlinks': node.inlinks,
            'file_references': list(node.file_references),
            'is_covered': node.is_covered,
            'columns_data': node.columns_data,
        }
        for node in iter_descendants(module)
    ]


def requirements_to_dict(requirements):
    return {
        requirement.get('reference'): requirement.get('columns_data')
        for requirement in requirements
    }


def requirement_module_to_dict(module):
    return {
        "path": module.path,
        "columns": module.columns_names_backup,
        "attributes": module.attributes,
        "baseline": module.baseline,
        "update_time": module.timestamp,
        "coverage_filter": module.coverage_filter,
        "coverage_dict": module.coverage_dict,
        "ignore_list": list(module.ignore_list),
        "notes": module.notes,
        "current_baseline": module.current_baseline_backup,
        "column_number_as_identifier": module.column_number_as_identifier,
        "requirements": requirement_tree_to_list(module),
    }
