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

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QPushButton, QVBoxLayout

from ...utils.commons import init_layout


class ExplorerTree(QFrame):
    """File Explorer Tree"""

    def __init__(self) -> None:
        super().__init__()

        init_layout(self, QVBoxLayout)

        self._exclude_list: List[str] = []
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

        self.load_items(user_home_dir)

        self.layout().addStretch()

    def load_items(self, dir_path: str) -> None:
        """Load folders and files under given dir_path

        Parameters
        ----------
        dir_path: str = Root path to be explored

        Returns
        -------
        None
        """
        for item in chain(
            glob(os.path.join(dir_path, '*')),
            glob(os.path.join(dir_path, '.*')),
        ):
            item_name: str = item.lstrip(dir_path)
            if os.path.isdir(item):
                item_name += '/'
            if item_name not in self._exclude_list:
                button: QPushButton = QPushButton(item_name)
                color = 'blue' if os.path.isdir(item) else 'black'
                button.setStyleSheet(f'border: None; color: {color};')
                self._items_list.append(button)
                self.layout().addWidget(button, alignment=Qt.AlignLeft)
        self.layout().addStretch()
