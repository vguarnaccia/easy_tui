#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module contains the demos for :mod:`.ui`

Example:
    $ python ui_example.py
"""

import ui
from tqdm import tqdm


def coloring_demo():
    """Print each color and style"""
    ui.info_1(
        'We have a ton of ANSI color codes and styles such as:',
        ui.bold, "bold",
        ui.faint, "faint",
        ui.standout, "standout (italics)",
        ui.underline, "underline",
        ui.blink, "blink",
        ui.overline, "overline",

        ui.black, "black",
        ui.darkred, "darkred",
        ui.darkgreen, "darkgreen",
        ui.brown, "brown",
        ui.darkblue, "darkblue",
        ui.purple, "purple",
        ui.teal, "teal",
        ui.lightgray, "lightgray",

        ui.darkgray, "darkgray",
        ui.red, "red",
        ui.green, "green",
        ui.yellow, "yellow",
        ui.blue, "blue",
        ui.fuchsia, "fuchsia",
        ui.turquoise, "turquoise",
        ui.white, "white",

        'And a few color aliases like:',
        ui.darkteal, "darkteal" + ui.reset + " which is turquoise,",
        ui.darkyellow, "darkyellow" + ui.reset + " which is brown,",
        "and " + ui.fuscia + "fuscia" + ui.reset + " which is fuchsia.",
        sep=(ui.reset + '\n' + ui.tabs(2))
    )


def icon_demo():
    """Show built-in unicode icons"""
    ui.info_1(
        'Did I forget to mention the ellipsis, ',
        ui.ellipsis,
        ', the check, ',
        ui.check,
        ', or the cross ',
        ui.cross,
        '?\n They might not appear '
        'correctly on windows, sadly, but they\'re super cool on bash!',
    )


def enumerations_demo():
    """Demonstate enumerations and timestamps"""
    ui.info_1('You can do pretty enumerations!')
    list_of_things = ["foo", "bar", "baz"]
    for i, thing in enumerate(list_of_things):
        ui.info_count(i, 12, thing)
    ui.info(ui.ellipsis)
    ui.CONFIG['timestamp'] = True
    ui.info_1('And you can add timestamps.')
    list_of_more_things = ["oof", "rab", "zab", "OBOE"]
    for i, thing in enumerate(list_of_more_things, 9):
        ui.info_count(i, 12, thing)
    ui.CONFIG['timestamp'] = False
    ui.info_1('No more timestamps.')
    ui.info_2('It\'s hard to read.')


def progress_demo():
    """Show progress bar"""
    ui.info_1('Unicode progress bar')
    for _ in tqdm(range(10)):
        ui.time.sleep(.1)
    ui.info_1('ASCII progress bar')
    for _ in tqdm(range(10), ascii=True):
        ui.time.sleep(.1)


def input_options_demo():
    """Show the input options"""
    with_sugar = ui.ask_yes_no("With sugar?", default=False)
    fruits = ["apple", "orange", "banana"]
    selected_fruit = ui.ask_choice("Choose a fruit", fruits)
    ui.info(selected_fruit, "with sugar" if with_sugar else "without sugar")


def main():
    """Run all demos"""
    coloring_demo()
    ui.info()
    icon_demo()
    enumerations_demo()
    progress_demo()
    input_options_demo()


if __name__ == '__main__':
    main()
