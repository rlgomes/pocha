# coding: utf-8

import sh

import test.util

from robber import expect

from pocha import describe, it


@describe('only tests')
def pocha_cli():

    @it('can run a single @it with only flag')
    def _():
        cmd = sh.python('pocha/cli.py',
                        'test/input/only_its.py',
                        _tty_out=False)
        stdout = cmd.stdout.decode('utf-8')
        expect(stdout).to.match(u'''
  ✓ third it

  1 passing \(\d+ms\)

''')

    @it('can not override an only @it with a filter')
    def _():
        cmd = sh.python('pocha/cli.py',
                        'test/input/only_its.py',
                        '--filter', 'first',
                        _tty_out=False)
        stdout = cmd.stdout.decode('utf-8')
        expect(stdout).to.match(u'''
  ✓ third it

  1 passing \(\d+ms\)

''')

    @it('can run a single @describe with only flag')
    def _():
        cmd = sh.python('pocha/cli.py',
                        'test/input/only_describe.py',
                        _tty_out=False)
        stdout = cmd.stdout.decode('utf-8')
        expect(stdout).to.match(u'''
  second describe
    ✓ third it
    ✓ fourth it

  2 passing \(\d+ms\)

''')
