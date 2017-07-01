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
    """This is the example provided by Dimitri Merejkowsky."""
    core.say1("Important info")
    core.say2("Secondary info")
    core.say3("This is " + core.colorize('red', 'red'))
    core.say3("this is " + core.colorize('bold', 'bold'))


def colors_demo():
    """Print each color and style"""
    core.say1('We have a ton of ANSI color codes and styles such as:')
    for color in core.COLORS:
        core.say3(core.colorize(color, color))


def icon_demo():
    """Show bcorelt-in unicode icons"""
    core.say1('Did I forget to mention the ellipsis?', core.ELLIPSIS)
    core.say2('The check?', core.CHECK)
    core.say2('The cross?', core.CROSS)
    core.say3('They might not appear correctly on windows sadly, but they\'re super cool on bash!')


def enumerations_demo():
    """Demonstate enumerations and timestamps"""
    core.say1('You can do pretty enumerations!')
    list_of_things = ["foo", "bar", "baz"]
    for i, thing in enumerate(list_of_things):
        core.countdown(i, 3, thing)


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
    core.say1('core is very good at asking questions')
    core.ask_string("What's your favorite website?", default=r'https://github.com')
    core.ask_choice("whose your favorite?",
                    choices=['Doc', 'Grumpy', 'Happy', 'Sleepy', 'Bashful', 'Sneezy', 'Dopey'])
    answer = core.ask_bool('So, do you want to see something cool?', default=True)
    print(core.colorize('bold', 'GREAT!' if answer else 'Too bad.'))


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
    core.say1(core.colorize('yellow', 'Thanks!'))
