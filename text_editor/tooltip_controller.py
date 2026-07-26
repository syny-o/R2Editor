from PyQt5.QtCore import QEvent, QObject, QPoint, QTimer
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QToolTip
from PyQt5 import sip

from text_editor.tooltip_content import render_tooltip


HOVER_DELAY_MS = 350
TOOLTIP_OFFSET = QPoint(12, 20)


class TooltipController(QObject):
    def __init__(self, editor, registry, delay=HOVER_DELAY_MS):
        super().__init__(editor)
        self.editor = editor
        self.viewport = editor.viewport()
        self.registry = registry
        self.mouse_position = None
        self.last_word = None

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.setInterval(delay)
        self.timer.timeout.connect(self._show)

        self.viewport.setMouseTracking(True)
        self.viewport.installEventFilter(self)
        self.editor.installEventFilter(self)
        self.editor.verticalScrollBar().valueChanged.connect(self.hide)
        self.editor.horizontalScrollBar().valueChanged.connect(self.hide)

    def eventFilter(self, watched, event):
        event_type = event.type()

        if (
            watched is self.viewport
            and event_type == QEvent.MouseMove
        ):
            self.mouse_position = event.pos()
            self.timer.start()
        elif event_type in (
            QEvent.Leave,
            QEvent.MouseButtonPress,
            QEvent.Wheel,
            QEvent.KeyPress,
            QEvent.FocusOut,
        ):
            self.hide()

        return super().eventFilter(watched, event)

    def hide(self):
        self.timer.stop()
        self.last_word = None
        QToolTip.hideText()

    def _show(self):
        if self.mouse_position is None or sip.isdeleted(self.editor):
            return

        cursor = self.editor.cursorForPosition(self.mouse_position)
        cursor.select(QTextCursor.WordUnderCursor)
        word = cursor.selectedText()
        content = self.registry.get(word)

        if content is None:
            self.last_word = word
            QToolTip.hideText()
            return

        if word == self.last_word and QToolTip.isVisible():
            return

        self.last_word = word
        position = self.viewport.mapToGlobal(
            self.mouse_position + TOOLTIP_OFFSET
        )
        QToolTip.showText(
            position,
            render_tooltip(content, self.editor.palette()),
            self.editor,
        )
