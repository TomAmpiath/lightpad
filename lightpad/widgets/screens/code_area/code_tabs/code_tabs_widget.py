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
from typing import Dict

from PySide6.QtWidgets import QTabWidget

from lightpad.widgets.screens.code_area.code_tabs.editor.code_editor import CodeEditor


class CodeTabsWidget(QTabWidget):
    """Handles code editor tabs"""

    def __init__(self) -> None:
        super().__init__()

        self._opened_files_dict: Dict[str, CodeEditor] = {}

        self.setTabsClosable(True)
        self.setMovable(True)

        self.tabCloseRequested.connect(self.removeTab)  # type: ignore

    def open_file(self, file_path: str) -> bool:
        """Create a new code editor tab for the given file.

        Returns
        -------
        status: bool
            True if file was successfully opened, else False.
        """
        status: bool = True
        if file_path in self._opened_files_dict.keys():
            code_editor: CodeEditor = self._opened_files_dict[file_path]
            self.setCurrentWidget(code_editor)
        else:
            code_editor_instance: CodeEditor = CodeEditor()
            status = code_editor_instance.open_file(file_path)
            if status:
                file_name: str = os.path.basename(os.path.normpath(file_path))
                self.addTab(code_editor_instance, file_name)
                self.setCurrentWidget(code_editor_instance)
                self._opened_files_dict[file_path] = code_editor_instance
            else:
                del code_editor_instance
        return status

    def get_text(self) -> str:
        """Get text of current code editor tab.

        Returns
        -------
        text: str
            Text of current code editor tab.
        """
        return self.currentWidget().toPlainText()  # type: ignore
