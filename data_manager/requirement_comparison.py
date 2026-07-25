def compare_requirement_data(columns, old_data, new_data):
    differences = []

    for identifier in set(old_data) - set(new_data):
        differences.append({
            'identifier': identifier,
            'status': 'missing',
            'changes': [],
        })

    for identifier in set(new_data) - set(old_data):
        differences.append({
            'identifier': identifier,
            'status': 'new',
            'changes': [],
        })

    for identifier, old_columns in old_data.items():
        if identifier not in new_data:
            continue

        new_columns = new_data[identifier]
        if old_columns == new_columns:
            continue

        changes = []
        for index, old_value in enumerate(old_columns):
            if old_value != new_columns[index]:
                changes.append(
                    (
                        columns[index],
                        old_value,
                        new_columns[index],
                    )
                )

        differences.append({
            'identifier': identifier,
            'status': 'changed',
            'changes': changes,
        })

    return differences
