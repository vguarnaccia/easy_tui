# -*- coding: utf-8 -*-
"""This module provides helper functions for pretty, colorized TUIs.
"""
import datetime
import difflib
import io
import os
import sys
import traceback

import colorama
import unidecode

colorama.init()
# Global variable to store configuration

CONFIG = {
    "verbose": os.environ.get("VERBOSE"),
    "quiet": False,
    "timestamp": False,
}


def _color(code, modifier=None):
    code = '\033[%d' % code
    code += ';%dm' % modifier if modifier is not None else 'm'
    return code

COLORS = {
    # Styles
    'reset': _color(0),
    'bold': _color(1),
    'faint': _color(2),
    'standout': _color(3),
    'underline': _color(4),
    'blink': _color(5),
    'overline': _color(6),

    # Major colors
    'black': _color(30),
    'darkred': _color(31),
    'darkgreen': _color(32),
    'brown': _color(33),
    'darkblue': _color(34),
    'purple': _color(35),
    'teal': _color(36),
    'lightgray': _color(37),

    # Minor colors
    'darkgray': _color(30, 1),
    'red': _color(31, 1),
    'green': _color(32, 1),
    'yellow': _color(33, 1),
    'blue': _color(34, 1),
    'fuchsia': _color(35, 1),
    'turquoise': _color(36, 1),
    'white': _color(37, 1),
}

# Other nice-to-have characters:

def colorize(colors, phrase):
    """Wrap a string in a color"""
    as_string = ' '.join(COLORS[color] for color in colors.split())
    return COLORS['reset'] + as_string + phrase + COLORS['reset']

def _characters(color, as_unicode, as_ascii):
    as_string = as_unicode if os.name != 'nt' else as_ascii
    return colorize(color, as_string)


ELLIPSIS = _characters('reset', "…", "...")
CHECK = _characters('green', "✓", "ok")
CROSS = _characters('red', "❌", "ko")

# ARROW =
# THUS =

def process_tokens(tokens, *, end="\n", sep=" "):
    """ Returns two strings from a list of tokens.
    One containing ASCII escape codes, the other
    only the 'normal' characters

    """
    with_color = _process_tokens(tokens, end=end, sep=sep, color=True)
    without_color = _process_tokens(tokens, end=end, sep=sep, color=False)
    return (with_color, without_color)


def _process_tokens(tokens, *, end="\n", sep=" ", color=True):
    res = ""

    if CONFIG["timestamp"]:
        now = datetime.datetime.now()
        res += now.strftime("[%Y-%m-%d %H:%M:%S] ")

    for i, token in enumerate(tokens):
        res += str(token)
        if i != len(tokens) - 1:
            res += sep
    res += end
    if color:
        res += COLORS['reset']
    return res


def message(*tokens, **kwargs):
    """ Helper method for error, warning, info, debug

    """
    sep = kwargs.get("sep", " ")
    end = kwargs.get("end", "\n")
    fileobj = kwargs.get("fileobj") or sys.stdout
    with_color, without_color = process_tokens(tokens, end=end, sep=sep)
    # sys.isatty() is False on mintty, so
    # let there be colors by default. (when running on windows,
    # people can use --color=never)
    # Note that on Windows, when run from cmd.exe,
    # console.init() does the right thing if sys.stdout is redirected
    to_write = with_color if fileobj.isatty() or os.name == "nt" else without_color
    try:
        fileobj.write(to_write)
    except UnicodeEncodeError:
        # Maybe the file descritor does not support the full Unicode
        # set, like stdout on Windows.
        # Use the unidecode library
        # to make sure we only have ascii, while still keeping
        # as much info as we can
        fileobj.write(unidecode.unidecode(to_write))
    fileobj.flush()


def fatal(*tokens, **kwargs):
    """ Print an error message and calls sys.exit """
    error(*tokens, **kwargs)
    sys.exit(1)


def error(*tokens, **kwargs):
    """ Print an error message """
    tokens = colorize('bold read', '[ERROR]:') + list(tokens)
    kwargs["fileobj"] = sys.stderr
    message(*tokens, **kwargs)


def warning(*tokens, **kwargs):
    """ Print a warning message """
    tokens = colorize('brown', '[WARN ]:') + list(tokens)
    kwargs["fileobj"] = sys.stderr
    message(*tokens, **kwargs)


def info(*tokens, **kwargs):
    """ Print an informative message """
    if CONFIG["quiet"]:
        return
    message(*tokens, **kwargs)


def info_1(*tokens, **kwargs):
    """ Print an important informative message """
    sys.stdout.write(colorize('bold blue', '::'))
    info(*tokens, **kwargs)


def info_2(*tokens, **kwargs):
    """ Print an not so important informative message """
    sys.stdout.write(colorize('bold blue', '=>'))
    info(*tokens, **kwargs)


def info_3(*tokens, **kwargs):
    """ Print an even less important informative message """
    sys.stdout.write(colorize('bold blue', '*'))
    info(*tokens, **kwargs)


def info_count(current, total, *rest, **kwargs):
    """ Same as info, but displays a nice counter
    color will be reset
    >>> info_count(0, 4)
    * (1/4)
    >>> info_count(5, 12)
    * ( 5/12)
    >>> info_count(5, 10)
    * ( 5/10)

    """
    num_digits = len(str(total))  # lame, I know
    counter_format = "(%{}d/%d)".format(num_digits)
    counter_str = counter_format % (current + 1, total)
    info(colorize('green', "*"), counter_str, COLORS['reset'], *rest, **kwargs)


def info_progress(
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
    fill = '█' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write('\r%s |%s| %s%s %s' %(prefix, fill, percents, '%', suffix))
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()


def debug(*tokens, **kwargs):
    """ Print a debug message """
    if CONFIG["verbose"]:
        tokens = colorize('blue', '[DEBUG]:') + list(tokens)
        message(*tokens, **kwargs)


def indent_iterable(elems, num=2):
    """Indent an iterable."""
    return [" " * num + l for l in elems]


def indent(text, num=2):
    """Indent a piece of text."""
    lines = text.splitlines()
    return '\n'.join(indent_iterable(lines, num=num))


def tabs(num):
    """ Compute a blank tab """
    return "  " * num


def message_for_exception(exception, msg):
    """ Returns a tuple suitable for ui.error()
    from the given exception.
    (Traceback will be part of the message, after
    the ``message`` argument)

    Useful when the exception occurs in an other thread
    than the main one.

    """
    trace = sys.exc_info()[2]
    buffer = io.StringIO()
    traceback.print_tb(trace, file=io)
    return (COLORS['red'], msg + "\n",
            exception.__class__.__name__,
            str(exception), "\n",
            COLORS['reset'],
            buffer.getvalue())


def read_input():
    """ Read input from the user
    """
    info(colorize('green', '> '), end="")
    return input()


def ask_string(question, default=None):
    """Ask the user to enter something.

    Returns what the user entered
    """
    if default:
        question += " (Default: %s)" % default
    info(COLORS['green'], "::", COLORS['reset'], question)
    try:
        answer = read_input()
    except KeyboardInterrupt:
        return default
    if not answer:
        return default
    return answer


def ask_choice(input_text, choices):
    """Ask the user to choose from a list of choices

    """
    info(COLORS['green'], "::", COLORS['reset'], input_text)
    for i, choice in enumerate(choices, start=1):
        if i == 1:
            choice += " \t(default)"
        info("  ", COLORS['blue'], "%i" % i, COLORS['reset'], choice)
    keep_asking = True
    res = None
    while keep_asking:
        try:
            answer = read_input()
        except KeyboardInterrupt:
            break
        if not answer:
            return choices[0]
        try:
            index = int(answer)
        except ValueError:
            info("Please enter number")
            continue
        if index not in range(1, len(choices) + 1):
            info(index, "is out of range")
            continue
        res = choices[index - 1]
        keep_asking = False

    return res


def ask_yes_no(question, default=False):
    """Ask the user to answer by yes or no"""
    while True:
        if default:
            info(COLORS['green'], "::", COLORS['reset'], question, "(Y/n)")
        else:
            info(COLORS['green'], "::", COLORS['reset'], question, "(y/N)")
        answer = read_input()
        if answer.lower() in ["y", "yes"]:
            return True
        if answer.lower() in ["n", "no"]:
            return False
        if not answer:
            return default
        warning("Please answer by 'y' (yes) or 'n' (no) ")


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

def example():
    """This is the example provided by Dimitri Merejkowsky.
    """
    info_1("Important info")
    info_2("Secondary info")
    info("This is", COLORS['red'], "red")
    info("this is", COLORS['bold'], "bold")
    list_of_things = ["foo", "bar", "baz"]
    for j, thing in enumerate(list_of_things):
        info_count(j, len(list_of_things), thing)
    info_progress(5, 20)
    info_progress(10, 20)
    info_progress(20, 20)
    info("\n", CHECK, "all done")
    fruits = ["apple", "orange", "banana"]
    answer = ask_choice("Choose a fruit", fruits)
    info("You chose:", answer)

if __name__ == "__main__":
    example()
