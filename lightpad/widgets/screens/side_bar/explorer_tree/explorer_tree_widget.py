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
from configparser import ConfigParser
from glob import glob
from itertools import chain
from typing import List

from PySide6.QtCore import QFileInfo, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QFileIconProvider,
    QFrame,
    QLayout,
    QLayoutItem,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from lightpad.utils.commons import init_layout


class ExplorerTreeWidget(QFrame):
    """File Explorer Tree"""

    def __init__(self) -> None:
        super().__init__()

        self._exclude_list: List[str] = []
        self._file_icon_provider: QFileIconProvider = QFileIconProvider()

        user_home_dir: str = os.path.expanduser('~')
        git_config_file: str = os.path.join(user_home_dir, '.gitconfig')

        if os.path.exists(git_config_file):
            config: ConfigParser = ConfigParser()
            config.read(git_config_file)

            if config.has_option('Core', 'excludefile'):
                git_global_ignore_file: str = config['Core']['excludefile']

                with open(git_global_ignore_file, 'r') as f:
                    for line in f:
                        self._exclude_list.append(line.replace('\n', ''))

        self._items_list: List[QPushButton] = []

        init_layout(self, QVBoxLayout)

        self._scroll_area: QScrollArea = QScrollArea()
        self._scroll_widget: QWidget = QWidget()
        self._scroll_area.setWidget(self._scroll_widget)
        self._scroll_area.setWidgetResizable(True)
        init_layout(
            self._scroll_widget,
            QVBoxLayout,
            layout_spacing=4,
            contents_margins=(4, 2, 2, 2),
        )

        self.load_items(user_home_dir)

        self.layout().addWidget(self._scroll_area)

    def clear_layout_items(self, layout: QLayout) -> None:
        """Clear all items in the layouto

        Parameters
        ----------
        layout: QLayout
            The layout from which we want to clear items

        Returns
        -------
        None
        """
        while layout.count():
            item: QLayoutItem = layout.itemAt(0)
            widget: QWidget = item.widget()
            if widget is not None:
                item.widget().setParent(None)  # type: ignore
                item.widget().deleteLater()
            else:
                self.clear_layout_items(item.layout())  # type: ignore

    def load_items(self, dir_path: str) -> None:
        """Load folders and files under given dir_path

        Parameters
        ----------
        dir_path: str
            Root path to be explored

        Returns
        -------
        None
        """
        self.clear_layout_items(self._scroll_widget.layout())
        for item in chain(
            glob(os.path.join(dir_path, '*')),
            glob(os.path.join(dir_path, '.*')),
        ):
            icon: QIcon = self._file_icon_provider.icon(QFileInfo(item))
            item_name: str = os.path.basename(os.path.normpath(item))
            if os.path.isdir(item):
                item_name += '/'
            if item_name not in self._exclude_list:
                button: QPushButton = QPushButton(item_name)
                button.setIcon(icon)
                color = 'blue' if os.path.isdir(item) else 'black'
                button.setStyleSheet(f'border: None; color: {color};')
                self._items_list.append(button)
                self._scroll_widget.layout().addWidget(button, alignment=Qt.AlignLeft)  # type: ignore
        self._scroll_widget.layout().addStretch()  # type: ignore
