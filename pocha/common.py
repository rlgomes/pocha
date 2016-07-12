"""
pocha decorator module
"""

from collections import OrderedDict
from functools import wraps

from pocha.util import EasyDict

TESTS = OrderedDict()

SUITE_STACK = [EasyDict({
    'name': '__default__',
    'type': 'suite',
    'tests': OrderedDict(),
    'skip': False,
    'only': False,
    'tags': {},

    'before': [],
    'after': [],
    'before_each': [],
    'after_each': []
})]

# __default__ suite is created but never recorded as a suite
TESTS['__default__'] = SUITE_STACK[0]


def handle_tags(tags):

    if tags is None:
        return {}

    if isinstance(tags, dict):
        return tags

    if isinstance(tags, list):
        return {key: True for key in tags}

    raise Exception('unexpected tags type %s' % type(tags))


class describe(object):
    """
    decorator used to define a test suite by name

    params:
        name - name of the test suite
        tags - list of tags used to tag this test suite. You can provide a list
               of tags ie `tags=['foo', 'bar']` or you can provide a dictionary
               of tags ie `tags={ 'foo': 1, 'bar': True }`
        only - when set to True, pocha will only run this test or suite and skip
               all others without producing a skipped test result
        skip - when set to True, pocha will skip this test and produce a skipped
               test result
    """

    def __init__(self,
                 name,
                 only=False,
                 skip=False,
                 tags=None):
        self.name = name
        self.only = only
        self.skip = skip
        self.tags = handle_tags(tags)

    def __call__(self, func):
        suite = EasyDict({
            'name': self.name,
            'type': 'suite',
            'tests': OrderedDict(),
            'only': self.only,
            'skip': self.skip,
            'tags': self.tags,

            'before': [],
            'after': [],
            'before_each': [],
            'after_each': []
        })
        SUITE_STACK[-1].tests[self.name] = suite
        SUITE_STACK.append(suite)

        # run the underlying describe function which in turns executes any other
        # @describe and @it decorators
        func()
        SUITE_STACK.pop()
        return func


class it(object):
    """
    decorator used to define a test case by name

    params:
        name - name of the test case
        tags - list of tags used to tag this test. You can provide a list of
               tags ie `tags=['foo', 'bar']` or you can provide a dictionary
               of tags ie `tags={ 'foo': 1, 'bar': True }`
        only - when set to True, pocha will only run this test or suite and skip
               all others without producing a skipped test result
        skip - when set to True, pocha will skip this test and produce a skipped
               test result
    """

    def __init__(self,
                 name,
                 only=False,
                 skip=False,
                 tags=None):
        self.name = name
        self.only = only
        self.skip = skip
        self.tags = handle_tags(tags)

    def __call__(self, func):
        current_stack = SUITE_STACK[-1]
        tags = current_stack.tags.copy()
        tags.update(self.tags)
        current_stack.tests[self.name] = EasyDict({
            'name': self.name,
            'type': 'test',
            'func': func,
            'tags': tags,
            'only': self.only,
            'skip': self.skip or current_stack.skip
        })
        func.name = self.name
        return func


def before(func):
    """
    decorator used to define a function to execute before the current suite is
    executed
    """
    current_stack = SUITE_STACK[-1]
    current_stack.before.append(func)
    return func


def after(func):
    """
    decorator used to define a function to execute after the current suite is
    executed
    """
    current_stack = SUITE_STACK[-1]
    current_stack.after.append(func)
    return func


def before_each(func):
    """
    decorator used to define a function to execute before each test case
    """
    current_stack = SUITE_STACK[-1]
    current_stack.before_each.append(func)
    return func


def after_each(func):
    """
    decorator used to define a function to execute after each test case
    """
    current_stack = SUITE_STACK[-1]
    current_stack.after_each.append(func)
    return func

# aliases
beforeEach = before_each
afterEach = after_each
