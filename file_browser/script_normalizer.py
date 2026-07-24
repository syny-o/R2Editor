from config.pbc_patterns_scripts import patterns


def normalize_script_text(text, normalization_patterns=patterns):
    replacements = []

    for pattern, expected_value in normalization_patterns.items():
        for match in pattern.finditer(text):
            value_to_replace = match.group()
            if value_to_replace == expected_value:
                continue

            text = text.replace(value_to_replace, expected_value)
            replacements.append((value_to_replace, expected_value))

    return text, replacements
