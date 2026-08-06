from PyQt5.QtWidgets import QPlainTextEdit, QWidget
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(event.rect(), QColor(10, 10, 10))

        block = self.editor.firstVisibleBlock()
        blockNumber = block.blockNumber()

        top = self.editor.blockBoundingGeometry(block)\
            .translated(self.editor.contentOffset()).top()
        height = self.editor.fontMetrics().height()

        painter.setPen(Qt.lightGray)

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible():
                painter.drawText(
                    0,
                    int(top),
                    self.width() - 5,
                    height,
                    Qt.AlignRight,
                    str(blockNumber + 1)
                )

            block = block.next()
            top += self.editor.blockBoundingRect(block).height()
            blockNumber += 1


class FastCodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()

        self.lineNumberArea = LineNumberArea(self)

        # ✅ super důležité pro výkon
        self.setViewportUpdateMode(QPlainTextEdit.MinimalViewportUpdate)

        self.blockCountChanged.connect(self.updateMargin)
        self.updateRequest.connect(self.updateLineNumbers)

        self.updateMargin()

    def updateMargin(self):
        width = self.fontMetrics().horizontalAdvance("9") * len(str(self.blockCount())) + 10
        self.setViewportMargins(width, 0, 0, 0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(0, 0, self.viewportMargins().left(), cr.height())

    def updateLineNumbers(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())