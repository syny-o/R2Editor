from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QStandardItem



class ConditionNode(QStandardItem):
    def __init__(self, name, category):
        super().__init__()
        self.setEditable(False)
        self.setIcon(QIcon(u"ui/icons/condition.png"))

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
        return self.parent()

    def get_node_copy(self):
        # create list of children --> ValueNode objects
        my_val_nodes = [self.child(row) for row in range(self.rowCount())]
        # create copies of all children
        new_val_nodes = [val_node.get_node_copy() for val_node in my_val_nodes]
        new_cond_node = ConditionNode(self.name, self.category)
        new_cond_node.appendRows(new_val_nodes)
        return new_cond_node        