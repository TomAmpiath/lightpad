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
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout

from lightpad import meta
from lightpad.utils.commons import init_layout


class WelcomeScreen(QFrame):
    """This is the screen shown when the app is opened"""

    def __init__(self) -> None:
        super().__init__()

        init_layout(self, QVBoxLayout, layout_spacing=8)

        self.setStyleSheet('background: white; color: black;')

        self.layout().addWidget(QLabel('Welcome'), alignment=Qt.AlignmentFlag.AlignCenter)  # type: ignore
        self.layout().addWidget(
            QLabel(f'{meta["name"]} - version {meta["version"]}'),
            alignment=Qt.AlignmentFlag.AlignCenter,  # type: ignore
        )
        self.layout().addWidget(
            QLabel(f'{meta["description"]}'), alignment=Qt.AlignmentFlag.AlignCenter
        )  # type: ignore
        self.layout().addStretch()  # type: ignore

        self.layout().itemAt(0).widget().setStyleSheet('font-size: 96px;')
