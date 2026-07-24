import unittest

from data_manager.view.filter_specifications import (
    AllSpecification,
    CoveredSpecification,
    FullTextRequirementSpecification,
    FullTextSpecification,
    IgnoredSpecification,
    NotCoveredSpecification,
)


class FakeModule:
    def __init__(self, ignored=None):
        self.ignore_list = ignored or []


class FakeNode:
    def __init__(
        self,
        text='',
        reference='REQ-1',
        columns=None,
        icon=None,
        ignored=None,
    ):
        self._text = text
        self.reference = reference
        self.columns_data = columns or []
        self.node_icon = icon
        self.MODULE = FakeModule(ignored)

    def text(self):
        return self._text


class FilterSpecificationsTests(unittest.TestCase):
    def test_combines_coverage_specifications(self):
        covered = FakeNode(icon='green')
        uncovered = FakeNode(icon='red')

        specification = (
            CoveredSpecification() | NotCoveredSpecification()
        )

        self.assertTrue(specification.is_satisfied(covered))
        self.assertTrue(specification.is_satisfied(uncovered))

    def test_combines_coverage_and_fulltext(self):
        specification = (
            CoveredSpecification()
            & FullTextRequirementSpecification('approved')
        )

        self.assertTrue(
            specification.is_satisfied(
                FakeNode(
                    reference='REQ-1',
                    columns=['Approved requirement'],
                    icon='green',
                )
            )
        )
        self.assertFalse(
            specification.is_satisfied(
                FakeNode(
                    columns=['Draft requirement'],
                    icon='green',
                )
            )
        )

    def test_matches_ignored_reference_case_insensitively(self):
        node = FakeNode(reference='REQ-1', ignored=['req-1'])

        self.assertTrue(IgnoredSpecification().is_satisfied(node))

    def test_matches_standard_node_text_case_insensitively(self):
        node = FakeNode(text='Engine Speed')

        self.assertTrue(
            FullTextSpecification('speed').is_satisfied(node)
        )

    def test_all_specification_accepts_any_node(self):
        self.assertTrue(AllSpecification().is_satisfied(FakeNode()))
        self.assertFalse(AllSpecification().is_satisfied(None))


if __name__ == '__main__':
    unittest.main()
