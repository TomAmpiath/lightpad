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

import inspect
import os
import sys
from datetime import datetime
from enum import Enum, auto
from typing import Callable, Optional, Tuple, Union

from PySide6.QtWidgets import QBoxLayout, QMessageBox, QWidget


class DebugType(Enum):
    INFORMATION = auto()
    WARNING = auto()
    CRITICAL = auto()


def debug(*args, debug_type: Optional[DebugType] = DebugType.INFORMATION) -> None:
    if 'LIGHTPAD_DEBUG' in os.environ and os.environ['LIGHTPAD_DEBUG'] == '1':
        message: str = ''
        for arg in args:
            message += str(arg) + ' '
        print(datetime.now(), end='\t')
        if debug_type == DebugType.INFORMATION:
            print('INFO\t', *args, flush=True)
        elif debug_type == DebugType.WARNING:
            print('WARN\t', *args, flush=True)
        else:
            print('CRIT\t', *args, flush=True)


def init_layout(
    widget: QWidget,
    layout: Union[QBoxLayout, Callable],
    layout_spacing: int = 0,
    contents_margins: Tuple[int, int, int, int] = (0, 0, 0, 0),
) -> None:
    """Initialize a layout for the given widget.

    Parameters
    ----------
    widget: QWidget
        The widget to which the layout need to be set.
    layout: Union[QBoxLayout, Callable]
        The layout to be set to the widget.
    layout_spacing: int
        The spacing to be set for the layout. (default is 0)
    contents_margins: Tuple[int, int, int, int]
        The contents margins to be set for the layout. (default is (0, 0, 0, 0))

    Returns
    -------
    None
    """
    widget.setLayout(layout())  # type: ignore
    widget.layout().setSpacing(layout_spacing)
    widget.layout().setContentsMargins(*contents_margins)


def raise_exception(*args, **kwargs) -> None:
    """Open a message window, and show passed items as critical warning"""
    message: str = ''
    for arg in args:
        message += str(arg) + ' '
    message_box: QMessageBox = QMessageBox()
    message_box.setText(message)
    message_box.setIcon(QMessageBox.Critical)  # type: ignore
    message_box.exec()
    debug(message, inspect.stack()[2], debug_type=DebugType.CRITICAL)
    if 'terminate' in kwargs and kwargs['terminate']:
        sys.exit(1)


def string_width(string_to_modify: str, width: int, show_dots: bool = False) -> str:
    """Obtain string of fixed width"""
    string_len: int = len(string_to_modify)
    abs_width: int = abs(width)

    if width > 0:
        if string_len > abs_width:
            return string_to_modify[:abs_width] + '...' if show_dots else string_to_modify[:abs_width]
        elif string_len < abs_width:
            return string_to_modify[:string_len] + ' ' * (abs_width - string_len)
        else:
            return string_to_modify
    elif width < 0:
        if string_len < abs_width:
            return ' ' * (abs_width - string_len) + string_to_modify
        elif string_len > abs_width:
            return '...' + string_to_modify[width:] if show_dots else string_to_modify[width:]
        else:
            return string_to_modify
    else:
        return string_to_modify
