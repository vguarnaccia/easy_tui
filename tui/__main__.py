#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module contains the demos for :mod:`.core`

Example:
    $ python core_example.py
"""

from __future__ import print_function

import time

from . import core


def say_levels():
    """The different levels of say."""
    core.say1("Important info")
    time.sleep(1)
    core.say2("Secondary info")
    time.sleep(1)
    core.say3("This is " + core.colorize('red', 'red'))
    time.sleep(1)
    core.say3("this is " + core.colorize('bold', 'bold'))
    time.sleep(1)


def colors_demo():
    """Print each color and style"""
    core.say1('We have a ton of ANSI color codes and styles such as:')
    for color in core.COLORS:
        core.say3(core.colorize(color, color))
        time.sleep(0.2)


def icon_demo():
    """Show bcorelt-in unicode icons"""
    core.say1('Did I forget to mention the ellipsis?', core.ELLIPSIS)
    time.sleep(1)
    core.say2('The check?', core.CHECK)
    time.sleep(1)
    core.say2('The cross?', core.CROSS)
    time.sleep(1)
    core.say3('They might not appear correctly on windows sadly, but they\'re super cool on bash!')
    time.sleep(2)


def enumerations_demo():
    """Demonstate enumerations and timestamps"""
    core.say1('You can do pretty enumerations!')
    list_of_things = ["foo", "bar", "baz"]
    for i, thing in enumerate(list_of_things):
        core.countdown(i, 3, thing)
        time.sleep(1)


@core.proc(desc="Isn't it great when things work out?")
def this_function_will_succeed():
    """Dumby function"""
    time.sleep(3)


@core.proc()
def fails_always():
    """This function throws an error"""
    time.sleep(3)
    raise NotImplementedError


def input_options_demo():
    """Show the input options"""
    core.say1('TUI is very good at asking questions')
    core.ask_string("What's your favorite website?", default=r'https://github.com')
    core.ask_choice("who's your favorite?",
                    choices=['Doc', 'Grumpy', 'Happy', 'Sleepy', 'Bashful', 'Sneezy', 'Dopey'])
    answer = core.ask_bool('So, do you want to see something cool?', default=True)
    core.say1(core.colorize('bold', 'GREAT!' if answer else 'Too bad.'))


say_levels()
colors_demo()
icon_demo()
enumerations_demo()
input_options_demo()
core.say2('These last two examples are simply a decorator on functions')
this_function_will_succeed()
print()
try:
    fails_always()
except NotImplementedError:
    print()
    core.say1(core.colorize('yellow', 'Thanks!'))
print('\n\n')
