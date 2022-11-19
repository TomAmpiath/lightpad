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

from __future__ import annotations

from enum import Enum, auto

from lightpad.utils.commons import raise_exception
from lightpad.utils.custom_typing import HexColor


class BASE_COLOR(Enum):
    GREY = auto()
    RED = auto()
    GREEN = auto()
    BLUE = auto()


class SHADE(Enum):
    EXTRA_LIGHT = auto()
    LIGHTER = auto()
    LIGHT = auto()
    NORMAL = auto()
    DARK = auto()
    DARKER = auto()
    EXTRA_DARK = auto()


class _RGB:
    def __init__(self: _RGB, red: int, green: int, blue: int) -> None:
        if not all([color in range(0, 256) for color in (red, green, blue)]):
            raise_exception('Unsupported RGB values', terminate=True)
        self.red = red
        self.green = green
        self.blue = blue

    def get_hexcolor(self) -> HexColor:
        return '#%02x%02x%02x' % (self.red, self.green, self.blue)

    def __add__(self: _RGB, rgb_instance: _RGB) -> _RGB:
        return _RGB(
            min(self.red + rgb_instance.red, 255),
            min(self.green + rgb_instance.green, 255),
            min(self.blue + rgb_instance.blue, 255),
        )

    def __sub__(self: _RGB, rgb_instance: _RGB) -> _RGB:
        return _RGB(
            max(self.red - rgb_instance.red, 0),
            max(self.green - rgb_instance.green, 0),
            max(self.blue - rgb_instance.blue, 0),
        )

    def __mul__(self: _RGB, scalar: float) -> _RGB:
        if not 0 <= scalar:
            raise_exception('Unsupported scalar used for RGB multiplication', terminate=True)
        return _RGB(
            min(int(self.red * scalar), 255),
            min(int(self.green * scalar), 255),
            min(int(self.blue * scalar), 255),
        )

    def __truediv__(self: _RGB, scalar: float) -> _RGB:
        if not 0 < scalar:
            raise_exception('Unsupported scalar used for RGB division', terminate=True)
        return _RGB(
            max(int(self.red / scalar), 0),
            max(int(self.green / scalar), 0),
            max(int(self.blue / scalar), 0),
        )

    def __repr__(self) -> str:
        return f'_RGB(red: {self.red}, green: {self.green}, blue: {self.blue})'


def _get_base_color_rgb(base_color: BASE_COLOR) -> _RGB:
    rgb_color: _RGB = _RGB(0, 0, 0)

    if base_color == BASE_COLOR.GREY:
        rgb_color = _RGB(127, 127, 127)
    elif base_color == BASE_COLOR.RED:
        rgb_color = _RGB(127, 0, 0)
    elif base_color == BASE_COLOR.GREEN:
        rgb_color = _RGB(0, 127, 0)
    elif base_color == BASE_COLOR.BLUE:
        rgb_color = _RGB(0, 0, 127)
    else:
        raise_exception('Unsupported base color!', terminate=True)

    return rgb_color


def _get_shaded_color(rgb_color: _RGB, shade: SHADE) -> _RGB:
    shaded_color: _RGB = _RGB(0, 0, 0)

    if shade == SHADE.EXTRA_DARK:
        shaded_color = rgb_color / 5.0
    elif shade == SHADE.DARKER:
        shaded_color = rgb_color / 2.22
    elif shade == SHADE.DARK:
        shaded_color = rgb_color / 1.33
    elif shade == SHADE.NORMAL:
        shaded_color = rgb_color * 1.0
    elif shade == SHADE.LIGHT:
        shaded_color = rgb_color * 1.25
    elif shade == SHADE.LIGHTER:
        shaded_color = rgb_color * 1.55
    elif shade == SHADE.EXTRA_LIGHT:
        shaded_color = rgb_color * 1.8
    else:
        raise_exception('Unsupported shade!', terminate=True)

    return shaded_color


def get_rgb_color(red_shade: SHADE, green_shade: SHADE, blue_shade: SHADE) -> HexColor:
    """Get color from given shades.

    Parameters
    ----------
    red_shade: SHADE
        Shade of red
    green_shade: SHADE
        Shade of green
    blue_shade: SHADE
        Shade of blue

    Returns
    -------
    rgb_color: HexColor
        RGB color of given shades.
    """
    shaded_red = _get_shaded_color(_get_base_color_rgb(BASE_COLOR.RED), red_shade)
    shaded_green = _get_shaded_color(_get_base_color_rgb(BASE_COLOR.GREEN), green_shade)
    shaded_blue = _get_shaded_color(_get_base_color_rgb(BASE_COLOR.BLUE), blue_shade)

    rgb_color: HexColor = (shaded_red + shaded_green + shaded_blue).get_hexcolor()

    return rgb_color


def get_color(base_color: BASE_COLOR, shade: SHADE) -> HexColor:
    """Get color of given base color with given shade.

    Parameters
    ----------
    base_color: BASE_COLOR
        Base color enum.
    shade: SHADE
        Shade of color enum.

    Returns
    -------
    color: HexColor
        HexColor value for the color.
    """
    rgb_color: _RGB = _get_base_color_rgb(base_color)
    rgb_color = _get_shaded_color(rgb_color, shade)

    color: HexColor = rgb_color.get_hexcolor()
    return color
