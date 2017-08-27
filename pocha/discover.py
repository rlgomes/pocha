"""
pocha test discovery module responsible for creating a dictionary containing the
testing hierarchy as represented by the underlying tests.

"""
import os
import imp
import sys

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
    filtered_tests = OrderedDict()

    for (key, thing) in tests.items():
        if thing.only:
            return OrderedDict({
                thing.name: thing
            })

        if thing.type == 'test':
            if expression is None:
                filtered_tests[key] = thing
                continue

            global_tags = FalseyDict(thing.tags)

            if eval(expression, global_tags):
                filtered_tests[key] = thing

        elif thing.type == 'suite':
            thing.tests = filter_tests(thing.tests, expression)
                
            if len(thing.tests) != 0:
                filtered_tests[key] = thing

    return filtered_tests


def search(path, expression):
    modules = __load_modules(path)

    # load each module and then we'll have a complete list of the tests
    # to run
    def get_module_package_root_path_and_module_name(module_full_path):
        module_full_path = module_full_path.replace('/', os.path.sep).replace('\\', os.path.sep)
        path_list = module_full_path.split(os.path.sep)
        if path_list[-1].endswith('.py'):
            path_list[-1] = path_list[-1][:-3]
        module_name_list = []
        module_dir = os.path.sep.join(path_list[:-1])
        while True:
            if len(path_list) > 0:
                module_name_list.insert(0, path_list.pop())
                package_init_file_path = os.path.sep.join(path_list + ['__init__.py'])
                if os.path.isfile(package_init_file_path):
                    module_dir = os.path.sep.join(path_list[:-1])
                else:
                    break
        # print '==: ', module_dir, module_name_list
        return module_dir, '.'.join(module_name_list)

    for module in modules:
        cur_dir = os.getcwdu()
        module = module.replace('/', os.path.sep).replace('\\', os.path.sep)
        abs_path = os.path.abspath(os.path.join(cur_dir, module)).replace('/', os.path.sep).replace('\\', os.path.sep)
        if not module.endswith('.py'):
            continue
        # print get_module_package_root_path_and_module_name(abs_path)
        module_dir, module_name = get_module_package_root_path_and_module_name(abs_path)
        try:
            if module in sys.modules:
                del sys.modules[module] 
            sys.path.insert(0, module_dir)
            __import__(module_name)
        except ImportError as e:
            raise e
        except Exception as e:
            raise e
        finally:
            sys.path.remove(module_dir)

    # print common.TESTS
    return filter_tests(common.TESTS, expression)