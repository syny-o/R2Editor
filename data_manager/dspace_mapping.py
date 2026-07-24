import re


def parse_dspace_mapping(text):
    definition_blocks = re.split(r"def ", text)
    header = definition_blocks[0]
    footer = definition_blocks[-1]
    definitions = []

    for definition_block in definition_blocks[1:-1]:
        variable_blocks = re.split(r"append", definition_block)
        definition_name = re.split(r"\(", variable_blocks[0])[0].strip()
        variables = []

        for variable_block in variable_blocks[1:]:
            quoted_parts = re.split('"', variable_block)
            if len(quoted_parts) < 4:
                continue
            variables.append(
                (
                    quoted_parts[1],
                    quoted_parts[2].strip(", "),
                    quoted_parts[3],
                )
            )

        definitions.append((definition_name, variables))

    return header, footer, definitions


def serialize_dspace_mapping(header, footer, definitions):
    output = header
    for definition_name, variables in definitions:
        output += f"def {definition_name}():\n"
        output += f"\t{definition_name}Var = []\n"

        for variable_name, value, path in variables:
            padded_name = f'{variable_name + chr(34) : <70}'
            output += (
                f'\t{definition_name}Var.append(["{padded_name}, '
                f'{value : <5},"{path}"])\n'
            )

        output += f"\treturn {definition_name}Var\n\n"

    return output + "def " + footer
