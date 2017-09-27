#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""This module provides helper functions for pretty, colorized TUIs.
All `sayN` functions take the same args and kwargs as `print`.

All responsibility for correct coloring and stream handling has been removed
to print or colorama.

If you want a pretty progress bar, take a look at `tqdm <https://pypi.python.org/pypi/tqdm>`_.
"""

from __future__ import absolute_import, print_function

from builtins import input
from functools import partial, wraps

from .colors_symbols import CHECK, COLORS, CROSS, ELLIPSIS, colorize


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
    """Print top level information, prefixed with a green `::`.

    Example:
        >>> say1('Make sure to run apt-get with sudo.')
        \x1b[0m\x1b[32;1m::\x1b[0m Make sure to run apt-get with sudo.

    """
    important = colorize('green', '::')
    say(important, *args, **kwargs)


def say2(*args, **kwargs):
    """Print secondary information, prefixed with a green `=>`.

    Example:
        >>> say2('This is some relevant information')
        \x1b[0m\x1b[32;1m=>\x1b[0m This is some relevant information

    """
    relevant = colorize('green', '=>')
    say(relevant, *args, **kwargs)


def say3(*args, **kwargs):
    """Print a block of text indented.

    Example:
            >>> say3('''This a a very,
            ... long paragraph
            ... over many lines
            ... ''')
                This a a very,
                long paragraph
                over many lines

    """
    for block in args:
        for line in block.splitlines():
            say(3 * ' ', line, **kwargs)


def countdown(current, total, *args, **kwargs):
    """Print prefixed with a countdown. Starts from 0.

    Examples:
            >>> countdown(0, 4, 'item 1')
            \x1b[0m\x1b[34;1m*\x1b[0m (1/4) item 1

            >>> countdown(4, 12)
            \x1b[0m\x1b[34;1m*\x1b[0m ( 5/12)

            >>> countdown(4, 10, 'first', 'second', 'third')
            \x1b[0m\x1b[34;1m*\x1b[0m ( 5/10) first second third

    """
    counter_str = "{0} ({1:{width}d}/{2})".format(colorize('blue', "*"),
                                                  current + 1, total,
                                                  width=len(str(total)))

    # Avoid extraneous whitespace
    if args or kwargs:
        say(counter_str, *args, **kwargs)
    else:
        print(counter_str)


def _input():
    """Read input from the user."""
    # this is not strip if made an argument to input
    say(colorize('blue', '>'), end='')
    return input()


def ask_string(question, default=''):
    """Ask the user to enter something.

    Example:
            >>> ask_string("What's your name?", default='No Bo Dy')  # doctest: +SKIP
            :: What's your name? (Default: No Bo Dy)
            > Odysseus
            You chose: Odysseus
            'Odysseus'

    """
    if default:
        question += " (Default: %s)" % default
    say(colorize('blue', '::'), question)
    answer = _input()
    result = answer if answer else default
    print('You chose:', result)
    return result


def ask_bool(question, default=False):
    """Ask the user to answer by yes or no.

    Examples:
        >>> ask_bool('Do you use Linux?')  # doctest: +SKIP
        :: Do you use Linux? [y/N]
        > yes
        You chose: yes
        True

        >>> ask_bool('Are you using python 3?', default=True)  # doctest: +SKIP
        :: Are you using python 3? [Y/n]
        >
        You chose: yes
        True

    """
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
    """Ask the user to choose from a list of choices.

    Example:
        >>> ask_choice('Which editor do you use?', choices=['vim', 'emacs'])  # doctest: +SKIP
        :: Which editor do you use?
            1  vim
            2  emacs
        > 1
        You chose: vim
        'vim'

    """
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
            if answer not in list(range(1, len(choices) + 1)):
                print(answer, "is out of range")
            else:
                choice = choices[answer - 1]
                print('You chose:', choice)
                return choice


def proc(name=None, desc=None):
    """Decorate top level function to print success for failure.

    Examples:
        >>> @proc(desc='frobnicate for a while')  # doctest: +SKIP
        ... def foo():
        ...     pass
        ...
        >>> foo()  # doctest: +SKIP
        foo: frobnicate for a while...... Done

        >>> @proc()  # doctest: +SKIP
        ... def bar():
        ...     '''Bar raises an error.'''
        ...     raise NotImplementedError
        ...
        >>> bar()  # doctest: +SKIP
        bar: Bar raises an error...... Fail
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "/home/vincent/code/python-tui/tui.py", line 216, in _wrap
            name = func.__name__
        File "<stdin>", line 4, in bar
        NotImplementedError

    Args:
        name (str, optional): Defaults to the function's name.
        desc (str, optional): Defaults to the function's docstring.

    """

    def _decor(func):
        @wraps(func)
        def _wrap(name, desc, *args, **kwargs):
            if desc is None:
                desc = func.__doc__.split('\n', 1)[0] \
                    if func.__doc__ else 'no description'
            if name is None:
                name = func.__name__
            print(colorize('green', name + ':'),
                  desc + ELLIPSIS * 2, end=' ', flush=True)
            try:
                result = func(*args, **kwargs)
            except BaseException:
                print(CROSS)
                raise
            print(CHECK)
            return result

        return partial(_wrap, name, desc)

    return _decor


if __name__ == '__main__':
    import doctest
    doctest.testmod()
