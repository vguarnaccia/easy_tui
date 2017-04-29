#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module contains the demos for :mod:`.ui`

Example:
    $ python ui_example.py
"""

import ui


def coloring_demo():
    """Print each color and style"""
    ui.info(
        'We have a ton of ANSI color codes and styles such as:\n',
        ui.bold, "bold\n", ui.reset,
        ui.faint, "faint\n", ui.reset,
        ui.standout, "standout (italics)\n", ui.reset,
        ui.underline, "underline" + ui.reset + "\n",  # reset before space sep
        ui.blink, "blink\n", ui.reset,
        ui.overline, "overline\n", ui.reset,

        ui.black, "black\n", ui.reset,
        ui.darkred, "darkred\n", ui.reset,
        ui.darkgreen, "darkgreen\n", ui.reset,
        ui.brown, "brown\n", ui.reset,
        ui.darkblue, "darkblue\n", ui.reset,
        ui.purple, "purple\n", ui.reset,
        ui.teal, "teal\n", ui.reset,
        ui.lightgray, "lightgray\n", ui.reset,

        ui.darkgray, "darkgray\n", ui.reset,
        ui.red, "red\n", ui.reset,
        ui.green, "green\n", ui.reset,
        ui.yellow, "yellow\n", ui.reset,
        ui.blue, "blue\n", ui.reset,
        ui.fuchsia, "fuchsia\n", ui.reset,
        ui.turquoise, "turquoise\n", ui.reset,
        ui.white, "white\n", ui.reset,

        'And a few color aliases like',
        ui.darkteal, "darkteal which is turquoise,", ui.reset,
        ui.darkyellow, "darkyellow which is brown,", ui.reset,
        ui.fuscia, "and fuscia which is fuchsia.", ui.reset,
    )


def icon_demo():
    """Show built-in unicode icons"""
    ui.info(
        'Did I forget to mention the ellipsis, ',
        ui.ellipsis,
        ', the check, ',
        ui.check,
        ', or the cross ',
        ui.cross,
        '?\n They might not appear '
        'correctly on windows, sadly, but they\'re super cool on bash!',
        sep=''
    )


def enumerations_demo():
    """Demonstate enumerations and timestamps"""
    ui.info('You can do pretty enumerations!')
    list_of_things = ["foo", "bar", "baz"]
    for i, thing in enumerate(list_of_things):
        ui.info_count(i, 12, thing)
    ui.info(ui.ellipsis)
    ui.CONFIG['timestamp'] = True
    ui.info('And you can add timestamps.')
    list_of_more_things = ["oof", "rab", "zab", "OBOE"]
    for i, thing in enumerate(list_of_more_things, 9):
        ui.info_count(i, 12, thing)
    ui.CONFIG['timestamp'] = False
    ui.info('No more timestamps.')


def progress_demo():
    """Show progress bar"""
    ui.info_progress("Done", 5, 20)
    ui.time.sleep(1)
    ui.info_progress("Done", 10, 20)
    ui.time.sleep(1)
    ui.info_progress("Done", 20, 20)
    ui.time.sleep(1)


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
