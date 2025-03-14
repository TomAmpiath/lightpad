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

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QSplitter, QVBoxLayout

from lightpad.utils.commons import init_layout
from lightpad.widgets.screens.code_area.code_tabs.code_tabs_widget import CodeTabsWidget


class CodeAreaFrame(QFrame):
    """Frame containing code editor and terminal"""

    def __init__(self) -> None:
        super().__init__()

        init_layout(self, QVBoxLayout)

        self._splitter_vertical: QSplitter = QSplitter(Qt.Orientation.Vertical)

        self.code_tabs_widget: CodeTabsWidget = CodeTabsWidget()
        # /* TBD --- Terminal Frame
        # self.terminal_frame = QFrame()
        # self.terminal_frame.setStyleSheet('background: black;')
        # */

        self._splitter_vertical.addWidget(self.code_tabs_widget)
        # self._splitter_vertical.addWidget(self.terminal_frame)

        # self._splitter_vertical.setStretchFactor(0, 8)
        # self._splitter_vertical.setStretchFactor(1, 2)

        self.layout().addWidget(self._splitter_vertical)
