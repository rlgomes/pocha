"""
pocha test discovery module responsible for creating a dictionary containing the
testing hierarchy as represented by the underlying tests.

"""
import os
import imp

from collections import OrderedDict

from pocha import common


def __load_modules(path):
    modules = []

    if os.path.isfile(path) and path.endswith('.py'):
        modules.append(path)

    elif os.path.isdir(path):
        # we do recursively attempt to find tests in a directory that contains
        # the pocha.ignore file in it
        if os.path.exists(os.path.join(path, 'pocha.ignore')):
            return modules

        for filename in os.listdir(path):
            modules += __load_modules(os.path.join(path, filename))

    return modules

class FalseyDict(dict):

    def __init__(self, dictionary):
        self.dict = dictionary

    def __getitem__(self, key):

        if key in self.dict.keys():
            return self.dict[key]

        else:
            # by returning False the evaluation can happen for tags that
            # are not defined
            return False


def filter_tests(tests, expression):
    filtered_tests = tests.copy()

    for (key, thing) in filtered_tests.items():
        if thing.only:
            return OrderedDict({
                thing.name: thing
            })

        if expression is None:
            continue

        if thing.type == 'test':
            global_tags = FalseyDict(thing.tags)

            if not eval(expression, global_tags):
                del filtered_tests[key]

        elif thing.type == 'suite':
            thing.tests = filter_tests(thing.tests, expression)

            if len(thing.tests) == 0:
                del filtered_tests[key]

    return filtered_tests


def search(path, expression):
    modules = __load_modules(path)

    # load each module and then we'll have a complete list of the tests
    # to run
    for module in modules:
        imp.load_source('foo', module)
    
    return filter_tests(common.TESTS, expression)
