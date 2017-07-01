#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Call doctests on TUI"""


if __name__ == "__main__":
    TEST = True
    import doctest
    doctest.testfile('tui/tui.py')
else:
    TEST = False
