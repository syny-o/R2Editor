from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QTextEdit, QApplication
from PyQt5.QtGui import QColor, QPainter, QTextFormat, QTextCursor, QTextCharFormat, QPalette
import sys

class QLineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.codeEditor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)

class QCodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = QLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlight_keywords)
        self.updateLineNumberAreaWidth(0)
        self.original_background_color = QColor(33, 35, 35)

    def paintEvent(self, event):
        super().paintEvent(event)

        # Draw outline around the current line
        if not self.isReadOnly():
            cursor = self.textCursor()
            block = cursor.block()
            top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
            bottom = top + self.blockBoundingRect(block).height()

            # Define the outline color and thickness
            outline_color = QColor(100, 100, 100)  # Light gray
            outline_thickness = 1

            painter = QPainter(self.viewport())
            painter.setPen(QColor(outline_color))
            rect = QRect(0, int(top), self.viewport().width(), int(bottom - top))
            painter.drawRect(rect.adjusted(0, 0, -outline_thickness, -outline_thickness))        

    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 18 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))


    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor(10, 10, 10))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                painter.setPen(Qt.lightGray)
                painter.drawText(10, int(top), self.lineNumberArea.width(), height, Qt.AlignLeft, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def highlight_keywords(self):
        self.clear_highlight()
        
        cursor = self.textCursor()
        text = self.toPlainText()
        cursor_pos = cursor.position()


        keywords = [('IF', 'ENDIF'), ('FOR', 'NEXT')]
        for keyword_pair in keywords:
            self.highlight_pair(text, cursor_pos, keyword_pair[0], keyword_pair[1])

 

    def highlight_pair(self, text, cursor_pos, start_keyword, end_keyword):
        TEXT_RADIUS = 500  # Define the search radius
        start_len = len(start_keyword)
        end_len = len(end_keyword)
        
        # Calculate the bounds for the search area around the cursor position
        start_pos = max(0, cursor_pos - TEXT_RADIUS)
        end_pos = min(len(text), cursor_pos + TEXT_RADIUS)
        
        # Only work within the limited text slice
        limited_text = text[start_pos:end_pos]
        pos = 0
        stack = []

        # Adjusted cursor position within the limited text slice
        adjusted_cursor_pos = cursor_pos - start_pos

        while pos < len(limited_text):
            if limited_text[pos:pos + start_len] == start_keyword and \
            (pos == 0 or limited_text[pos - 1].isspace()) and \
            (pos + start_len == len(limited_text) or limited_text[pos + start_len].isspace()):
                stack.append(pos)
                pos += start_len
            elif limited_text[pos:pos + end_len] == end_keyword and \
                (pos == 0 or limited_text[pos - 1].isspace()) and \
                (pos + end_len == len(limited_text) or limited_text[pos + end_len].isspace()):
                if stack:
                    start_match_pos = stack.pop()
                    if start_match_pos <= adjusted_cursor_pos <= start_match_pos + start_len:
                        # Convert positions back to the original text positions
                        self.highlight_text(start_pos + start_match_pos, start_pos + start_match_pos + start_len)
                        self.highlight_text(start_pos + pos, start_pos + pos + end_len)
                    elif pos <= adjusted_cursor_pos <= pos + end_len:
                        self.highlight_text(start_pos + start_match_pos, start_pos + start_match_pos + start_len)
                        self.highlight_text(start_pos + pos, start_pos + pos + end_len)
                pos += end_len
            else:
                pos += 1


    def highlight_text(self, start, end):
        cursor = self.textCursor()
        cursor.setPosition(start)
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, end - start)
        
        # Set a solid yellow background for keywords
        fmt = QTextCharFormat()
        fmt.setBackground(QColor(255, 255, 0))  # Yellow
        cursor.setCharFormat(fmt)

    def clear_highlight(self):
        cursor = self.textCursor()
        cursor.select(QTextCursor.Document)
        fmt = QTextCharFormat()
        fmt.setBackground(self.original_background_color)  # Use stored color
        cursor.setCharFormat(fmt)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = QCodeEditor()
    editor.show()
    sys.exit(app.exec_())
