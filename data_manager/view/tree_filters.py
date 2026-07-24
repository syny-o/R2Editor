from abc import ABC, abstractmethod

from PyQt5.QtGui import QColor

from data_manager.view.filter_specifications import Specification


class TreeFilter(ABC):
    @abstractmethod
    def filter(self, tree, node, specification: Specification):
        pass


class FirstLevelFilter(TreeFilter):
    def filter(self, tree, node, specification: Specification):
        for row in range(node.rowCount()):
            child = node.child(row)
            tree.setRowHidden(
                row,
                node.index(),
                not specification.is_satisfied(child),
            )


class LastLevelFilter(TreeFilter):
    def filter(self, tree, node, specification: Specification):
        for row in range(node.rowCount()):
            child = node.child(row)
            is_satisfied = specification.is_satisfied(child)
            tree.setRowHidden(row, node.index(), not is_satisfied)

            if is_satisfied:
                parent = child.parent()
                while parent and parent.parent():
                    tree.setRowHidden(
                        parent.row(),
                        parent.parent().index(),
                        False,
                    )
                    parent = parent.parent()

            self.filter(tree, child, specification)


class DecoratedAutoExpandingLastLevelFilter(TreeFilter):
    def filter(self, tree, node, specification: Specification):
        for row in range(node.rowCount()):
            child = node.child(row)
            is_satisfied = specification.is_satisfied(child)
            tree.setRowHidden(row, node.index(), not is_satisfied)

            if is_satisfied:
                child.setForeground(QColor(0, 150, 0))
                parent = child.parent()
                while parent and parent.parent():
                    tree.setRowHidden(
                        parent.row(),
                        parent.parent().index(),
                        False,
                    )
                    tree.expand(parent.index())
                    parent = parent.parent()
            else:
                child.setForeground(QColor(90, 90, 90))
                tree.collapse(child.index())

            self.filter(tree, child, specification)
