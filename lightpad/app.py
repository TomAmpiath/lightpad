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
import sys
from typing import List, Optional

from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox

from lightpad import meta
from lightpad.widgets.main_window import MainWindow


class Application(QApplication):

    pwd: str = os.path.expanduser('~')
    current_file: Optional[str] = None
    opened_files: List[str] = []
    open_files: List[str] = []

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setApplicationName(meta['name'])
        self.setApplicationVersion(str(meta['version']))
        self.setApplicationDisplayName(meta['name'])

        self.main_window: MainWindow = MainWindow()
        self.main_window.show()

        self.init_connections()

    def init_connections(self) -> None:
        """Initializes widget connections"""
        self.main_window.menu_bar.open_file_action.triggered.connect(self.on_open_file)
        self.main_window.menu_bar.open_dir_action.triggered.connect(self.on_open_dir)
        self.main_window.menu_bar.save_file_action.triggered.connect(self.on_save_file)
        self.main_window.menu_bar.exit_action.triggered.connect(self.closeAllWindows)

    def on_open_file(self) -> None:
        """Actions to be performed when open file action is triggered"""
        file_path: str = QFileDialog.getOpenFileName(self.main_window, 'Open File', self.pwd)[0]
        if file_path:
            self.current_file = file_path
            self.opened_files.append(file_path)
            self.open_files.append(file_path)

            self.main_window.container_widget.stacked_container.setCurrentWidget(self.main_window.container_widget.editor_screen)
            self.main_window.container_widget.editor_screen.open_file(file_path)

    def on_open_dir(self) -> None:
        """Actions to be performed when open dir action is triggered"""
        dir_path: str = QFileDialog.getExistingDirectory(self.main_window, 'Open Directory', self.pwd)
        if dir_path:
            self.pwd = dir_path

            self.main_window.container_widget.stacked_container.setCurrentWidget(self.main_window.container_widget.editor_screen)

    def on_save_file(self) -> None:
        """Actions to be performed when save file action is triggered"""
        save_file_messagebox: QMessageBox = QMessageBox()
        save_file_messagebox.setWindowTitle('Save File')
        save_file_messagebox.setText('The document has been modified')
        save_file_messagebox.setInformativeText('Do you wish to save your changes?')
        save_file_messagebox.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
        save_file_messagebox.setDefaultButton(QMessageBox.Save)
        ret = save_file_messagebox.exec_()
        if ret == QMessageBox.Save:
            file_contents: str = self.main_window.container_widget.editor_screen.code_editor.toPlainText()
            with open(self.current_file, 'w') as f:
                f.write(file_contents)


def main() -> None:
    app: Application = Application(sys.argv)
    sys.exit(app.exec_())
