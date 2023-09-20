class TemplateTestCase:

    test_case_body_testable = """\

    $COM: "HIL initialisation" $
        HIL = Init;
    
    $COM: "Set preconditions" $
        PRE = StaticMode
        PRE = EPBReleased
        PRE = IgnOnWait

    $COM: "Monitor Variables" $
        MonitorVariables = "Clampforce_L Clampforce_R,10000,20"
        MonitorVariablesCANape = "PbcOutActuatorStateLeft PbcOutActuatorStateRight,10000,20"

    $COM: "Perform the test" $
        Brake = Apply

    $COM: "Check PBC Status" $
        CANapeCommand = "CANape_GetObjectValue(PbcOutActuatorStateLeft,27,==)"
        CANapeCommand = "CANape_GetObjectValue(PbcOutActuatorStateRight,27,==)"

    $COM: "Check: EPB applied" $
        Clampforce.Right = Applied
        Clampforce.Left = Applied
        EPB.Status = Applied

    $COM: "Create Graph(s)" $
        GraphVariables = "Clampforce_L Clampforce_R"
        GraphVariables = "PbcOutActuatorStateLeft PbcOutActuatorStateRight"

    $COM: "Read faults" $
        ReadDTC = NoDTC

    $COM: "HIL reset" $
        HIL = Reset
                """

    test_case_body_not_testable = """\

    $COM: "HIL Not Testable" $"""                

    def __init__(self, req_id=None, req_text=None, is_testable=True) -> None:
        self.req_id = req_id
        self.req_text = req_text
        self.expected_result = "1" if is_testable else "8"

    def add_header(self):
        if self.req_id and self.req_text:
            
            req_text_list = self.req_text.splitlines()
            req_text_list_commented = ["' " + line for line in req_text_list]

            header_text = "\n".join(req_text_list_commented)
            
            header_text += "\n"

            header_text += \
                f"""\
TESTCASE "TC for {self.req_id}" EXPECTEDRESULT {self.expected_result}
	$SEV: 10$	$CAT: 3$
	$REF: "{self.req_id}"$
"""

            return header_text

        else:
            return f"""\
TESTCASE "NEW TESTCASE" EXPECTEDRESULT 1
	$SEV: 10$	$CAT: 3$
	$REF: ""$
"""



    def generate_tc_template(self):
        if self.expected_result == "1":
            full_tc_text = self.add_header() + self.test_case_body_testable
        else:
            full_tc_text = self.add_header() + self.test_case_body_not_testable
            
        return full_tc_text