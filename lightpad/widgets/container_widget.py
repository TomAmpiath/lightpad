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

from PySide6.QtWidgets import QStackedWidget, QVBoxLayout, QWidget

from lightpad.utils.commons import init_layout
from lightpad.widgets.screens.editor_screen import EditorScreen
from lightpad.widgets.screens.welcome_screen import WelcomeScreen


class ContainerWidget(QWidget):
    """Main Central widget of the application"""

    def __init__(self) -> None:
        super().__init__()

        init_layout(self, QVBoxLayout)
        self.stacked_container: QStackedWidget = QStackedWidget()
        self.layout().addWidget(self.stacked_container)

        self.welcome_screen: WelcomeScreen = WelcomeScreen()
        self.editor_screen: EditorScreen = EditorScreen()

        self.stacked_container.addWidget(self.welcome_screen)
        self.stacked_container.addWidget(self.editor_screen)

        self.stacked_container.setCurrentWidget(self.welcome_screen)
