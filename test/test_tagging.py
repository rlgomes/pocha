# coding: utf-8

import sh

from robber import expect

from pocha import describe, it
from test import util
util.init()


@describe('filtering tagged tests')
def pocha_cli():

    @it('can run an it filtered on a unique tag')
    def _():
        cmd = sh.python('pocha/cli.py',
                        'test/input/tagged_its.py',
                        '--filter', 'third',
                        _tty_out=False)
        stdout = cmd.stdout.decode('utf-8')
        expect(stdout).to.match(u'''
  ✓ third it

  1 passing \(\d+ms\)

''')

    @it('can run a set of its filtered with the same tag')
    def _():
        cmd = sh.python('pocha/cli.py',
                        'test/input/tagged_its.py',
                        '--filter', 'edge',
                        _tty_out=False)
        stdout = cmd.stdout.decode('utf-8')
        expect(stdout).to.match(u'''
  ✓ first it
  ✓ third it

  2 passing \(\d+ms\)

''')

    @it('can run with `or` expression')
    def _():
        cmd = sh.python('pocha/cli.py',
                        'test/input/tagged_its.py',
                        '--filter', 'first or second',
                        _tty_out=False)
        stdout = cmd.stdout.decode('utf-8')
        expect(stdout).to.match(u'''
  ✓ first it
  ✓ second it

  2 passing \(\d+ms\)

''')

    @it('can run with `and` expressions')
    def _():
        cmd = sh.python('pocha/cli.py',
                        'test/input/tagged_its.py',
                        '--filter', 'first and edge',
                        _tty_out=False)
        stdout = cmd.stdout.decode('utf-8')
        expect(stdout).to.match(u'''
  ✓ first it

  1 passing \(\d+ms\)

''')

    @it('can run with `not` expression')
    def _():
        cmd = sh.python('pocha/cli.py',
                        'test/input/tagged_its.py',
                        '--filter', 'not middle',
                        _tty_out=False)
        stdout = cmd.stdout.decode('utf-8')
        expect(stdout).to.match(u'''
  ✓ first it
  ✓ third it

  2 passing \(\d+ms\)

''')
