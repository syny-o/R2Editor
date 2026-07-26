from data_manager.requirements.tree_builder import iter_descendants


def build_export_header(column_names, column_indexes, include_note):
    header = ['Identifier']
    header.extend(column_names[index] for index in column_indexes)
    if include_note:
        header.append('User note')
    return header


def build_export_rows(
    requirement_module,
    column_indexes,
    include_note,
    is_hidden,
):
    rows = []
    for requirement in iter_descendants(requirement_module):
        if requirement.hasChildren() or is_hidden(requirement):
            continue

        row = [requirement.reference]
        row.extend(
            requirement.columns_data[index]
            for index in column_indexes
        )
        if include_note:
            row.append(requirement.note)
        rows.append(row)

    return rows
