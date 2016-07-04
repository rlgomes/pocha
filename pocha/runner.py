"""
pocha runner module
"""

import sys

from pocha.util import EasyDict

def run_tests(tests, reporter):
    reporter.beforeTests(sys.stdout)
    hadfailures = __run_tests(tests, reporter, sys.stdout)
    reporter.afterTests(sys.stdout)
    return hadfailures


def __run_tests(tests, reporter, stdout):
    hadfailures = False

    for (key, thing) in tests.items():
        if thing.type == 'test':
            try:
                reporter.beforeTest(stdout, EasyDict({
                    'name': thing.func.name
                }))

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

            except Exception as exception:
                reporter.afterTest(stdout, EasyDict({
                    'name': thing.func.name,
                    'status': 'fail',
                    'exc_info': sys.exc_info()
                }))
                hadfailures = True

        elif thing.type == 'suite':
            reporter.beforeSuite(stdout, EasyDict({
                'name': key
            }))

            hadfailures |= __run_tests(thing.tests, reporter, stdout)

            reporter.afterSuite(stdout, EasyDict({
                'name': key
            }))

        else:
            raise Exception('wtf')

    return hadfailures
