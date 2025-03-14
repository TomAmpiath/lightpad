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
import time

from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont, QFontDatabase

from lightpad import base_dir
from lightpad.utils.commons import debug, raise_exception
from lightpad.widgets.screens.code_area.code_tabs.editor._plain_text_editor import PlainTextEditor


class CodeEditor(PlainTextEditor):
    """Code Editor widget"""

    def __init__(self) -> None:
        super().__init__()

        self.file_path: str = os.path.join(os.path.expanduser('~'), 'unnamed')  # default file path
        self.content_view: memoryview = memoryview(b'')
        self.content_index: int = 0

        self.start_time: float = 0.0

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
        font: QFont = QFont(font_family, 12)

        self.setFont(font)

        self.content_update_timer: QTimer = QTimer()
        self.content_update_timer.timeout.connect(self.update_content)  # type: ignore

    def update_content(self) -> None:
        content = self.content_view[self.content_index : self.content_index + 10_000].tobytes().decode('utf-8')
        if content:
            self.appendPlainText(content)
            self.content_index += 10_000
        else:
            self.content_update_timer.stop()
            debug(f'Took: %.2f seconds to read %s' % (time.monotonic() - self.start_time, self.file_path))

    def open_file(self, file_path: str) -> bool:
        """Open file for editing.

        Parameters
        ----------
        file_path: str
            The path to file to be opened.

        Returns
        -------
        status: bool
            True if file was successfully opened, else False.
        """
        self.start_time = time.monotonic()
        try:
            content: str = ''

            if os.path.isfile(file_path):
                with open(file_path, 'rb') as f:
                    self.content_view = memoryview(f.read())
                    content = self.content_view[:10_000].tobytes().decode('utf-8')
                    self.content_index += 10_000
                    self.content_update_timer.start(100)

            self.setPlainText(content)
            self.file_path = file_path
            return True
        except:
            raise_exception(f'Unsupported file type!', terminate=False)
            debug('Could not open file: %s' % (file_path))
            return False
