from vda_normaliser.pbc_patterns_scripts import patterns


def open_file(path):
    with open(path, 'r') as f:
        return f.read()


def save_file(path, text):
    with open(path, 'w') as f:
        f.write(text)


def normalise_text(text):

    for key, value in patterns.items():
        # find all matches for each variable
        pattern = key
        iteration = pattern.finditer(text)

        # check how many matches have been found (in current iteration)
        matches = pattern.findall(text)

        # if multiple matches (variable definitions) have been found:
        if len(matches) > 1:
            string_to_replace = None
            smallest_match_length = 1000
            for i in iteration:

                # check if one of the matches is in correct form (pattern value) --> no replacement needed
                if i.group(1) == value:
                    string_to_replace = None  # 2021-07-27 FIXED BUG (f.e. Saic AS28 M2M3 issue)
                    break

                # if all matches are in wrong form, choose shortest one and replace it with correct pattern value
                elif len(i.group(1)) < smallest_match_length:
                    smallest_match_length = len(i.group(1))
                    string_to_replace = i.group(1)
                    string_to_replace_start, string_to_replace_end = i.span(1)

            if string_to_replace:
                text = text[:string_to_replace_start] + value + text[string_to_replace_end:]

        # only one match at all has been found
        elif len(matches) == 1:
            for i in iteration:

                string_to_replace = i.group(1)
                string_to_replace_start, string_to_replace_end = i.span(1)

                if string_to_replace != value:
                    text = text[:string_to_replace_start] + value + text[string_to_replace_end:]

    return text



def normalise_file(file_path):

    text_2_normalise = open_file(file_path)

    normalised_text = normalise_text(text_2_normalise)

    save_file(file_path, normalised_text)

