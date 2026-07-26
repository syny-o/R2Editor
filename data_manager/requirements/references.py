import re


REFERENCE_PATTERN = re.compile(
    r'(?:REFERENCE|\$REF:)\s*"(?P<references>.+)"'
    r'\s*(?:\$|EXPECTEDRESULT)',
    re.IGNORECASE,
)


def extract_requirement_references(text):
    references = set()
    for reference_list in REFERENCE_PATTERN.findall(text):
        references.update(
            reference.strip().lower()
            for reference in reference_list.split(',')
            if reference.strip()
        )
    return references


def changed_requirement_references(original_text, updated_text):
    original_references = extract_requirement_references(original_text)
    updated_references = extract_requirement_references(updated_text)
    return original_references.symmetric_difference(updated_references)
