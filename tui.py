#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module provides helper functions for pretty, colorized TUIs.
"""
import difflib
import os
import sys

from colorama import init

from colors_symbols import *

init()
# Global variable to store configuration

CONFIG = {
    "verbose": os.environ.get("VERBOSE"),
    "quiet": False,
    "timestamp": False,
}


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
        current+1,
        total,
        width=len(str(total))
    )
    say(counter_str, *args, **kwargs)


def progress_bar(
        iteration,
        total,
        prefix='',
        suffix='',
        bar_length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    # https://gist.github.com/aubricus/f91fb55dc6ba5557fbab06119420dd6a
    percents = "{0:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    fill = BLOCK * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write('\r%s |%s| %s%s %s' %(prefix, fill, percents, '%', suffix))
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()


def read_input():
    """ Read input from the user"""
    return input(colorize('blue', '> '))


def ask_string(question, default=''):
    """Ask the user to enter something"""
    if default:
        question += " (Default: %s)" % default
    say(colorize('blue', '::'), question)
    answer = read_input()
    return answer if answer else default


def ask_yes_no(question, default=False):
    """Ask the user to answer by yes or no"""
    while True:
        say(colorize('blue', '::'), question, '[Y/n]' if default else  '[y/N]')
        answer = read_input()
        if answer.lower() in ["y", "yes"]:
            return True
        if answer.lower() in ["n", "no"]:
            return False
        if not answer:
            return default
        print("Please answer by 'y' (yes) or 'n' (no) ")


def did_you_mean(msg, user_input, choices):
    """Present user with iterable of choices"""
    if not choices:
        return msg
    result = {
        difflib.SequenceMatcher(
            a=user_input,
            b=choice).ratio(): choice for choice in choices}
    msg += "\nDid you mean: %s?" % result[max(result)]
    return msg

def ask_choice(input_text, choices, *, func_desc=None):
    """Ask the user to choose from a list of choices
    `func_desc` will be called on list item for displaying
    and sorting the list. If not given, will default to
    the identity function

    Will loop until:
        * the user enters a valid index
        * or he hits ctrl-c
        * or he leaves the prompt empty

    In the last two cases, None is returned

    """
    if func_desc is None:
        func_desc = lambda x: x
    say(colorize('blue', '::'), input_text)
    choices.sort(key=func_desc)
    for i, choice in enumerate(choices, start=1):
        choice_desc = func_desc(choice)
        print("  ", COLORS['blue'], "%i" % i, COLORS['reset'], choice_desc)
    keep_asking = True
    res = None
    while keep_asking:
        try:
            answer = read_input()
        except KeyboardInterrupt:
            return None
        if not answer:
            return None
        try:
            index = int(answer)
        except ValueError:
            print("Please enter a valid number")
            continue
        if index not in range(1, len(choices) + 1):
            print(index, "is out of range")
            continue
        res = choices[index - 1]
        keep_asking = False

    return res


def example():
    """This is the example provided by Dimitri Merejkowsky.
    """
    say1("Important info")
    say2("Secondary info")
    say3("This is", colorize('red', 'red'))
    say3("this is", colorize('bold', 'bold'))
    list_of_things = ["foo", "bar", "baz"]
    for j, thing in enumerate(list_of_things):
        countdown(j, len(list_of_things), thing)
    progress_bar(5, 20)
    progress_bar(10, 20)
    progress_bar(20, 20)
    print("\n", CHECK, "all done")
    fruits = ["apple", "orange", "banana"]
    answer = ask_choice("Choose a fruit", fruits)
    print("You chose:", answer)

if __name__ == "__main__":
    example()
