import re

# CREATE PATTERNS DICTIONARY
patterns = {}

#######################################################################################
########################################  PBC IN  #####################################
#######################################################################################

# DRIVEAWAY
key = re.compile(r'_?PbcIn\.?_?DriveAway[A-Za-z]*Ind[a-z]*')
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
    key = re.compile(r'_?PbcIn\.?_?' + signal)
    value = 'PbcIn' + signal
    patterns.update({key : value})


# SIGNALS WITH NUMBERS
for signal in ("FaultRecoveryRequest", "DataStorageRead", "PbcSoftwareVersion", "MotorVoltageLeft", "MotorVoltageRight", "MotorCurrentLeft", "MotorCurrentRight", "HostSoftwareVersion", "VariantItem"):
    for number in range(0, 20):
        if number < 10:
            p_key = f'_?PbcIn\\.?_?{signal}\\.?[_\\[]?0{number}\\]?_?'
            p_value = f'PbcIn{signal}_0' + str(number)
            patterns.update({re.compile(p_key): p_value})

            p_key = f'_?PbcIn\\.?_?{signal}\\.?[_\\[]?{number}(?!\\d)[_\\]]*'
            p_value = f'PbcIn{signal}_0' + str(number)
            patterns.update({re.compile(p_key): p_value})

        else:
            p_key = f'_?PbcIn\\.?_?{signal}\\.?_?\\[?{number}\\]?_?'
            p_value = f'PbcIn{signal}_' + str(number)
            patterns.update({re.compile(p_key) : p_value})


#######################################################################################
#######################################  PBC OUT  ####################################
#######################################################################################


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
    key = re.compile(r'_?PbcOut(Debug)?\.?_?' + signal_key)
    value = signal_value
    patterns.update({key : value})


# SIGNALS WITH NUMBERS
for signal in ("FaultStatus", "DataStorageWrite", "PbcSoftwareVersion", "DevelopmentMessages"):
    for number in range(0, 20):
        if number < 10:
            p_key = f'_?PbcOut(Debug)?\\.?_?{signal}\\.?[_\\[]?0{number}\\]?_?'
            p_value = f'PbcOut{signal}_0' + str(number)
            patterns.update({re.compile(p_key): p_value})

            p_key = f'_?PbcOut(Debug)?\\.?_?{signal}\\.?[_\\[]?{number}(?!\\d)[_\\]]*'
            p_value = f'PbcOut{signal}_0' + str(number)
            patterns.update({re.compile(p_key): p_value})

        else:
            p_key = f'_?PbcOut(Debug)?\\.?_?{signal}\\.?_?\\[?{number}\\]?_?'
            p_value = f'PbcOut{signal}_' + str(number)
            patterns.update({re.compile(p_key) : p_value})







