tooltips = {
    'MonitorVariablesCANape':
        """   
        <p align="center">     
        <font color=white>MonitorVariablesCANape&nbsp;=&nbsp;</font><font color=white>"</font><font color=#4da6ff>VARIABLE_1&nbsp;</font><font color=#4da6ff>VARIABLE_2&nbsp;</font><font color=#4da6ff>VARIABLE_N</font>,&nbsp;<font color=#4da6ff>TOTAL_TIME</font>,&nbsp;<font color=#4da6ff>SAMPLE_TIME</font>"
        </p>
        """,

    'MonitorVariables':
        """   
        <p align="center">     
        <font color=white>MonitorVariables&nbsp;=&nbsp;</font><font color=white>"</font><font color=#4da6ff>VARIABLE_1&nbsp;</font><font color=#4da6ff>VARIABLE_2&nbsp;</font><font color=#4da6ff>VARIABLE_N</font>,&nbsp;<font color=#4da6ff>TOTAL_TIME</font>,&nbsp;<font color=#4da6ff>SAMPLE_TIME</font>"
        </p>
        """,

    'GraphVariables':
        """
        GraphVariables&nbsp;=&nbsp;"<font color=#4da6ff>VARIABLE_1&nbsp;VARIABLE_2&nbsp;VARIABLE_N</font>"
        """,

    'VariableRisingInRange':
        """
        VariableRisingInRange&nbsp;=&nbsp;"<font color=#4da6ff>VARIABLE</font><font color=white>,</font>&nbsp;<font color=#4da6ff>SAMPLE_TIME</font><font color=white>,</font>&nbsp;<font color=#4da6ff>NUMBER_OF_RISES</font><font color=white>,</font>&nbsp;<font color=#4da6ff>TOLERANCE</font><font color=white>"</font>
        """,

    'VariableDroppingInRange':
        """
        VariableDroppingInRange&nbsp;=&nbsp;"<font color=#4da6ff>VARIABLE</font><font color=white>,</font>&nbsp;<font color=#4da6ff>SAMPLE_TIME</font><font color=white>,</font>&nbsp;<font color=#4da6ff>NUMBER_OF_DROPS</font><font color=white>,</font>&nbsp;<font color=#4da6ff>TOLERANCE</font><font color=white>"</font>
        """,

    'VariableRisingChanges':
        """
        VariableRisingChanges&nbsp;=&nbsp;"<font color=#4da6ff>VARIABLE</font><font color=white>,</font>&nbsp;<font color=#4da6ff>NUMBER_OF_RISES</font><font color=white>,</font>&nbsp;<font color=#4da6ff>SAMPLE_TIME</font><font color=white>,</font>&nbsp;<font color=#4da6ff>OPERATOR</font><font color=white>"</font>
        <div>&nbsp;</div>
        <div>OPERATOR:&nbsp; "<font color=#4da6ff>==</font>"&nbsp;OR&nbsp;"<font color=#4da6ff>&#60;</font>"&nbsp;OR&nbsp;"<font color=#4da6ff>&#62;</font>"</div>
        """,

    'VariableDroppingChanges':
        """
        VariableDroppingChanges&nbsp;=&nbsp;"<font color=#4da6ff>VARIABLE</font><font color=white>,</font>&nbsp;<font color=#4da6ff>NUMBER_OF_DROPS</font><font color=white>,</font>&nbsp;<font color=#4da6ff>SAMPLE_TIME</font><font color=white>,</font>&nbsp;<font color=#4da6ff>OPERATOR</font><font color=white>"</font>
        <div>&nbsp;</div>
        <div>OPERATOR:&nbsp; "<font color=#4da6ff>==</font>"&nbsp;OR&nbsp;"<font color=#4da6ff>&#60;</font>"&nbsp;OR&nbsp;"<font color=#4da6ff>&#62;</font>"</div>
        """,

    'VariableMaxInRange':
        """
        VariableMaxInRange&nbsp;=&nbsp;"<font color=#4da6ff>VARIABLE_NAME</font><font color=white>,</font>&nbsp;<font color=#4da6ff>MAX_VALUE</font><font color=white>,</font>&nbsp;<font color=#4da6ff>TOLERANCE</font><font color=white>"</font>
        """,

    'VariableMinInRange':
        """
        VariableMinInRange&nbsp;=&nbsp;"<font color=#4da6ff>VARIABLE_NAME</font><font color=white>,</font>&nbsp;<font color=#4da6ff>MIN_VALUE</font><font color=white>,</font>&nbsp;<font color=#4da6ff>TOLERANCE</font><font color=white>"</font>
        """,

    'CANape_GetObjectValue':
        """
        <font color=#4da6ff>CANapeCommand&nbsp;=&nbsp;</font><font color=white>"CANape_GetObjectValue(<font color=#4da6ff>OBJECT_NAME</font>,&nbsp;<font color=#4da6ff>OBJECT_VALUE</font>,&nbsp;<font color=#4da6ff>OPERATOR</font><font color=#aaaaaa>,&nbsp;TOLERANCE</font>)"
        <div>&nbsp;</div>
        <div>OPERATOR:&nbsp; "<font color=#4da6ff>==</font>"&nbsp;OR&nbsp;"<font color=#4da6ff>=</font>"&nbsp;OR&nbsp;"<font color=#4da6ff>&#60;</font>"&nbsp;OR&nbsp;"<font color=#4da6ff>&#62;</font>"&nbsp;OR&nbsp;"<font color=#4da6ff>&#60;&#62;</font>"</div>
        """,

    'VariableSequence':
        """
        <p align="center">   
        VariableSequence&nbsp;=&nbsp;"<font color=#4da6ff>VARIABLE_NAME</font>,&nbsp;<font color=#4da6ff>VALUE_1&nbsp;VALUE_2&nbsp;VALUE_N</font>"
        <div>&nbsp;</div>
        <div><font color=#4da6ff>Example:</font>&nbsp;<font color=white>VariableSequence = "PbcOutMotorCommandRight, 5 27 54 5"</font></div>
        </p>
        """,

    'PbcInApplyReleaseRequest':
        """
        <font color=white>Variable: </font><font color=#4da6ff>PbcInApplyReleaseRequest</font> 
        <div>&nbsp;</div>
        <div><font color=white>5</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>None</font></div>
        <div><font color=white>27</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>ParkApply</font></div>
        <div><font color=white>40</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>HoldApply</font></div>
        <div><font color=white>54</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Release</font></div>
        <div><font color=white>66</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>DynamicApply</font></div>
        <div><font color=white>92</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>RollerBenchApply</font></div>
        <div><font color=white>111</font><span>&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>PadAdjustment</font></div>
        """,

    'PbcInDiagRequest':
        """
        <font color=white>Variable: </font><font color=#4da6ff>PbcInDiagRequest</font> 
        <div>&nbsp;</div>
        <div><font color=white>5</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>None</font></div>
        <div><font color=white>27</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>OpenBrakeRearLeft</font></div>
        <div><font color=white>40</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>OpenBrakeRearRight</font></div>
        <div><font color=white>54</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>OpenBrakeBoth</font></div>
        <div><font color=white>66</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>CloseBrakeRearLeft</font></div>
        <div><font color=white>92</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>CloseBrakeRearRight</font></div>
        <div><font color=white>111</font><span>&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>CloseBrakeBoth</font></div>
        <div><font color=white>113</font><span>&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>TouchBrakeRearLeft</font></div>
        <div><font color=white>142</font><span>&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>TouchBrakeRearRight</font></div>
        <div><font color=white>144</font><span>&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>TouchBrakeBoth</font></div>
        <div><font color=white>163</font><span>&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>StepCloseRearLeft</font></div>
        <div><font color=white>189</font><span>&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>StepCloseRearRight</font></div>
        <div><font color=white>201</font><span>&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>StepCloseBoth</font></div>
        <div><font color=white>215</font><span>&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>AssemblyCheck</font></div>
        <div><font color=white>228</font><span>&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>EnterMaintenanceMode</font></div>
        <div><font color=white>250</font><span>&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>ExitMaintenanceMode</font></div>
        """,

    'PbcOutDiagRequestAcknowledge':
        """
        <font color=white>Variable: </font><font color=#4da6ff>PbcOutDiagRequestAcknowledge</font> 
        <div>&nbsp;</div>
        <div><font color=white>5</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>None</font></div>
        <div><font color=white>27</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>OpenBrakeRearLeft</font></div>
        <div><font color=white>40</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>OpenBrakeRearRight</font></div>
        <div><font color=white>54</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>OpenBrakeBoth</font></div>
        <div><font color=white>66</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>CloseBrakeRearLeft</font></div>
        <div><font color=white>92</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>CloseBrakeRearRight</font></div>
        <div><font color=white>111</font><span>&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>CloseBrakeBoth</font></div>
        <div><font color=white>113</font><span>&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>TouchBrakeRearLeft</font></div>
        <div><font color=white>142</font><span>&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>TouchBrakeRearRight</font></div>
        <div><font color=white>144</font><span>&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>TouchBrakeBoth</font></div>
        <div><font color=white>163</font><span>&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>StepCloseRearLeft</font></div>
        <div><font color=white>189</font><span>&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>StepCloseRearRight</font></div>
        <div><font color=white>201</font><span>&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>StepCloseBoth</font></div>
        <div><font color=white>215</font><span>&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>AssemblyCheck</font></div>
        <div><font color=white>228</font><span>&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>EnterMaintenanceMode</font></div>
        <div><font color=white>250</font><span>&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>ExitMaintenanceMode</font></div>
        """,

    'PbcOutActuatorStateLeft':
        """
        <font color=white>Variable: </font><font color=#4da6ff>PbcOutActuatorStateLeft</font> 
        <div>&nbsp;</div>
        <div><font color=white>27</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>ParkApplied</font></div>
        <div><font color=white>40</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>HoldApplied</font></div>
        <div><font color=white>54</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Released</font></div>
        <div><font color=white>113</font><span>&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Applying</font></div>
        <div><font color=white>142</font><span>&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Releasing</font></div>
        <div><font color=white>144</font><span>&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Completely Released</font></div>
        <div><font color=white>163</font><span>&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Unknown</font></div>
        """,

    'PbcOutActuatorStateRight':
        """
        <font color=white>Variable: </font><font color=#4da6ff>PbcOutActuatorStateRight</font> 
        <div>&nbsp;</div>
        <div><font color=white>27</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>ParkApplied</font></div>
        <div><font color=white>40</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>HoldApplied</font></div>
        <div><font color=white>54</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Released</font></div>
        <div><font color=white>113</font><span>&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Applying</font></div>
        <div><font color=white>142</font><span>&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Releasing</font></div>
        <div><font color=white>144</font><span>&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Completely Released</font></div>
        <div><font color=white>163</font><span>&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Unknown</font></div>
        """,

    'PbcOutMotorCommandLeft':
        """
        <font color=white>Variable: </font><font color=#4da6ff>PbcOutMotorCommandLeft</font> 
        <div>&nbsp;</div>
        <div><font color=white>5</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>None</font></div>
        <div><font color=white>27</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Apply</font></div>
        <div><font color=white>40</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Release</font></div>
        <div><font color=white>54</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Stop</font></div>
        <div><font color=white>66</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Freerun</font></div>
        """,

    'PbcOutMotorCommandRight':
        """
        <font color=white>Variable: </font><font color=#4da6ff>PbcOutMotorCommandRight</font> 
        <div>&nbsp;</div>
        <div><font color=white>5</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>None</font></div>
        <div><font color=white>27</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Apply</font></div>
        <div><font color=white>40</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Release</font></div>
        <div><font color=white>54</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Stop</font></div>
        <div><font color=white>66</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Freerun</font></div>
        """,

    'PbcInRollerbenchActive':
        """
        <font color=white>Variable: </font> <font color=#4da6ff>PbcInRollerbenchActive</font> 
        <div>&nbsp;</div>
        <div><font color=white>5</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Active</font></div>
        <div><font color=white>27</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Inactive</font></div>
        """,

    'PbcOutDiagRequestStatus':
        """
        <font color=white>Variable: </font> <font color=#4da6ff>PbcOutDiagRequestStatus</font> 
        <div>&nbsp;</div>
        <div><font color=white>5</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Idle</font></div>
        <div><font color=white>27</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Started</font></div>
        <div><font color=white>40</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Running</font></div>
        <div><font color=white>54</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Done</font></div>
        <div><font color=white>66</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Error</font></div>
        """,

    'PbcInHostAvailabilityLeft':
        """
        <font color=white>Variable: </font> <font color=#4da6ff>PbcInHostAvailabilityLeft</font> 
        <div>&nbsp;</div>
        <div><font color=white>5</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>None</font></div>
        <div><font color=white>27</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Apply</font></div>
        <div><font color=white>40</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Release</font></div>
        <div><font color=white>54</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Apply and Release</font></div>
        """,

    'PbcInHostAvailabilityRight':
        """
        <font color=white>Variable: </font> <font color=#4da6ff>PbcInHostAvailabilityRight</font> 
        <div>&nbsp;</div>
        <div><font color=white>5</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>None</font></div>
        <div><font color=white>27</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Apply</font></div>
        <div><font color=white>40</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Release</font></div>
        <div><font color=white>54</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Apply and Release</font></div>
        """,

    'PbcOutFaultStatus_00':
        """
        Variable:&nbsp;<font color=#4da6ff>PbcOutFaultStatus_00</font>
        <div>&nbsp;</div>
        <div>DTC&nbsp;Name:&nbsp;<font color=#4da6ff>FC_ACTUATOR_BROKEN_LEFT</font></div> 
        <div>&nbsp;</div>
        <div><font color=white>5</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>NoResult</font></div>
        <div><font color=white>27</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>PrePassed</font></div>
        <div><font color=white>40</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Passed</font></div>
        <div><font color=white>54</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>PreFailed</font></div>
        <div><font color=white>66</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Failed</font></div>
        <div><font color=white>92</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>NotSupported</font></div>
        """,

    'PbcOutFaultStatus_01':
        """
        Variable:&nbsp;<font color=#4da6ff>PbcOutFaultStatus_01</font>
        <div>&nbsp;</div>
        <div>DTC&nbsp;Name:&nbsp;<font color=#4da6ff>FC_ACTUATOR_BROKEN_RIGHT</font></div> 
        <div>&nbsp;</div>
        <div><font color=white>5</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>NoResult</font></div>
        <div><font color=white>27</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>PrePassed</font></div>
        <div><font color=white>40</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Passed</font></div>
        <div><font color=white>54</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>PreFailed</font></div>
        <div><font color=white>66</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Failed</font></div>
        <div><font color=white>92</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>NotSupported</font></div>
        """,

    'PbcOutFaultStatus_02':
        """
        Variable:&nbsp;<font color=#4da6ff>PbcOutFaultStatus_02</font>
        <div>&nbsp;</div>
        <div>DTC&nbsp;Name:&nbsp;<font color=#4da6ff>FC_CANT_ACHIEVE_CLEARANCE_LEFT</font></div> 
        <div>&nbsp;</div>
        <div><font color=white>5</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>NoResult</font></div>
        <div><font color=white>27</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>PrePassed</font></div>
        <div><font color=white>40</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Passed</font></div>
        <div><font color=white>54</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>PreFailed</font></div>
        <div><font color=white>66</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Failed</font></div>
        <div><font color=white>92</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>NotSupported</font></div>
        """,

    'PbcOutFaultStatus_03':
        """
        Variable:&nbsp;<font color=#4da6ff>PbcOutFaultStatus_03</font>
        <div>&nbsp;</div>
        <div>DTC&nbsp;Name:&nbsp;<font color=#4da6ff>FC_CANT_ACHIEVE_CLEARANCE_RIGHT</font></div> 
        <div>&nbsp;</div>
        <div><font color=white>5</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>NoResult</font></div>
        <div><font color=white>27</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>PrePassed</font></div>
        <div><font color=white>40</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Passed</font></div>
        <div><font color=white>54</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>PreFailed</font></div>
        <div><font color=white>66</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Failed</font></div>
        <div><font color=white>92</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>NotSupported</font></div>
        """,

    'PbcOutFaultStatus_04':
        """
        Variable:&nbsp;<font color=#4da6ff>PbcOutFaultStatus_04</font>
        <div>&nbsp;</div>
        <div>DTC&nbsp;Name:&nbsp;<font color=#4da6ff>FC_CANT_ACHIEVE_CLAMP_LEFT</font></div> 
        <div>&nbsp;</div>
        <div><font color=white>5</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>NoResult</font></div>
        <div><font color=white>27</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>PrePassed</font></div>
        <div><font color=white>40</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Passed</font></div>
        <div><font color=white>54</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>PreFailed</font></div>
        <div><font color=white>66</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Failed</font></div>
        <div><font color=white>92</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>NotSupported</font></div>
        """,

    'PbcOutFaultStatus_05':
        """
        Variable:&nbsp;<font color=#4da6ff>PbcOutFaultStatus_05</font>
        <div>&nbsp;</div>
        <div>DTC&nbsp;Name:&nbsp;<font color=#4da6ff>FC_CANT_ACHIEVE_CLAMP_RIGHT</font></div> 
        <div>&nbsp;</div>
        <div><font color=white>5</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>NoResult</font></div>
        <div><font color=white>27</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>PrePassed</font></div>
        <div><font color=white>40</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Passed</font></div>
        <div><font color=white>54</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>PreFailed</font></div>
        <div><font color=white>66</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Failed</font></div>
        <div><font color=white>92</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>NotSupported</font></div>
        """,

    'PbcOutFaultStatus_06':
        """
        Variable:&nbsp;<font color=#4da6ff>PbcOutFaultStatus_06</font>
        <div>&nbsp;</div>
        <div>DTC&nbsp;Name:&nbsp;<font color=#4da6ff>FC_HIGH_MOTOR_FREE_RUN_CURRENT_RIGHT</font></div> 
        <div>&nbsp;</div>
        <div><font color=white>5</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>NoResult</font></div>
        <div><font color=white>27</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>PrePassed</font></div>
        <div><font color=white>40</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Passed</font></div>
        <div><font color=white>54</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>PreFailed</font></div>
        <div><font color=white>66</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Failed</font></div>
        <div><font color=white>92</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>NotSupported</font></div>
        """,

    'PbcOutFaultStatus_07':
        """
        Variable:&nbsp;<font color=#4da6ff>PbcOutFaultStatus_07</font>
        <div>&nbsp;</div>
        <div>DTC&nbsp;Name:&nbsp;<font color=#4da6ff>FC_HIGH_MOTOR_FREE_RUN_CURRENT_RIGHT</font></div> 
        <div>&nbsp;</div>
        <div><font color=white>5</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>NoResult</font></div>
        <div><font color=white>27</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>PrePassed</font></div>
        <div><font color=white>40</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Passed</font></div>
        <div><font color=white>54</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>PreFailed</font></div>
        <div><font color=white>66</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Failed</font></div>
        <div><font color=white>92</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>NotSupported</font></div>
        """,

    'PbcOutFaultStatus_08':
        """
        Variable:&nbsp;<font color=#4da6ff>PbcOutFaultStatus_08</font>
        <div>&nbsp;</div>
        <div>DTC&nbsp;Name:&nbsp;<font color=#4da6ff>FC_VOLTAGE_BELOW_ACTUATION_INHIBIT</font></div> 
        <div>&nbsp;</div>
        <div><font color=white>5</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>NoResult</font></div>
        <div><font color=white>27</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>PrePassed</font></div>
        <div><font color=white>40</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Passed</font></div>
        <div><font color=white>54</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>PreFailed</font></div>
        <div><font color=white>66</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Failed</font></div>
        <div><font color=white>92</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>NotSupported</font></div>
        """,

    'PbcOutFaultStatus_09':
        """
        Variable:&nbsp;<font color=#4da6ff>PbcOutFaultStatus_09</font>
        <div>&nbsp;</div>
        <div>DTC&nbsp;Name:&nbsp;<font color=#4da6ff>FC_VOLTAGE_ABOVE_ACTUATION_INHIBIT</font></div> 
        <div>&nbsp;</div>
        <div><font color=white>5</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>NoResult</font></div>
        <div><font color=white>27</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>PrePassed</font></div>
        <div><font color=white>40</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Passed</font></div>
        <div><font color=white>54</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>PreFailed</font></div>
        <div><font color=white>66</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Failed</font></div>
        <div><font color=white>92</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>NotSupported</font></div>
        """,

    'PbcOutFaultStatus_10':
        """
        Variable:&nbsp;<font color=#4da6ff>PbcOutFaultStatus_10</font>
        <div>&nbsp;</div>
        <div>DTC&nbsp;Name:&nbsp;<font color=#4da6ff>FC_ACTUATOR_POSITION_INCOHERENT</font></div> 
        <div>&nbsp;</div>
        <div><font color=white>5</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>NoResult</font></div>
        <div><font color=white>27</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>PrePassed</font></div>
        <div><font color=white>40</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Passed</font></div>
        <div><font color=white>54</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>PreFailed</font></div>
        <div><font color=white>66</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Failed</font></div>
        <div><font color=white>92</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>NotSupported</font></div>
        """,

    'PbcOutFaultStatus_11':
        """
        Variable:&nbsp;<font color=#4da6ff>PbcOutFaultStatus_11</font>
        <div>&nbsp;</div>
        <div>DTC&nbsp;Name:&nbsp;<font color=#4da6ff>FC_ACTUATOR_STATE_UNKNOWN</font></div> 
        <div>&nbsp;</div>
        <div><font color=white>5</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>NoResult</font></div>
        <div><font color=white>27</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>PrePassed</font></div>
        <div><font color=white>40</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Passed</font></div>
        <div><font color=white>54</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>PreFailed</font></div>
        <div><font color=white>66</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Failed</font></div>
        <div><font color=white>92</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>NotSupported</font></div>
        """,

    'PbcOutFaultStatus_16':
        """
        Variable:&nbsp;<font color=#4da6ff>PbcOutFaultStatus_16</font>
        <div>&nbsp;</div>
        <div>DTC&nbsp;Name:&nbsp;<font color=#4da6ff>FC_PBC_IN_MAINTENANCE_MODE</font></div> 
        <div>&nbsp;</div>
        <div><font color=white>5</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>NoResult</font></div>
        <div><font color=white>27</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>PrePassed</font></div>
        <div><font color=white>40</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Passed</font></div>
        <div><font color=white>54</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>PreFailed</font></div>
        <div><font color=white>66</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>Failed</font></div>
        <div><font color=white>92</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>NotSupported</font></div>
        """,

    'IF':
        """
        <font color=#4da6ff>IF STATEMENT</font>
        <div>&nbsp;</div> 
        <div><font color=white>IF</font><span>&nbsp;&nbsp;</span><font color=#4da6ff>(var = value)</font><font color=white>AND/OR</font> <font color=#4da6ff>(var = value2)</font> <font color=white>THEN</font></div>
        <div>&nbsp;</div>        
        <div><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>condition_1 = value_1</font></div>
        <div><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>condition_2 = value_2</font></div>
        <div><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>condition_N = value_N</font></div>
        <div>&nbsp;</div>        
        <div><font color=white>ELSE</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></div>
        <div>&nbsp;</div>        
        <div><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>condition_1 = value_1</font></div>
        <div><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>condition_2 = value_2</font></div>
        <div><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>condition_N = value_N</font></div>
        <div>&nbsp;</div>        
        <div><font color=white>ENDIF</font></div>
        """,

    'FOR':
        """
        <font color=#4da6ff>FOR CYCLE</font>
        <div>&nbsp;</div> 
        <div><font color=white>FOR</font><span>&nbsp;&nbsp;</span><font color=#4da6ff>variable = value_1 value_2 ... value_N <font color=white>DO</font></div>
        <div>&nbsp;</div>
        <div><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>{PROGRAM BODY}</font></div>
        <div>&nbsp;</div>
        <div><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>condition_name = variable</font></div>
        <div>&nbsp;</div>          
        <div><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><font color=#4da6ff>{PROGRAM BODY}</font></div>
        <div>&nbsp;</div>        
        <div><font color=white>NEXT</font><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></div>
        """,

}
