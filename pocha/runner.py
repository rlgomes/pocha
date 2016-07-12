"""
pocha runner module
"""

import sys

from pocha.util import EasyDict

def run_tests(tests, reporter):
    reporter.beforeTests(sys.stdout)
    hadfailures = __run_tests(None, tests, reporter, sys.stdout)
    reporter.afterTests(sys.stdout)
    return hadfailures


def __run_tests(suite, tests, reporter, stdout):
    hadfailures = False

    for (key, thing) in tests.items():
        if thing.type == 'test':
            try:
                reporter.beforeTest(stdout, EasyDict({
                    'name': thing.func.name
                }))

                try:
                    for before_each in suite.before_each:
                        before_each()

                except Exception as exception:
                    reporter.afterTest(stdout, EasyDict({
                        'name': '"before each" hook for "%s"' % thing.func.name,
                        'status': 'fail',
                        'exc_info': sys.exc_info()
                    }))
                    continue

                if not thing.skip:
                    thing.func()

                    reporter.afterTest(stdout, EasyDict({
                        'name': thing.func.name,
                        'status': 'pass'
                    }))

                else:
                    reporter.afterTest(stdout, EasyDict({
                        'name': thing.func.name,
                        'status': 'skip'
                    }))

                try:
                    for after_each in suite.after_each:
                        after_each()
                except Exception as exception:
                    reporter.afterTest(stdout, EasyDict({
                        'name': '"after each" hook for "%s"' % thing.func.name,
                        'status': 'fail',
                        'exc_info': sys.exc_info()
                    }))

            except Exception as exception:
                reporter.afterTest(stdout, EasyDict({
                    'name': thing.func.name,
                    'status': 'fail',
                    'exc_info': sys.exc_info()
                }))
                hadfailures = True

        elif thing.type == 'suite':
            beforeHookFailed = False

            if thing.name != '__default__':
                reporter.beforeSuite(stdout, EasyDict({
                    'name': key
                }))

            try:
                for before in thing.before:
                    before()
            except Exception as exception:
                reporter.afterTest(stdout, EasyDict({
                    'name': '"before all" hook',
                    'status': 'fail',
                    'exc_info': sys.exc_info()
                }))
                return True

            hadfailures |= __run_tests(thing, thing.tests, reporter, stdout)

            if thing.name != '__default__':
                reporter.afterSuite(stdout, EasyDict({
                    'name': key
                }))

            try:
                for after in thing.after:
                    after()
            except Exception as exception:
                reporter.afterTest(stdout, EasyDict({
                    'name': '"after all" hook',
                    'status': 'fail',
                    'exc_info': sys.exc_info()
                }))
                return True

    return hadfailures
