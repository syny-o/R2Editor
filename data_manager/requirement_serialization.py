def requirement_tree_to_list(module):
    requirements = []
    _append_children(module, requirements)
    return requirements


def requirements_to_dict(requirements):
    return {
        requirement.get('reference'): requirement.get('columns_data')
        for requirement in requirements
    }


def _append_children(parent, requirements):
    for row in range(parent.rowCount()):
        node = parent.child(row)
        requirements.append(
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
        )
        _append_children(node, requirements)
