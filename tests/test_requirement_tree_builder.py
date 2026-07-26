import unittest

from data_manager.requirements.tree_builder import (
    append_nodes_by_level,
    iter_descendants,
)


class FakeNode:
    def __init__(self, name, level=0):
        self.name = name
        self.level = level
        self.children = []

    def appendRow(self, node):
        self.children.append(node)

    def rowCount(self):
        return len(self.children)

    def child(self, row):
        return self.children[row]


class RequirementTreeBuilderTests(unittest.TestCase):
    def test_builds_hierarchy_from_requirement_levels(self):
        root = FakeNode('root')
        nodes = [
            FakeNode('chapter', 1),
            FakeNode('requirement-1', 2),
            FakeNode('requirement-2', 2),
            FakeNode('subchapter', 2),
            FakeNode('requirement-3', 3),
            FakeNode('chapter-2', 1),
        ]

        append_nodes_by_level(root, nodes)

        self.assertEqual(
            [node.name for node in root.children],
            ['chapter', 'chapter-2'],
        )
        self.assertEqual(
            [node.name for node in root.children[0].children],
            ['requirement-1', 'requirement-2', 'subchapter'],
        )
        self.assertEqual(
            root.children[0].children[2].children[0].name,
            'requirement-3',
        )

    def test_accepts_empty_node_list(self):
        root = FakeNode('root')

        append_nodes_by_level(root, [])

        self.assertEqual(root.children, [])

    def test_iterates_descendants_in_depth_first_order(self):
        root = FakeNode('root')
        first = FakeNode('first', 1)
        first_child = FakeNode('first-child', 2)
        second = FakeNode('second', 1)
        first.appendRow(first_child)
        root.appendRow(first)
        root.appendRow(second)

        result = [node.name for node in iter_descendants(root)]

        self.assertEqual(result, ['first', 'first-child', 'second'])


if __name__ == '__main__':
    unittest.main()
