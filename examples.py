#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module contains the demos for :mod:`.tui`

Example:
    $ python tui_example.py
"""

import time

import tui


def say_levels():
    """This is the example provided by Dimitri Merejkowsky."""
    tui.say1("Important info")
    tui.say2("Secondary info")
    tui.say3("This is " + tui.colorize('red', 'red'))
    tui.say3("this is " + tui.colorize('bold', 'bold'))


def colors_demo():
    """Print each color and style"""
    tui.say1('We have a ton of ANSI color codes and styles such as:')
    for color in tui.COLORS:
        tui.say3(tui.colorize(color, color))


def icon_demo():
    """Show btuilt-in unicode icons"""
    tui.say1('Did I forget to mention the ellipsis?', tui.ELLIPSIS)
    tui.say2('The check?', tui.CHECK)
    tui.say2('The cross?', tui.CROSS)
    tui.say3('They might not appear correctly on windows sadly, but they\'re super cool on bash!')


def enumerations_demo():
    """Demonstate enumerations and timestamps"""
    tui.say1('You can do pretty enumerations!')
    list_of_things = ["foo", "bar", "baz"]
    for i, thing in enumerate(list_of_things):
        tui.countdown(i, 3, thing)


@tui.proc(desc="Isn't it great when things work out?")
def this_function_will_succeed():
    """Dumby function"""
    time.sleep(3)


@tui.proc()
def fails_always():
    """This function throws an error"""
    time.sleep(3)
    raise NotImplementedError


def input_options_demo():
    """Show the input options"""
    tui.say1('TUI is very good at asking questions')
    tui.ask_string("What's your favorite website?", default=r'https://github.com')
    tui.ask_choice("whose your favorite?",
                   choices=['Doc', 'Grumpy', 'Happy', 'Sleepy', 'Bashful', 'Sneezy', 'Dopey'])
    answer = tui.ask_bool('So, do you want to see something cool?', default=True)
    print(tui.colorize('bold', 'GREAT!' if answer else 'Too bad.'))


def main():
    """Run all demos"""
    say_levels()
    colors_demo()
    icon_demo()
    enumerations_demo()
    input_options_demo()
    this_function_will_succeed()
    try:
        fails_always()
    except NotImplementedError:
        print()
        tui.say1(tui.colorize('bold blue', 'Thanks!'))


if __name__ == '__main__':
    main()
