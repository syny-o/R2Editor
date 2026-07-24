from config.pbc_patterns import patterns, signals_to_check


def contains_number(string):
    return any(char.isdigit() for char in string)


def find_missing_signals(text, required_signals=signals_to_check):
    return [
        signal
        for signal in required_signals
        if signal not in text and not contains_number(signal)
    ]


def normalize_a2l_text(
    text,
    normalization_patterns=patterns,
    status_callback=None,
):
    duplicated_signals = []
    replacements = {}

    for pattern, expected_value in normalization_patterns.items():
        if status_callback:
            status_callback(f"Checking: <{expected_value}>")

        matches = pattern.findall(text)
        iteration = pattern.finditer(text)

        if len(matches) > 1:
            if not contains_number(expected_value):
                duplicated_signals.append(expected_value)

            string_to_replace = None
            smallest_match_length = 1000
            for match in iteration:
                if match.group(2) == expected_value:
                    string_to_replace = None
                    break
                if len(match.group(2)) < smallest_match_length:
                    smallest_match_length = len(match.group(2))
                    string_to_replace = match.group(2)
                    replace_start, replace_end = match.span(2)

            if string_to_replace:
                text = (
                    text[:replace_start]
                    + expected_value
                    + text[replace_end:]
                )
                replacements[string_to_replace] = expected_value

        elif len(matches) == 1:
            for match in iteration:
                string_to_replace = match.group(2)
                replace_start, replace_end = match.span(2)
                if string_to_replace != expected_value:
                    text = (
                        text[:replace_start]
                        + expected_value
                        + text[replace_end:]
                    )
                    replacements[string_to_replace] = expected_value

    return text, replacements, duplicated_signals
