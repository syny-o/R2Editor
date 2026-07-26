import re
from dataclasses import dataclass
from functools import cache
from math import prod


SECTION_PATTERN = re.compile(
    r'^[ \t]*(?P<command>END\s+CHAPTER|CHAPTER|TESTCASE)\b(?P<rest>.*)$',
    re.IGNORECASE | re.MULTILINE,
)
EXPECTED_RESULT_PATTERN = re.compile(r'\bEXPECTEDRESULT\b', re.IGNORECASE)
TITLE_METADATA_PATTERN = re.compile(r'\s+(?:ID|REFERENCE)\s+')
FOR_PATTERN = re.compile(
    r'^[ \t]*FOR\s+(?P<variable>[A-Za-z_]\w*)\s*='
    r'\s*(?P<values>.*?)\s+DO\s*$',
    re.IGNORECASE,
)
NEXT_PATTERN = re.compile(r'^[ \t]*NEXT\b', re.IGNORECASE)


@dataclass(frozen=True)
class OutlineSection:
    kind: str
    title: str
    position: int
    for_variables: tuple = ()
    iteration_count: int = 1


def _for_context_by_line(text):
    contexts = {}
    active_loops = []
    position = 0

    for line in text.splitlines(keepends=True):
        contexts[position] = tuple(active_loops)
        line_without_newline = line.rstrip('\r\n')

        for_match = FOR_PATTERN.match(line_without_newline)
        if for_match is not None:
            values = tuple(for_match.group('values').split())
            active_loops.append((for_match.group('variable'), values))
        elif NEXT_PATTERN.match(line_without_newline) and active_loops:
            active_loops.pop()

        position += len(line)

    return contexts


def _extract_title(rest, command):
    if command == 'TESTCASE':
        expected_result = EXPECTED_RESULT_PATTERN.search(rest)
        if expected_result is None:
            return None
        title_expression = rest[:expected_result.start()]
    else:
        title_expression = rest

    metadata = TITLE_METADATA_PATTERN.search(title_expression)
    if metadata is not None:
        title_expression = title_expression[:metadata.start()]

    title = title_expression.strip()
    if not title.startswith('"'):
        return None

    title = title[1:]
    if title.endswith('"'):
        title = title[:-1]

    return title.strip()


@cache
def parse_outline_sections(text):
    sections = []
    for_contexts = _for_context_by_line(text)
    for match in SECTION_PATTERN.finditer(text):
        command = match.group('command').upper()
        rest = match.group('rest')

        if command == 'END CHAPTER':
            sections.append(OutlineSection('end_chapter', '', match.start()))
            continue

        if command == 'TESTCASE':
            kind = 'testcase'
        else:
            kind = 'chapter'

        title = _extract_title(rest, command)
        if title is None:
            continue

        active_loops = (
            for_contexts.get(match.start(), ())
            if kind == 'testcase'
            else ()
        )
        iteration_count = (
            prod(len(values) for _, values in active_loops)
            if active_loops
            else 1
        )
        sections.append(
            OutlineSection(
                kind,
                title,
                match.start(),
                tuple(variable for variable, _ in active_loops),
                iteration_count,
            )
        )

    return tuple(sections)


def line_number_from_position(text, position):
    return text[:position].count('\n') + 1
