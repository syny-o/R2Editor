from abc import ABC, abstractmethod

class ISyntaxHighlighter(ABC):
    
    @abstractmethod
    def highlightBlock(self, text: str) -> str:
        pass

    @abstractmethod
    def __init__(self, document, dark_mode):
        pass