import re

from pbc_patterns_scripts import patterns


def normalise_text(text):
    for key, value in patterns.items():
        # find all matches for each variable
        pattern = key
        iteration = pattern.finditer(text)

        for i in iteration:

            string_to_replace = i.group()
            print(string_to_replace)

            text = text.replace(string_to_replace, value)

    return text  


text = """

        MonitorVariablesCANape = "PbcIn.FaultRecoveryRequest._7_ PbcIn.FaultRecoveryRequest._11_ PbcIn.MotorCurrentRight._0_ PbcOutDebug.FaultStatus7 PbcOutDebug.FaultStatus._7_ PbcOutDebug.FaultStatus._11_ PbcIn.ApplyReleaseRequest,60000,20"
    
    """


text = normalise_text(text)

# text = re.sub(r"""_?PbcOut(Debug)?\.?_?FaultStatus.?[_\[]?(?P<number>\d\d)\]?_?""", r"""PbcOutFaultStatus_\g<number>""", text)

# text = re.sub(r"""_?PbcOut(Debug)?\.?_?FaultStatus.?[_\[]?(?P<number>\d)(?!\d)\]?_?""", r"""PbcOutFaultStatus_0\g<number>""", text)



print(text)