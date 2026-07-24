from abc import ABC, abstractmethod


class Specification(ABC):
    @abstractmethod
    def is_satisfied(self, node):
        pass

    def __and__(self, other):
        return AndSpecification(self, other)

    def __or__(self, other):
        return OrSpecification(self, other)


class AndSpecification(Specification):
    def __init__(self, *specifications):
        self.specifications = specifications

    def is_satisfied(self, node):
        return all(
            specification.is_satisfied(node)
            for specification in self.specifications
        )


class OrSpecification(Specification):
    def __init__(self, *specifications):
        self.specifications = specifications

    def is_satisfied(self, node):
        return any(
            specification.is_satisfied(node)
            for specification in self.specifications
        )


class NotCoveredSpecification(Specification):
    def is_satisfied(self, node):
        return node.node_icon == "red"


class CoveredSpecification(Specification):
    def is_satisfied(self, node):
        return node.node_icon == "green"


class IgnoredSpecification(Specification):
    def is_satisfied(self, node):
        return node.reference.lower() in node.MODULE.ignore_list


class AllSpecification(Specification):
    def is_satisfied(self, node):
        return node is not None


class FullTextSpecification(Specification):
    def __init__(self, filtered_text):
        self.filtered_text = filtered_text

    def is_satisfied(self, node):
        return self.filtered_text.lower() in node.text().lower()


class FullTextRequirementSpecification(Specification):
    def __init__(self, filtered_text):
        self.filtered_text = filtered_text

    def is_satisfied(self, node):
        data = " ".join(node.columns_data) + " " + str(node.reference)
        return self.filtered_text.lower() in data.lower()
