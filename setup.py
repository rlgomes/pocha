"""
setup.py
"""
import os

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

class PochaTestCommand(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        from pocha.cli import cli
        cli()

def load(filename):
    with open(filename, 'r') as input_file:
        return input_file.read().split('\n')

setup(
    name='pocha',
    version='0.10.0',
    author='Rodney Gomes',
    author_email='rodneygomes@gmail.com',
    url='',

    install_requires=load('requirements.txt'),
    tests_require=load('requirements-dev.txt'),

    cmdclass={'test': PochaTestCommand},
    test_suite='test',
    keywords=[''],
    py_modules=['pocha'],
    packages=find_packages(exclude=['tests']),


    entry_points={
        'console_scripts': [
            'pocha=pocha.cli:cli'
        ]
    },

    license='Apache 2.0 License',
    description='',
    long_description='',
)
