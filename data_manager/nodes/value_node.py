from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QStandardItem


class ValueNode(QStandardItem):
    def __init__(self, name, category):
        super().__init__()
        self.setEditable(False)
        self.setIcon(QIcon(u"ui/icons/value.png"))

        self.name = name
        self.category = category



    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self.setText(name)
        self._name = name


    def get_file_node(self):
        return self.parent().parent()

    @property
    def my_test_step_nodes(self):
        return [self.child(row) for row in range(self.rowCount())]

    def get_node_copy(self):
        new_ts_nodes = [ts_node.get_node_copy() for ts_node in self.my_test_step_nodes]
        new_value_node = ValueNode(self.name, self.category)
        new_value_node.appendRows(new_ts_nodes)
        return new_value_node