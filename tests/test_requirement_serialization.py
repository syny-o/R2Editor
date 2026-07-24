import unittest

from data_manager.requirement_serialization import (
    requirement_tree_to_list,
    requirements_to_dict,
)


class FakeNode:
    def __init__(self, reference, children=None):
        self.reference = reference
        self.heading = False
        self.level = 1
        self.outlinks = []
        self.inlinks = []
        self.file_references = {'script.par'}
        self.is_covered = True
        self.columns_data = [f'text for {reference}']
        self.children = children or []

    def rowCount(self):
        return len(self.children)

    def child(self, row):
        return self.children[row]


class RequirementSerializationTests(unittest.TestCase):
    def test_serializes_tree_in_depth_first_order(self):
        root = FakeNode(
            'root',
            [
                FakeNode('REQ-1', [FakeNode('REQ-1-1')]),
                FakeNode('REQ-2'),
            ],
        )

        serialized = requirement_tree_to_list(root)

        self.assertEqual(
            [item['reference'] for item in serialized],
            ['REQ-1', 'REQ-1-1', 'REQ-2'],
        )
        self.assertEqual(serialized[0]['file_references'], ['script.par'])

    def test_converts_requirements_to_comparison_dictionary(self):
        requirements = [
            {'reference': 'REQ-1', 'columns_data': ['first']},
            {'reference': 'REQ-2', 'columns_data': ['second']},
        ]

        self.assertEqual(
            requirements_to_dict(requirements),
            {'REQ-1': ['first'], 'REQ-2': ['second']},
        )


if __name__ == '__main__':
    unittest.main()
