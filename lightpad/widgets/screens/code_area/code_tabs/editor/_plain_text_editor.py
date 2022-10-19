#  MIT License
#
#  Copyright (c) 2022 Tom George Ampiath
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#

from PySide6.QtCore import QRect, Qt, Slot
from PySide6.QtGui import QColor, QPainter, QPaintEvent, QResizeEvent, QTextFormat
from PySide6.QtWidgets import QPlainTextEdit, QTextEdit

from lightpad.widgets.screens.code_area.code_tabs.editor._line_number_area import LineNumberArea


class PlainTextEditor(QPlainTextEdit):
    """Text editor implementation"""

    def __init__(self) -> None:
        super().__init__()

        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

        self.line_number_area: LineNumberArea = LineNumberArea(self)

        self.blockCountChanged[int].connect(self.update_line_number_area_width)  # type: ignore
        self.updateRequest[QRect, int].connect(self.update_line_number_area)  # type: ignore
        self.cursorPositionChanged.connect(self.highlight_current_line)  # type: ignore

        self.update_line_number_area_width(0)
        self.highlight_current_line()

    def line_number_area_width(self) -> int:
        """Returns the width of line number area."""
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num *= 0.1
            digits += 1

        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def resizeEvent(self, e: QResizeEvent) -> None:
        super().resizeEvent(e)
        cr = self.contentsRect()
        width = self.line_number_area_width()
        rect = QRect(cr.left(), cr.top(), width, cr.height())
        self.line_number_area.setGeometry(rect)

    def line_number_area_paint_event(self, event: QPaintEvent) -> None:
        """overrides paint event for line number area"""
        with QPainter(self.line_number_area) as painter:
            painter.fillRect(event.rect(), Qt.lightGray)
            block = self.firstVisibleBlock()
            block_number = block.blockNumber()
            offset = self.contentOffset()
            top = self.blockBoundingGeometry(block).translated(offset).top()
            bottom = top + self.blockBoundingRect(block).height()

            while block.isValid() and top <= event.rect().bottom():
                if block.isVisible() and bottom >= event.rect().top():
                    number = str(block_number + 1)
                    painter.setPen(Qt.black)
                    width = self.line_number_area.width()
                    height = self.fontMetrics().height()
                    painter.drawText(0, top, width, height, Qt.AlignRight, number)  # type: ignore

                block = block.next()
                top = bottom
                bottom = top + self.blockBoundingRect(block).height()
                block_number += 1

    @Slot(int)
    def update_line_number_area_width(self, newBlockCount: int) -> None:
        """Signal slot to update line number area width based on newBlockCount"""
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    @Slot(QRect, int)
    def update_line_number_area(self, rect: QRect, dy: int) -> None:
        """Signal slot to update line number area based on update request"""
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            width = self.line_number_area.width()
            self.line_number_area.update(0, rect.y(), width, rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    @Slot()
    def highlight_current_line(self) -> None:
        """Signal slot to implement line highlighting"""
        extra_selections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()

            line_color = QColor(Qt.yellow).lighter(160)
            selection.format.setBackground(line_color)  # type: ignore

            selection.format.setProperty(QTextFormat.FullWidthSelection, True)  # type: ignore

            selection.cursor = self.textCursor()  # type: ignore
            selection.cursor.clearSelection()  # type: ignore

            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)
