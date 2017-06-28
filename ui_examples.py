#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module contains the demos for :mod:`.ui`

Example:
    $ python ui_example.py
"""

import time

import ui


def coloring_demo():
    """Print each color and style"""
    ui.lv1('We have a ton of ANSI color codes and styles such as:')
    for color in ui.COLORS:
        ui.lv3(ui.colorize(color, color))

def icon_demo():
    """Show built-in unicode icons"""
    ui.lv1('Did I forget to mention the ellipsis?', ui.ELLIPSIS)
    ui.lv2('The check?', ui.CHECK)
    ui.lv2('The cross?', ui.CROSS)
    ui.lv2('The block?', ui.BLOCK)
    ui.lv3('They might not appear correctly on windows sadly, but they\'re super cool on bash!')

def enumerations_demo():
    """Demonstate enumerations and timestamps"""
    ui.lv1('You can do pretty enumerations!')
    list_of_things = ["foo", "bar", "baz"]
    for i, thing in enumerate(list_of_things):
        ui.info_count(i, 3, thing)
    print(ui.ELLIPSIS)
    ui.CONFIG['timestamp'] = True
    ui.lv1('And you can add timestamps.')
    list_of_more_things = ["oof", "rab", "zab", "OBOE"]
    for i, thing in enumerate(list_of_more_things, 9):
        ui.info_count(i, 12, thing)
    ui.CONFIG['timestamp'] = False
    ui.lv1('No more timestamps.')
    ui.lv2('It\'s hard to read.')


def progress_demo():
    """Show progress bar"""
    ui.lv1('Unicode progress bar')
    for i in range(11):
        ui.progress_bar(i, 10)
        time.sleep(.1)


def input_options_demo():
    """Show the input options"""
    with_sugar = ui.ask_yes_no("With sugar?", default=False)
    fruits = ["apple", "orange", "banana"]
    selected_fruit = ui.ask_choice("Choose a fruit", fruits)
    ui.lv2(selected_fruit, "with sugar" if with_sugar else "without sugar")


def main():
    """Run all demos"""
    coloring_demo()
    print()
    icon_demo()
    enumerations_demo()
    progress_demo()
    input_options_demo()


if __name__ == '__main__':
    main()
