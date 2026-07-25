import re
from dataclasses import dataclass
from functools import cache


SECTION_PATTERN = re.compile(
    r'^[ \t]*(?P<command>END\s+CHAPTER|CHAPTER|TESTCASE)\b(?P<rest>.*)$',
    re.IGNORECASE | re.MULTILINE,
)
TITLE_PATTERN = re.compile(r'"([^"]*)"')


@dataclass(frozen=True)
class OutlineSection:
    kind: str
    title: str
    position: int


@cache
def parse_outline_sections(text):
    sections = []
    for match in SECTION_PATTERN.finditer(text):
        command = match.group('command').upper()
        rest = match.group('rest')

        if command == 'END CHAPTER':
            sections.append(OutlineSection('end_chapter', '', match.start()))
            continue

        title_match = TITLE_PATTERN.search(rest)
        if title_match is None:
            continue

        if command == 'TESTCASE':
            if not re.search(r'\bEXPECTEDRESULT\b', rest, re.IGNORECASE):
                continue
            kind = 'testcase'
        else:
            kind = 'chapter'

        sections.append(
            OutlineSection(kind, title_match.group(1), match.start())
        )

    return tuple(sections)


def line_number_from_position(text, position):
    return text[:position].count('\n') + 1
