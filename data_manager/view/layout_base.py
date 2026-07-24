from abc import ABC, abstractmethod


class LayoutGenerator(ABC):
    @abstractmethod
    def fill_with_data(self, node):
        """Display data from a node in the generator widgets."""

    @abstractmethod
    def provide_layout(self):
        """Return the frame owned by the generator."""
