import re

# CREATE PATTERNS DICTIONARY
patterns = {}

#######################################################################################
########################################  PBC IN  #####################################
#######################################################################################
# DRIVEAWAY
key = re.compile(r'( MEASUREMENT| CHARACTERISTIC)\s+(_?PbcIn.?_?DriveAway[A-Za-z]*Ind[a-z]*[^\s/]*)')
value = 'PbcInDriveAwayIntentionIndication'
patterns.update({key : value})
# STANDARD SIGNALS
pbc_in_signals = [
    'ApplyReleaseRequest',
    'PowerSupplyState',
    'HostAvailabilityLeft',
    'HostAvailabilityRight',
    'MotorDriverSupplyVoltage',
    'MotorDriverStateLeft',
    'MotorDriverStateRight',
    'MasterCylinderPressure',
    'WheelPressureFrontLeft',
    'WheelPressureFrontRight',
    'WheelPressureRearLeft',
    'WheelPressureRearRight',
    'LongAcceleration',
    'VehicleAmbientTemperature',
    'WheelPulseFrontLeft',
    'WheelPulseFrontRight',
    'WheelPulseRearLeft',
    'WheelPulseRearRight',
    'WheelSpeedFrontLeft',
    'WheelSpeedFrontRight',
    'WheelSpeedRearLeft',
    'WheelSpeedRearRight',
    'RollerbenchActive',
    'HpsAcknowledge',
    'HpsAvailability',
    'UnexpectedPowerdown',
    'DiagOperationMode',
    'PbcSleepTime',
    'DiagRequest',
    'Mileage',
    'EngineCranking'
]





for signal in pbc_in_signals:
    key = re.compile(r'( MEASUREMENT| CHARACTERISTIC)\s+(_?PbcIn.?_?' + signal + r'[^\s/]*)')
    value = 'PbcIn' + signal
    patterns.update({key : value})

# HOST SW VERSION
for number in range(0, 6):
    p_key = f'( MEASUREMENT| CHARACTERISTIC)\\s+(_?PbcIn\\.?_?HostSoftwareVersion.?[_\\[]?0{number}\\]?[^\\s/]*)'
    p_value = 'PbcInHostSoftwareVersion_0' + str(number)
    patterns.update({re.compile(p_key): p_value})

    p_key = f'( MEASUREMENT| CHARACTERISTIC)\\s+(_?PbcIn\\.?_?HostSoftwareVersion.?[_\\[]?{number}\\]?\\D[^\\s/^"]*)'
    p_value = 'PbcInHostSoftwareVersion_0' + str(number) + ' '
    patterns.update({re.compile(p_key): p_value})


# FAULT RECOVERY
for number in range(0, 20):
    if number < 10:
        p_key = f'( MEASUREMENT| CHARACTERISTIC)\\s+(_?PbcIn\\.?_?FaultRecoveryRequest.?[_\\[]?0{number}\\]?[^\\s/]*)'
        p_value = 'PbcInFaultRecoveryRequest_0' + str(number)
        patterns.update({re.compile(p_key): p_value})

        p_key = f'( MEASUREMENT| CHARACTERISTIC)\\s+(_?PbcIn\\.?_?FaultRecoveryRequest.?[_\\[]?{number}\\]?\\D[^\\s/^"]*)'
        p_value = 'PbcInFaultRecoveryRequest_0' + str(number) + ' '
        patterns.update({re.compile(p_key): p_value})

    else:
        p_key = f'( MEASUREMENT| CHARACTERISTIC)\\s+(_?PbcIn\\.?_?FaultRecoveryRequest.?_?\\[?{number}\\]?[^\\s/]*)'
        p_value = 'PbcInFaultRecoveryRequest_' + str(number)
        patterns.update({re.compile(p_key) : p_value})

# MOTOR CURRENT LEFT/RIGHT
for number in range(0, 10):
    p_key = f'( MEASUREMENT| CHARACTERISTIC)\\s+(_?PbcIn\\.?_?MotorCurrentLeft.?[_\\[]?0{number}\\]?[^\\s/]*)'
    p_value = 'PbcInMotorCurrentLeft_0' + str(number)
    patterns.update({re.compile(p_key): p_value})

    p_key = f'( MEASUREMENT| CHARACTERISTIC)\\s+(_?PbcIn\\.?_?MotorCurrentLeft.?[_\\[]?{number}\\]?\\D[^\\s/^"]*)'
    p_value = 'PbcInMotorCurrentLeft_0' + str(number) + ' '
    patterns.update({re.compile(p_key): p_value})

    p_key = f'( MEASUREMENT| CHARACTERISTIC)\\s+(_?PbcIn\\.?_?MotorCurrentRight.?[_\\[]?0{number}\\]?[^\\s/]*)'
    p_value = 'PbcInMotorCurrentRight_0' + str(number)
    patterns.update({re.compile(p_key): p_value})

    p_key = f'( MEASUREMENT| CHARACTERISTIC)\\s+(_?PbcIn\\.?_?MotorCurrentRight.?[_\\[]?{number}\\]?\\D[^\\s/^"]*)'
    p_value = 'PbcInMotorCurrentRight_0' + str(number) + ' '
    patterns.update({re.compile(p_key): p_value})

# MOTOR VOLTAGE LEFT/RIGHT
for number in range(0, 10):
    p_key = f'( MEASUREMENT| CHARACTERISTIC)\\s+(_?PbcIn\\.?_?MotorVoltageLeft.?[_\\[]?0{number}\\]?[^\\s/]*)'
    p_value = 'PbcInMotorVoltageLeft_0' + str(number)
    patterns.update({re.compile(p_key): p_value})

    p_key = f'( MEASUREMENT| CHARACTERISTIC)\\s+(_?PbcIn\\.?_?MotorVoltageLeft.?[_\\[]?{number}\\]?\\D[^\\s/^"]*)'
    p_value = 'PbcInMotorVoltageLeft_0' + str(number) + ' '
    patterns.update({re.compile(p_key): p_value})

    p_key = f'( MEASUREMENT| CHARACTERISTIC)\\s+(_?PbcIn\\.?_?MotorVoltageRight.?[_\\[]?0{number}\\]?[^\\s/]*)'
    p_value = 'PbcInMotorVoltageRight_0' + str(number)
    patterns.update({re.compile(p_key): p_value})

    p_key = f'( MEASUREMENT| CHARACTERISTIC)\\s+(_?PbcIn\\.?_?MotorVoltageRight.?[_\\[]?{number}\\]?\\D[^\\s/^"]*)'
    p_value = 'PbcInMotorVoltageRight_0' + str(number) + ' '
    patterns.update({re.compile(p_key): p_value})


# # FAULT RECOVERY
# for number in range(0, 99):
#     if number < 10:
#         p_key = f'( MEASUREMENT| CHARACTERISTIC)\\s+(_?PbcIn[\\._]?DataStorageRead.?[_\\[]?0{number}\\]?[^\\s/]*)'
#         p_value = 'PbcInDataStorageRead_0' + str(number)
#         patterns.update({re.compile(p_key): p_value})

#         p_key = f'( MEASUREMENT| CHARACTERISTIC)\\s+(_?PbcIn[\\._]?DataStorageRead.?[_\\[]?{number}\\]?\\D[^\\s/^"]*)'
#         p_value = 'PbcInDataStorageRead_0' + str(number) + ' '
#         patterns.update({re.compile(p_key): p_value})

#     else:
#         p_key = f'( MEASUREMENT| CHARACTERISTIC)\\s+(_?PbcIn[._]?DataStorageRead.?_?\\[?{number}\\]?[^\\s/]*)'
#         p_value = 'PbcInDataStorageRead_' + str(number)
#         patterns.update({re.compile(p_key) : p_value})


#######################################################################################
#######################################  PBC OUT  ####################################
#######################################################################################

# SW VERSION SIGNALS
for number in range(0, 6):
    p_key = f'( MEASUREMENT| CHARACTERISTIC)\\s+(_?PbcOut\\.?_?PbcSoftwareVersion.?[_\\[]?0{number}\\]?[^\\s/]*)'
    p_value = 'PbcOutPbcSoftwareVersion_0' + str(number)
    patterns.update({re.compile(p_key): p_value})

    p_key = f'( MEASUREMENT| CHARACTERISTIC)\\s+(_?PbcOut\\.?_?PbcSoftwareVersion.?[_\\[]?{number}\\]?\\D[^\\s/^"]*)'
    p_value = 'PbcOutPbcSoftwareVersion_0' + str(number) + ' '
    patterns.update({re.compile(p_key): p_value})

# STANDARD SIGNALS
pbc_out_signals = {
    'ActuatorStateLeft' : 'PbcOutActuatorStateLeft',
    'ActuatorStateRight' : 'PbcOutActuatorStateRight',
    'MotorCommandLeft' : 'PbcOutMotorCommandLeft',
    'MotorCommandRight' : 'PbcOutMotorCommandRight',
    'OutOfSpecMsg' : 'PbcOutOutOfSpecMsg',
    'DiagRequestStatus' : 'PbcOutDiagRequestStatus',
    r'DiagBrake(?:Tmpr|Temperature)Left' : 'PbcOutDiagBrakeTemperatureLeft',
    r'DiagBrake(?:Tmpr|Temperature)Right' : 'PbcOutDiagBrakeTemperatureRight',
    r'Diag(?:Achieved)?ClampForceLeft' : 'PbcOutDiagAchievedClampForceLeft',
    r'Diag(?:Achieved)?ClampForceRight' : 'PbcOutDiagAchievedClampForceRight',
    r'DiagAct(?:uation)?CounterLeft' : 'PbcOutDiagActuationCounterLeft',
    r'DiagAct(?:uation)?CounterRight' : 'PbcOutDiagActuationCounterRight',
    'HpsPressure' : 'PbcOutHpsPressure',
    'HpsRequest' : 'PbcOutHpsRequest',
    'DiagRequestAcknowledge' : 'PbcOutDiagRequestAcknowledge',
    'DataStorageRequest' : 'PbcOutDataStorageRequest',
    'EcuPowerLatchRequest' : 'PbcOutEcuPowerLatchRequest',
    'PadAdjustmentRequest' : 'PbcOutPadAdjustmentRequest',
    'ParkSupportRequest' : 'PbcOutParkSupportRequest',
}

for signal_key, signal_value in pbc_out_signals.items():
    key = re.compile(r'( MEASUREMENT| CHARACTERISTIC)\s+(_?PbcOut(Debug)?.?_?' + signal_key + r'[^\s/]*)')
    value = signal_value
    patterns.update({key : value})




#FAULT SIGNALS
for number in range(0, 20):
    if number < 10:
        p_key = f'( MEASUREMENT| CHARACTERISTIC)\\s+(_?PbcOut(Debug)?\\.?_?FaultStatus.?[_\\[]?0{number}\\]?[^\\s/]*)'
        p_value = 'PbcOutFaultStatus_0' + str(number)
        patterns.update({re.compile(p_key): p_value})

        p_key = f'( MEASUREMENT| CHARACTERISTIC)\\s+(_?PbcOut(Debug)?\\.?_?FaultStatus.?[_\\[]?{number}\\]?\\D[^\\s/^"]*)'
        p_value = 'PbcOutFaultStatus_0' + str(number) + ' '
        patterns.update({re.compile(p_key): p_value})

    else:
        p_key = f'( MEASUREMENT| CHARACTERISTIC)\\s+(_?PbcOut(Debug)?\\.?_?FaultStatus.?_?\\[?{number}\\]?[^\\s/]*)'
        p_value = 'PbcOutFaultStatus_' + str(number)
        patterns.update({re.compile(p_key) : p_value})


#DATA STORAGE SIGNALS
for number in range(0, 99):
    if number < 10:
        p_key = f'( MEASUREMENT| CHARACTERISTIC)\\s+(_?PbcOut(Debug)?\\.?_?DataStorageWrite.?[_\\[]?0{number}\\]?[^\\s/]*)'
        p_value = 'PbcOutDataStorageWrite_0' + str(number)
        patterns.update({re.compile(p_key): p_value})

        p_key = f'( MEASUREMENT| CHARACTERISTIC)\\s+(_?PbcOut(Debug)?\\.?_?DataStorageWrite.?[_\\[]?{number}\\]?\\D[^\\s/^"]*)'
        p_value = 'PbcOutDataStorageWrite_0' + str(number) + ' '
        patterns.update({re.compile(p_key): p_value})

    else:
        p_key = f'( MEASUREMENT| CHARACTERISTIC)\\s+(_?PbcOut(Debug)?.?_?DataStorageWrite.?_?\\[?{number}\\]?[^\\s/]*)'
        p_value = 'PbcOutDataStorageWrite_' + str(number)
        patterns.update({re.compile(p_key) : p_value})


signals_to_check = []
for pattern_value in patterns.values():
    signals_to_check.append(pattern_value)
signals_to_check = list(dict.fromkeys(signals_to_check))

# print(signals_to_check)

# PRINT PATTERNS DICTIONARY
# for key, value in patterns.items():
#     print(key, ' : ', value)




