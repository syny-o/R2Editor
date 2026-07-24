import re


def _extract(pattern, text, default=""):
    match = re.search(pattern, text)
    return match.group(1) if match else default


def parse_condition_file(text):
    condition_sections = re.split(r"<Condition ", text)
    header = condition_sections.pop(0)
    conditions = []

    for condition_section in condition_sections:
        condition = {
            "name": _extract(
                r'Name\s*=\s*"([^"]+)',
                condition_section,
            ),
            "category": _extract(
                r'Type\s*=\s*"([^"]+)',
                condition_section,
            ),
            "values": [],
        }

        for value_section in re.split(r"<Value ", condition_section)[1:]:
            value = {
                "name": _extract(r'Name\s*=\s*"([^"]+)', value_section),
                "category": _extract(
                    r'Type\s*=\s*"([^"]+)',
                    value_section,
                ),
                "test_steps": [],
            }

            for test_step_section in re.split("TS", value_section)[1:]:
                value["test_steps"].append(
                    {
                        "name": _extract(
                            r'Name=\s*"([^"]+)',
                            test_step_section,
                        ),
                        "action": _extract(
                            r'A\s*=\s*"([^"]+)',
                            test_step_section,
                        ),
                        "nominal": _extract(
                            r'Nominal\s*=\s*"([^"]+)',
                            test_step_section,
                        ),
                        "comment": _extract(
                            r'Comment\s*=\s*"([^"]+)',
                            test_step_section,
                        ),
                    }
                )

            condition["values"].append(value)

        conditions.append(condition)

    return header, conditions


def serialize_condition_file(header, conditions):
    output_lines = [header]

    for condition in conditions:
        output_lines.append(
            f'\t<Condition Name="{condition["name"]}" '
            f'Type="{condition["category"]}">'
        )
        for value in condition["values"]:
            output_lines.append(
                f'\t\t<Value Name="{value["name"]}" '
                f'Type="{value["category"]}">'
            )
            for test_step in value["test_steps"]:
                output_lines.append(
                    f'\t\t\t<TS Name="{test_step["name"]}" '
                    f'A="{test_step["action"]}" '
                    f'Nominal="{test_step["nominal"]}" '
                    f'Comment="{test_step["comment"]}" />'
                )
            output_lines.append("\t\t</Value>")
        output_lines.append("\t</Condition>")

    output_lines.append("</Conditions>")
    return "\n".join(output_lines)
