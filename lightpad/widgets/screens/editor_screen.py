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
from lightpad.widgets.editor.code_editor import CodeEditor
from lightpad.widgets.editor.explorer_tree import ExplorerTree


class EditorScreen(QFrame):
    """This screen contains the text editor and other assistance widges."""

    def __init__(self):
        super().__init__()

        self.setStyleSheet('background: white; color: black;')

        init_layout(self, QHBoxLayout)

        self._splitter_horizontal: QSplitter = QSplitter(Qt.Horizontal)
        self._splitter_horizontal.setSizes((200, 200))

        self.explorer_tree: ExplorerTree = ExplorerTree()
        self.code_editor: CodeEditor = CodeEditor()

        self._splitter_horizontal.addWidget(self.explorer_tree)
        self._splitter_horizontal.addWidget(self.code_editor)

        self.layout().addWidget(self._splitter_horizontal)

    def open_file(self, file_path: str) -> None:
        """Open file for editing.

        Parameters
        ----------
        file_path: str
            The path to file to be opened.

        Returns
        -------
        None
        """
        with open(file_path, 'r') as f:
            self.code_editor.setPlainText(f.read())
            self.code_editor.setFocus()
