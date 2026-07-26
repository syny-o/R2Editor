from text_editor.tooltips.content import TooltipEntry
from text_editor.tooltips.legacy import tooltips as legacy_tooltips


COMMAND_TOOLTIPS = {
    'MonitorVariablesCANape': TooltipEntry(
        title='MonitorVariablesCANape',
        signature=(
            'MonitorVariablesCANape = '
            '"VARIABLE_1 VARIABLE_2 VARIABLE_N, TOTAL_TIME, SAMPLE_TIME"'
        ),
        parameters=(
            ('VARIABLE_1 … VARIABLE_N', 'CANape variables to monitor'),
            ('TOTAL_TIME', 'Total monitoring time'),
            ('SAMPLE_TIME', 'Sampling interval'),
        ),
    ),
    'MonitorVariables': TooltipEntry(
        title='MonitorVariables',
        signature=(
            'MonitorVariables = '
            '"VARIABLE_1 VARIABLE_2 VARIABLE_N, TOTAL_TIME, SAMPLE_TIME"'
        ),
        parameters=(
            ('VARIABLE_1 … VARIABLE_N', 'Variables to monitor'),
            ('TOTAL_TIME', 'Total monitoring time'),
            ('SAMPLE_TIME', 'Sampling interval'),
        ),
    ),
    'GraphVariables': TooltipEntry(
        title='GraphVariables',
        signature='GraphVariables = "VARIABLE_1 VARIABLE_2 VARIABLE_N"',
    ),
    'VariableRisingInRange': TooltipEntry(
        title='VariableRisingInRange',
        signature=(
            'VariableRisingInRange = '
            '"VARIABLE, SAMPLE_TIME, NUMBER_OF_RISES, TOLERANCE"'
        ),
    ),
    'VariableDroppingInRange': TooltipEntry(
        title='VariableDroppingInRange',
        signature=(
            'VariableDroppingInRange = '
            '"VARIABLE, SAMPLE_TIME, NUMBER_OF_DROPS, TOLERANCE"'
        ),
    ),
    'VariableRisingChanges': TooltipEntry(
        title='VariableRisingChanges',
        signature=(
            'VariableRisingChanges = '
            '"VARIABLE, NUMBER_OF_RISES, SAMPLE_TIME, OPERATOR"'
        ),
        parameters=(('OPERATOR', '==, < or >'),),
    ),
    'VariableDroppingChanges': TooltipEntry(
        title='VariableDroppingChanges',
        signature=(
            'VariableDroppingChanges = '
            '"VARIABLE, NUMBER_OF_DROPS, SAMPLE_TIME, OPERATOR"'
        ),
        parameters=(('OPERATOR', '==, < or >'),),
    ),
    'VariableMaxInRange': TooltipEntry(
        title='VariableMaxInRange',
        signature='VariableMaxInRange = "VARIABLE, MAX_VALUE, TOLERANCE"',
    ),
    'VariableMinInRange': TooltipEntry(
        title='VariableMinInRange',
        signature='VariableMinInRange = "VARIABLE, MIN_VALUE, TOLERANCE"',
    ),
    'CANape_GetObjectValue': TooltipEntry(
        title='CANape_GetObjectValue',
        signature=(
            'CANapeCommand = '
            '"CANape_GetObjectValue(OBJECT_NAME, OBJECT_VALUE, OPERATOR, '
            'TOLERANCE)"'
        ),
        parameters=(('OPERATOR', '==, =, <, > or <>'),),
    ),
    'VariableSequence': TooltipEntry(
        title='VariableSequence',
        signature=(
            'VariableSequence = '
            '"VARIABLE_NAME, VALUE_1 VALUE_2 VALUE_N"'
        ),
        example=(
            'VariableSequence = '
            '"PbcOutMotorCommandRight, 5 27 54 5"'
        ),
    ),
    'IF': TooltipEntry(
        title='IF statement',
        signature='IF (variable = value) AND/OR (variable = value) THEN',
        description='Conditional execution block terminated by ENDIF.',
        minimum_width=620,
        structure=(
            'IF (variable = value) THEN',
            '    PROGRAM_BODY',
            'ELSE',
            '    PROGRAM_BODY',
            'ENDIF',
        ),
    ),
    'FOR': TooltipEntry(
        title='FOR cycle',
        signature='FOR variable = value_1 value_2 ... value_N DO',
        description='Repeats the block for every value and ends with NEXT.',
        minimum_width=620,
        structure=(
            'FOR variable = value_1 value_2 ... value_N DO',
            '    PROGRAM_BODY',
            'NEXT',
        ),
    ),
}

COMMAND_TOOLTIPS.update({
    'AND': COMMAND_TOOLTIPS['IF'],
    'DO': COMMAND_TOOLTIPS['FOR'],
    'ELSE': COMMAND_TOOLTIPS['IF'],
    'ENDIF': COMMAND_TOOLTIPS['IF'],
    'NEXT': COMMAND_TOOLTIPS['FOR'],
    'OR': COMMAND_TOOLTIPS['IF'],
    'THEN': COMMAND_TOOLTIPS['IF'],
})


tooltips = {
    **legacy_tooltips,
    **COMMAND_TOOLTIPS,
}
