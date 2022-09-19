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

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QMenuBar


class MenuBar(QMenuBar):
    """Menu bar of the application"""

    def __init__(self) -> None:
        super().__init__(parent=None)

        self.setNativeMenuBar(False)

        self.file_menu: QMenu = self.addMenu('File')
        self.open_file_action: QAction = QAction('Open File', self)
        self.open_dir_action: QAction = QAction('Open Dir', self)
        self.save_file_action: QAction = QAction('Save File', self)
        self.save_file_as_action: QAction = QAction('Save File As', self)
        self.exit_action: QAction = QAction('Exit', self)
        self.file_menu.addAction(self.open_file_action)
        self.file_menu.addAction(self.open_dir_action)
        self.file_menu.addAction(self.save_file_action)
        self.file_menu.addAction(self.save_file_as_action)
        self.file_menu.addAction(self.exit_action)

        self.edit_menu: QMenu = self.addMenu('Edit')
        self.view_menu: QMenu = self.addMenu('View')
        self.tools_menu: QMenu = self.addMenu('Tools')
        self.windows_menu: QMenu = self.addMenu('Windows')
        self.help_menu: QMenu = self.addMenu('Help')
