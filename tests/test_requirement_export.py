import unittest

from data_manager.requirement_export import (
    build_export_header,
    build_export_rows,
)


class FakeRequirement:
    def __init__(
        self,
        reference,
        columns=None,
        note='',
        children=None,
        hidden=False,
    ):
        self.reference = reference
        self.columns_data = columns or []
        self.note = note
        self.children = children or []
        self.hidden = hidden

    def rowCount(self):
        return len(self.children)

    def child(self, row):
        return self.children[row]

    def hasChildren(self):
        return bool(self.children)


class RequirementExportTests(unittest.TestCase):
    def test_builds_selected_header_with_note(self):
        self.assertEqual(
            build_export_header(
                ['Status', 'Text', 'Owner'],
                [0, 2],
                include_note=True,
            ),
            ['Identifier', 'Status', 'Owner', 'User note'],
        )

    def test_exports_only_visible_leaf_requirements(self):
        module = FakeRequirement(
            'module',
            children=[
                FakeRequirement(
                    'chapter',
                    children=[
                        FakeRequirement(
                            'REQ-1',
                            ['Approved', 'First'],
                            note='reviewed',
                        ),
                        FakeRequirement(
                            'REQ-2',
                            ['Draft', 'Second'],
                            hidden=True,
                        ),
                    ],
                ),
                FakeRequirement(
                    'REQ-3',
                    ['Approved', 'Third'],
                ),
            ],
        )

        rows = build_export_rows(
            module,
            [0],
            include_note=True,
            is_hidden=lambda item: item.hidden,
        )

        self.assertEqual(
            rows,
            [
                ['REQ-1', 'Approved', 'reviewed'],
                ['REQ-3', 'Approved', ''],
            ],
        )


if __name__ == '__main__':
    unittest.main()
