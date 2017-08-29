# coding: utf-8
"""
spec pocha reporter
"""

import time

from colored import fg, attr

from pocha.reporters.base import Reporter
from pocha.util import print_failures

_pass = fg('green')
_fail = fg('red')
_skip = fg('cyan')
_dim = attr('dim')
_reset = attr('reset')

class SpecReporter(Reporter):

    def __init__(self):
        self.start = None
        self.depth = 0
        self.suites = 0
        self.passing = 0
        self.failing = 0
        self.skipping = 0
        self.failures = []

    def beforeTests(self, stdout):
        self.start = time.time()*1000
        stdout.write('\n')

    def beforeSuite(self, stdout, suite):
        if self.depth == 0 and self.suites != 0:
            stdout.write('\n')

        self.depth += 2
        self.suites += 1
        stdout.write('%s%s\n' % (' ' * self.depth, suite.name))

    def beforeTest(self, stdout, test):
        pass

    def afterTests(self, stdout):
        duration = time.time()*1000 - self.start
        stdout.write('\n')
        if stdout.isatty():
            stdout.write('  %s%d passing%s %s(%dms)%s\n' %
                         (_pass, self.passing, _reset, _dim, duration, _reset))

        else:
            stdout.write('  %d passing (%dms)\n' % (self.passing, duration))

        if self.skipping > 0:
            if stdout.isatty():
                stdout.write('  %s%d pending%s\n' % (_skip, self.skipping, _reset))

            else:
                stdout.write('  %d pending\n' % self.skipping)

        if self.failing > 0:
            if stdout.isatty():
                stdout.write('  %s%d failing%s\n' % (_fail, self.failing, _reset))

            else:
                stdout.write('  %d failing\n' % self.failing)

            stdout.write('\n')
            # list the tests in order with their associated stacktrace
            print_failures(self.failures, stdout)

        stdout.write('\n')

    def afterSuite(self, stdout, suite):
        self.depth -= 2

    def afterTest(self, stdout, test):
        padding = ' ' * (self.depth + 2)

        if test.status == 'pass':
            if stdout.isatty():
                stdout.write('%s%s✓%s %s%s%s\n' % (padding, _pass, _reset, _dim, test.name, _reset))

            else:
                stdout.write('%s✓ %s\n' % (padding, test.name))

            self.passing += 1

        elif test.status == 'fail':
            which = len(self.failures) + 1

            if stdout.isatty():
                stdout.write('%s%s%d) %s%s%s\n' % (padding, _fail, which, _dim, test.name, _reset))

            else:
                stdout.write('%s%d) %s\n' % (padding, which, test.name))

            self.failures.append((test.name, test.exc_info))
            self.failing += 1

        elif test.status == 'skip':
            if stdout.isatty():
                stdout.write('%s%s- %s%s\n' % (padding, _skip, test.name, _reset))

            else:
                stdout.write('%s- %s\n' % (padding, test.name))

            self.skipping += 1

