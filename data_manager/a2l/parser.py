import re


MEASUREMENT_PATTERN = re.compile(
    r"(/begin MEASUREMENT|/begin CHARACTERISTIC)"
    r"(.*?)"
    r"(/end MEASUREMENT|end CHARACTERISTIC)",
    flags=re.DOTALL,
)
SIGNAL_NAME_PATTERN = re.compile(
    r"(/begin MEASUREMENT|/begin CHARACTERISTIC)\s+([^/\s]+)",
    flags=re.DOTALL,
)
SIGNAL_ADDRESS_PATTERN = re.compile(r"(ECU_ADDRESS|VALUE)\s+(\w+)")
SUPPORTED_SIGNAL_PARTS = ("pbcin", "pbcout", "ssmpbin", "ssmpbout")


def extract_measurement_blocks(text):
    return [
        match.group()
        for match in MEASUREMENT_PATTERN.finditer(text)
    ]


def parse_supported_signals(text):
    signals = []
    for measurement in extract_measurement_blocks(text):
        name_match = SIGNAL_NAME_PATTERN.search(measurement)
        if not name_match:
            continue

        name = name_match.group(2)
        if not any(part in name.lower() for part in SUPPORTED_SIGNAL_PARTS):
            continue

        address_match = SIGNAL_ADDRESS_PATTERN.search(measurement)
        address = address_match.group(2) if address_match else "Unknown"
        signals.append((name, address))
    return signals


def parse_supported_signals_from_file(file_path):
    with open(file_path, encoding="utf-8", errors="ignore") as file:
        return parse_supported_signals(file.read())
