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
from PySide6.QtWidgets import QFrame, QHBoxLayout, QSplitter

from lightpad.utils.commons import init_layout
from lightpad.widgets.screens.code_area.code_area_frame import CodeAreaFrame
from lightpad.widgets.screens.side_bar.side_bar_widget import SideBarWidget
from lightpad.widgets.screens.side_bar.stacked_widget import StackedWidget


class EditorScreen(QFrame):
    """This screen contains the text editor and other assistance widges."""

    def __init__(self):
        super().__init__()

        self.setStyleSheet('background: white; color: black;')

        init_layout(self, QHBoxLayout)

        self._splitter_horizontal: QSplitter = QSplitter(Qt.Horizontal)

        self.stacked_widget: StackedWidget = StackedWidget()
        self.code_area_frame: CodeAreaFrame = CodeAreaFrame()

        self._splitter_horizontal.addWidget(self.stacked_widget)
        self._splitter_horizontal.addWidget(self.code_area_frame)

        self._splitter_horizontal.setStretchFactor(0, 2)
        self._splitter_horizontal.setStretchFactor(1, 8)

        self.side_bar_widget: SideBarWidget = SideBarWidget()

        self.layout().addWidget(self.side_bar_widget)
        self.layout().addWidget(self._splitter_horizontal)
