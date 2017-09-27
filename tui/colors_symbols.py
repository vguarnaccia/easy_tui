#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""This file contains the helper functions and global variables from the module"""
import os


def _color(code, modifier=None):
    code = '\033[%d' % code
    code += ';%dm' % modifier if modifier is not None else 'm'
    return code


COLORS = {
    # Styles
    'reset': _color(0),
    'bold': _color(1),
    'faint': _color(2),
    'standout': _color(3),
    'underline': _color(4),
    'blink': _color(5),
    'overline': _color(6),

    # Major colors
    'black': _color(30),
    'darkred': _color(31),
    'darkgreen': _color(32),
    'brown': _color(33),
    'darkblue': _color(34),
    'purple': _color(35),
    'teal': _color(36),
    'lightgray': _color(37),

    # Minor colors
    'darkgray': _color(30, 1),
    'red': _color(31, 1),
    'green': _color(32, 1),
    'yellow': _color(33, 1),
    'blue': _color(34, 1),
    'fuchsia': _color(35, 1),
    'turquoise': _color(36, 1),
    'white': _color(37, 1),
}

# Other nice-to-have characters:


def colorize(colors, phrase):
    """Wrap a string in a color"""
    as_string = ''.join(COLORS[color] for color in colors.split())
    return COLORS['reset'] + as_string + phrase + COLORS['reset']


def _characters(color, as_unicode, as_ascii):
    as_string = as_unicode if os.name != 'nt' else as_ascii
    return colorize(color, as_string)


ELLIPSIS = _characters('lightgray', 2 * "…", "...")
CHECK = _characters('green', "✔", "Done")
CROSS = _characters('red', "❌", "Fail")
