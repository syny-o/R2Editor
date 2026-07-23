PBC_VARIABLE_COMMANDS = {
    "MonitorVariablesCANape",
    "MonitorVariablesCanape",
    "VariableSequence",
    "CANapeCommand",
}

SPECIAL_COMMAND_TEMPLATES = {
    "MonitorVariablesCANape": (' = ", 100000, 10"', 13),
    "MonitorVariablesCanape": (' = ", 100000, 10"', 13),
    "MonitorVariables": (' = ", 100000, 10"', 13),
    "GraphVariables": (' = ""', 1),
    "VariableRisingInRange": (' = ""', 1),
    "VariableDroppingInRange": (' = ""', 1),
    "VariableRisingChanges": (' = ""', 1),
    "VariableDroppingChanges": (' = ""', 1),
    "VariableMaxInRange": (' = ""', 1),
    "VariableMinInRange": (' = ""', 1),
    "CANapeCommand": (' = "CANape_GetObjectValue()"', 2),
    "VariableSequence": (' = ""', 1),
}

EQUAL_SPACING_EXCLUDED_COMMANDS = (
    "MonitorVariablesCANape",
    "MonitorVariablesCanape",
    "MonitorVariables",
    "GraphVariables",
    "VariableSequence",
    "CANapeCommand",
)


def completion_model_name(actual_text, condition_names=()):
    if actual_text in PBC_VARIABLE_COMMANDS:
        return "pbc_variables"
    if actual_text == "GraphVariables":
        return "graph_variables"
    if actual_text == "MonitorVariables":
        return "dspace_variables"
    if actual_text in condition_names:
        return "values"
    return "conditions"
