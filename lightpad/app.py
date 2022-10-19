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

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QFileDialog

from lightpad import meta
from lightpad.utils.commons import debug
from lightpad.widgets.main_window import MainWindow


class Application(QApplication):

    pwd: str = os.path.expanduser('~')

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
        self.main_window.menu_bar.new_file_action.triggered.connect(self.on_new_file)  # type: ignore
        self.main_window.menu_bar.open_file_action.triggered.connect(self.on_open_file)  # type: ignore
        self.main_window.menu_bar.open_dir_action.triggered.connect(self.on_open_dir)  # type: ignore
        self.main_window.menu_bar.save_file_action.triggered.connect(self.on_save_file)  # type: ignore
        self.main_window.menu_bar.save_file_as_action.triggered.connect(self.on_save_file_as)  # type: ignore
        self.main_window.menu_bar.exit_action.triggered.connect(self.closeAllWindows)  # type: ignore

    def _open_file(self, file_path: str) -> None:
        """Open given file in code editor"""
        if file_path:
            self.main_window.setCursor(Qt.WaitCursor)

            if self.main_window.container_widget.editor_screen.code_area_frame.code_tabs_widget.open_file(file_path):
                self.main_window.container_widget.stacked_container.setCurrentWidget(
                    self.main_window.container_widget.editor_screen
                )
                self.main_window.menu_bar.save_file_action.setEnabled(True)
                self.main_window.menu_bar.save_file_as_action.setEnabled(True)
            self.main_window.setCursor(Qt.ArrowCursor)

    def on_new_file(self) -> None:
        """Actions to be performed when new file action is triggered"""
        file_path: str = QFileDialog.getSaveFileName(self.main_window, 'Create New File', self.pwd)[0]
        debug('Opening new file: %s' % (file_path))
        self._open_file(file_path)

    def on_open_file(self) -> None:
        """Actions to be performed when open file action is triggered"""
        file_path: str = QFileDialog.getOpenFileName(self.main_window, 'Open File', self.pwd)[0]
        debug('Opening file: %s' % (file_path))
        self._open_file(file_path)

    def on_open_dir(self) -> None:
        """Actions to be performed when open dir action is triggered"""
        dir_path: str = QFileDialog.getExistingDirectory(self.main_window, 'Open Directory', self.pwd)
        debug('Opening dir: %s' % (dir_path))
        if dir_path:
            self.pwd = dir_path

            self.main_window.container_widget.stacked_container.setCurrentWidget(
                self.main_window.container_widget.editor_screen
            )
            self.main_window.menu_bar.save_file_as_action.setEnabled(True)

    def on_save_file(self) -> None:
        """Actions to be performed when save file action is triggered"""
        self.main_window.setCursor(Qt.WaitCursor)
        file_contents: str = self.main_window.container_widget.editor_screen.code_area_frame.code_tabs_widget.get_text()
        current_file: str = (
            self.main_window.container_widget.editor_screen.code_area_frame.code_tabs_widget.currentWidget().file_path
        )
        debug('Saving file: %s' % (current_file))
        with open(current_file, 'w') as f:
            f.write(file_contents)
        self.main_window.setCursor(Qt.ArrowCursor)

    def on_save_file_as(self) -> None:
        """Actions to be performed when save file as action is triggered"""
        file_path: str = QFileDialog.getSaveFileName(self.main_window, 'Save File As', self.pwd)[0]

        self.main_window.setCursor(Qt.WaitCursor)
        file_contents: str = self.main_window.container_widget.editor_screen.code_area_frame.code_tabs_widget.get_text()
        self.main_window.container_widget.editor_screen.code_area_frame.code_tabs_widget.currentWidget().file_path = (
            file_path
        )
        debug('Saving file: %s' % (file_path))
        with open(file_path, 'w') as f:
            f.write(file_contents)
        self.main_window.setCursor(Qt.ArrowCursor)


def main() -> None:
    """Main function of the application"""
    app: Application = Application(sys.argv)
    sys.exit(app.exec())
