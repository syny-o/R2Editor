import re

old_line = 'MonitorVariables = " PbcIn.ApplyReleaseRequest  PbcOutDebug.MotorCommandLeft PbcOutDebug.MotorCommandRight , 5000 , 20"'
old_line2 = 'GraphVariables =  "PbcOutDebug.MotorCommandLeft   PbcOutDebug.MotorCommandRight "'

PATTERN_MONITOR_VAR =  re.compile(r'(?P<command>MonitorVariables(CANape)?)\s*=\s*"(?P<variables>[\d\w_.\s]+),\s*(?P<time>\d+)\s*,\s*(?P<sample_time>\d+)\s*"', flags=re.IGNORECASE)
PATTERN_GRAPH_VAR =  re.compile(r'GraphVariables\s*=\s*"(?P<variables>[\d\w_.\s]+)"', flags=re.IGNORECASE)

def handle_syntax(string_line):
    # handle MonitorVariables/CANape
    if match := PATTERN_MONITOR_VAR.search(string_line):
        command = match.group("command")
        raw_variables = match.group("variables")
        variables = raw_variables.split()
        variables = [v.strip() for v in variables]
        time = match.group("time")
        sample_time = match.group("sample_time")
        return f'{command} = "{" ".join(variables)},{time},{sample_time}"'
    # handle GraphVariables
    elif match := PATTERN_GRAPH_VAR.search(string_line):
        raw_variables = match.group("variables")
        variables = raw_variables.split()
        variables = [v.strip() for v in variables]
        return f'GraphVariables = "{" ".join(variables)}"'        
    
    else:
        return string_line


new_line = handle_syntax(old_line)
new_line2 = handle_syntax(old_line2)

print(new_line)
print(new_line2)

    
    

