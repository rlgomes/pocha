"""
pocha utility module
"""

import traceback
import os


from colored import fg, attr

_fail = fg('red')
_reset = attr('reset')


class EasyDict(dict):

    def __init__(self, dictionary):
        for (key, value) in dictionary.items():
            self.__setitem__(key, value)

    def __getattr__(self, key):
        if key in self:
            return self[key]


def print_failures(failures, stdout):
    """
    pretty print failures in a common way to most reporters
    """
    for index in range(0, len(failures)):
        (name, exc_info) = failures[index]
        # extract the traceback and drop everything after the first part
        # which is in the pocha/runner.py file
        parts = traceback.extract_tb(exc_info[2])[1:]

        # File "../../", line 13, in _
        tb_lines = '\n'.join([
            '  File "%s", line %d, in %s\n    %s\n' %
            (os.path.relpath(path), line, method, exception)
            for path, line, method, exception in parts
        ])

        tb_lines = ['   %s' % line
                    for line in tb_lines.split('\n') if line.strip() != '']
        stdout.write('  %d) %s:\n' % (index + 1, name))
        exception_name = exc_info[1].__class__.__name__
        if stdout.isatty():
            stdout.write('     %s%s: %s%s\n' %
                         (_fail, exception_name, exc_info[1], _reset))

        else:
            stdout.write('     %s: %s\n' % (exception_name, exc_info[1]))
        stdout.write('\n'.join(tb_lines))
        stdout.write('\n\n')
