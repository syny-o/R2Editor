import enum
import re


PATTERN_REQ_REFERENCE = re.compile(r'(?:REFERENCE|\$REF:)\s*"(?P<req_reference>.+)"\s*(?:\$|EXPECTEDRESULT)', re.IGNORECASE)


class ViewCoverageFilter(enum.Enum):
    ALL = "All"
    COVERED_AND_NOT_COVERED = "Coverage"
    COVERED = "Covered"
    NOT_COVERED = "Not Covered"
