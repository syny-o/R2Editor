from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem

from data_manager.nodes.requirement_module import RequirementModule




class ModuleLocker:
    def __init__(self) -> None:
        self._locked_modules: List[RequirementModule|QStandardItem] = []
        self._locked_modules_properties: List[str] = []

    def lock_module(self, module: RequirementModule|QStandardItem) -> None:
        self._locked_modules.append(module)
        self._locked_modules_properties.append((module.foreground(), module.text()))
        self._decorate(module)
        # module.setEnabled(False)

    def unlock_module(self, module: RequirementModule|QStandardItem) -> None:
        self._undecorate(module)
        index = self._locked_modules.index(module)
        self._locked_modules.pop(index)
        self._locked_modules_properties.pop(index)
        
        # module.setEnabled(True)

    def unlock_all_modules(self) -> None:
        self._undecorate_all()
        self._locked_modules.clear()
        self._locked_modules_properties.clear()
        

    @property
    def locked_modules(self) -> List[RequirementModule|QStandardItem]:
        return self._locked_modules

    def _decorate(self, module: RequirementModule|QStandardItem):
        module.setForeground(Qt.green)
        module.setText(f"[ downloading ]  {module.text()}")

    def _undecorate(self, module: RequirementModule|QStandardItem):
        index = self._locked_modules.index(module)
        foreground, text = self._locked_modules_properties[index]
        module.setForeground(foreground)
        module.setText(text)

    def _undecorate_all(self):
        for module, (foreground, text) in zip(self._locked_modules, self._locked_modules_properties):
            module.setForeground(foreground)
            module.setText(text)

            # module.setEnabled(True)