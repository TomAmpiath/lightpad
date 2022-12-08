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

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QTabWidget

from lightpad.utils.commons import debug
from lightpad.widgets.screens.code_area.code_tabs.editor.code_editor import CodeEditor


class CodeTabsWidget(QTabWidget):
    """Handles code editor tabs"""

    all_tabs_closed_signal: Signal = Signal()

    def __init__(self) -> None:
        super().__init__()

        self._opened_files_dict: Dict[str, CodeEditor] = {}

        self.setTabsClosable(True)
        self.setMovable(True)

        self.tabCloseRequested.connect(self.handle_tab_close)  # type: ignore

    def handle_tab_close(self, index: int) -> None:
        """Actions to be performed when a tab is closed.

        Parameters
        ----------
        index: int
            Index of the closed tab.

        Returns
        -------
        None
        """
        code_editor_instance: CodeEditor = self.widget(index)  # type: ignore
        file_path: str = list(self._opened_files_dict.keys())[
            list(self._opened_files_dict.values()).index(code_editor_instance)
        ]
        self._opened_files_dict.pop(file_path, None)
        debug('poping %s from cached file paths' % (file_path))
        self.removeTab(index)
        code_editor_instance.content_update_timer.stop()
        del code_editor_instance.content_view
        code_editor_instance.clear()
        del code_editor_instance

        if self.count() == 0:
            self.all_tabs_closed_signal.emit()

    def open_file(self, file_path: str) -> bool:
        """Create a new code editor tab for the given file.

        Parameters
        ----------
        file_path: str
            Path of file to be opened.

        Returns
        -------
        status: bool
            True if file was successfully opened, else False.
        """
        status: bool = True
        if file_path in self._opened_files_dict.keys():
            debug('File path is already present in an opened tab')
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
