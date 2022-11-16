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

import os

from PySide6.QtCore import QFileInfo, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFileIconProvider, QFrame, QPushButton, QVBoxLayout

from lightpad.utils.colors import BASE_COLOR, SHADE, get_color
from lightpad.utils.commons import debug, init_layout
from lightpad.utils.custom_typing import HexColor


class ExplorerItem(QFrame):
    """File or directory item in explorer tree"""

    def __init__(self, item_abs_path: str) -> None:
        super().__init__()

        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.item_abs_path: str = item_abs_path
        self.item_name = str = os.path.basename(os.path.normpath(self.item_abs_path))
        self._file_icon_provider: QFileIconProvider = QFileIconProvider()
        self.icon: QIcon = self._file_icon_provider.icon(QFileInfo(self.item_abs_path))
        self.is_dir: bool = os.path.isdir(self.item_abs_path)

        init_layout(self, QVBoxLayout, layout_spacing=2)

        self.item_button: QPushButton = QPushButton(self.item_name)
        self.item_button.setIcon(self.icon)
        item_color: HexColor = (
            get_color(BASE_COLOR.BLUE, SHADE.NORMAL) if self.is_dir else get_color(BASE_COLOR.GREY, SHADE.EXTRA_DARK)
        )
        self.item_button.setStyleSheet('border: None; color: %s;' % (item_color))
        self.layout().addWidget(self.item_button)
