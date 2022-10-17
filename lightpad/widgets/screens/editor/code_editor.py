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

from PySide6.QtCore import QFile
from PySide6.QtGui import QFont, QFontDatabase

from lightpad import base_dir
from lightpad.utils.commons import raise_exception
from lightpad.widgets.screens.editor._plain_text_editor import PlainTextEditor


class CodeEditor(PlainTextEditor):
    """Code Editor widget"""

    def __init__(self) -> None:
        super().__init__()

        font_id: int = QFontDatabase.addApplicationFont(
            os.path.join(
                base_dir,
                os.path.pardir,
                'assets',
                'fonts',
                'CascadiaMono.ttf',
            )
        )
        font_family: str = QFontDatabase.applicationFontFamilies(font_id)[0]
        font: QFont = QFont(font_family)

        self.setFont(font)

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
        file: QFile = QFile(file_path)
        if file.open(QFile.ReadOnly):
            content: str = file.readAll().data().decode('utf8')
            self.setPlainText(content)
        else:
            raise_exception(f'Cannot open file: {file_path}, READ ONLY!')
