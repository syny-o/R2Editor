import enum

class ViewCoverageFilter(enum.Enum):
    ALL = "All"
    COVERED_AND_NOT_COVERED = "Coverage"
    COVERED = "Covered"
    NOT_COVERED = "Not Covered"
