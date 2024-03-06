from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QStandardItem



class TestStepNode(QStandardItem):
    def __init__(self, name, action, comment, nominal):
        super().__init__()

        self.setEditable(False)
        self.setIcon(QIcon(u"ui/icons/ts.png"))

        self.name = name
        self.action = action
        self.comment = comment
        self.nominal = nominal
        


    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, action):
        self.setText(action)
        self._action = action



    def get_file_node(self):
        return self.parent().parent().parent()

    def get_node_copy(self):
        return TestStepNode(self.name, self.action, self.comment, self.nominal)