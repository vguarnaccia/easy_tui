#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module provides helper functions for pretty, colorized TUIs.
"""

from functools import partial, wraps

from colorama import init

from colors_symbols import CHECK, COLORS, CROSS, ELLIPSIS, colorize

init()


def say(begin, *args, **kwargs):
    """Print with a beginning string.

    Just like print but requires a leading string.

    Example:
        >>> say('::', 'Open the pod bay doors!')
        :: Open the pod bay doors!
    """
    print(begin, end=' ')
    print(*args, **kwargs)


def say1(*args, **kwargs):
    """Print top level information"""
    important = colorize('bold green', '::')
    say(important, *args, **kwargs)


def say2(*args, **kwargs):
    """Print secondary information"""
    relevant = colorize('bold green', '=>')
    say(relevant, *args, **kwargs)


def say3(*args, **kwargs):
    """Print block of text"""
    for block in args:
        for line in block.splitlines():
            say(4 * ' ', line, **kwargs)


def countdown(current, total, *args, **kwargs):
    """Print prefixed with a countdown. Starts from 0.
    >>> info_count(0, 4 'item 1')
    * (1/4) item 1

    >>> info_count(5, 12)
    * ( 5/12)

    >>> info_count(5, 10, 'first', 'second', 'third')
    * ( 5/10) first second third
    """
    counter_str = "{0} ({1:{width}d}/{2})".format(
        colorize('blue', "*"),
        current + 1,
        total,
        width=len(str(total))
    )
    say(counter_str, *args, **kwargs)


def _input():
    """ Read input from the user"""
    return input(colorize('blue', '> '))


def ask_string(question, default=''):
    """Ask the user to enter something"""
    if default:
        question += " (Default: %s)" % default
    say(colorize('blue', '::'), question)
    answer = _input()
    result = answer if answer else default
    print('You chose:', result)
    return result


def ask_bool(question, default=False):
    """Ask the user to answer by yes or no"""
    while True:
        say(colorize('blue', '::'), question, '[Y/n]' if default else '[y/N]')
        answer = _input()
        if answer.lower() in ["y", "yes"]:
            print('You chose: yes')
            return True
        if answer.lower() in ["n", "no"]:
            print('You chose: no')
            return False
        if not answer:
            answer = 'yes' if default else 'no'
            print('You chose:', answer)
            return default
        print("Please answer by 'y' (yes) or 'n' (no) ")


def ask_choice(question, choices):
    """Ask the user to choose from a list of choices."""
    say(colorize('blue', '::'), question)
    choices = list(choices)
    for i, choice in enumerate(choices, start=1):
        print("  ", COLORS['blue'], i, COLORS['reset'], choice)

    # Keep asking user for valid input. Fail on Ctrl-C
    while True:
        try:
            answer = int(_input())
        except KeyboardInterrupt:
            raise  # there's potential here
        except ValueError:
            print("Please enter a valid number")
        else:
            if answer not in range(1, len(choices) + 1):
                print(answer, "is out of range")
            else:
                choice = choices[answer - 1]
                print('You chose:', choice)
                return choice


def proc(name=None, desc=None):
    """Decorate top level function to print success for failure.
    Usage:

        @proc
        def foo(x, y, x):
            ...


    Args:
        name (str, optional): Defaults to the function's name.
        desc (str, optional): Defaults to the function's docstring.

    Return:
        Prints the following ascci string, or a colorized unicode variant:
            {name}: {desc}...... Done/Fail
    """
    def _decor(func):
        @wraps(func)
        def _wrap(name, desc, *args, **kwargs):
            if desc is None:
                desc = func.__doc__.split('\n', 1)[0]  # first line of docstring
            if name is None:
                name = func.__name__
            print(colorize('green', name + ':'), desc + ELLIPSIS * 2, end=' ', flush=True)
            try:
                result = func(*args, **kwargs)
            except:
                print(CROSS)
                raise
            print(CHECK)
            return result
        return partial(_wrap, name, desc)
    return _decor
