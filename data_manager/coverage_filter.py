def translate_coverage_filter(filter_string, column_names):
    translated = filter_string.strip()
    indexed_names = enumerate(column_names)
    longest_first = sorted(
        indexed_names,
        key=lambda item: len(item[1]),
        reverse=True,
    )
    for index, column_name in longest_first:
        translated = translated.replace(
            column_name,
            f'column[{index}]',
        )
    return translated.strip()
