#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module contains the demos for :mod:`.tui`

Example:
    $ python tui_example.py
"""

import tui


def coloring_demo():
    """Print each color and style"""
    tui.say1('We have a ton of ANSI color codes and styles such as:')
    for color in tui.COLORS:
        tui.say3(tui.colorize(color, color))

def icon_demo():
    """Show btuilt-in unicode icons"""
    tui.say1('Did I forget to mention the ellipsis?', tui.ELLIPSIS)
    tui.say2('The check?', tui.CHECK)
    tui.say2('The cross?', tui.CROSS)
    tui.say2('The block?', tui.BLOCK)
    tui.say3('They might not appear correctly on windows sadly, but they\'re super cool on bash!')

def enumerations_demo():
    """Demonstate enumerations and timestamps"""
    tui.say1('You can do pretty enumerations!')
    list_of_things = ["foo", "bar", "baz"]
    for i, thing in enumerate(list_of_things):
        tui.countdown(i, 3, thing)
    print(tui.ELLIPSIS)
    tui.CONFIG['timestamp'] = True
    tui.say1('And you can add timestamps.')
    list_of_more_things = ["oof", "rab", "zab", "OBOE"]
    for i, thing in enumerate(list_of_more_things, 9):
        tui.countdown(i, 12, thing)
    tui.CONFIG['timestamp'] = False
    tui.say1('No more timestamps.')
    tui.say2('It\'s hard to read.')


def input_options_demo():
    """Show the input options"""
    with_sugar = tui.ask_bool("With sugar?", default=False)
    fruits = ["apple", "orange", "banana"]
    selected_fruit = tui.ask_choice("Choose a fruit", fruits)
    tui.say2(selected_fruit, "with sugar" if with_sugar else "without sugar")


def main():
    """Run all demos"""
    coloring_demo()
    print()
    icon_demo()
    enumerations_demo()
    input_options_demo()


def example():
    """This is the example provided by Dimitri Merejkowsky."""
    tui.say1("Important info")
    tui.say2("Secondary info")
    tui.say3("This is", tui.colorize('red', 'red'))
    tui.say3("this is", tui.colorize('bold', 'bold'))
    list_of_things = ["foo", "bar", "baz"]
    for j, thing in enumerate(list_of_things):
        tui.countdown(j, len(list_of_things), thing)
    print("\n", tui.CHECK, "all done")
    fruits = ["apple", "orange", "banana"]
    answer = tui.ask_choice("Choose a frtuit", fruits)
    print("You chose:", answer)


if __name__ == '__main__':
    example()
    main()
