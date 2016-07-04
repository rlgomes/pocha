# coding: utf-8

import sh

from robber import expect

from pocha import describe, it
from test import util
util.init()


@describe('skip tests')
def pocha_cli():

    @describe('spec reporter', tags=['spec'])
    def _():

        @it('can run handle skips with @its')
        def _():
            cmd = sh.python('pocha/cli.py',
                            'test/input/skip_its.py',
                            _tty_out=False)
            expect(cmd.stdout).to.match('''
  - first it
  ✓ second it
  - third it

  1 passing \(\d+ms\)
  2 pending
''')

    @describe('dot reporter', tags=['spec'])
    def _():

        @it('can run handle skips with @its')
        def _():
            cmd = sh.python('pocha/cli.py',
                            'test/input/skip_its.py',
                            '--reporter', 'dot',
                            _tty_out=False)
            expect(cmd.stdout).to.match('''
  ...

  1 passing \(\d+ms\)
  2 pending
''')

    @describe('xunit reporter', tags=['spec'])
    def _():

        @it('can run handle skips with @its')
        def _():
            cmd = sh.python('pocha/cli.py',
                            'test/input/skip_its.py',
                            '--reporter', 'xunit',
                            _tty_out=False)

            expect(cmd.stdout).to.have.xpath('./testsuite[' +
                                             '@name="Pocha Tests" and ' +
                                             '@tests="3" and ' +
                                             '@errors="0" and ' +
                                             '@failures="0" and ' +
                                             '@skip="2"]')

            expect(cmd.stdout).to.have.xpath('./testsuite/testcase[' +
                                             '@name="first it" and ' +
                                             '@classname="" and ' +
                                             '@time="0.000"]/skipped')

            expect(cmd.stdout).to.have.xpath('./testsuite/testcase[' +
                                             '@name="second it" and ' +
                                             '@classname="" and ' +
                                             '@time="0.000"]')

            expect(cmd.stdout).to.have.xpath('./testsuite/testcase[' +
                                             '@name="third it" and ' +
                                             '@classname="" and ' +
                                             '@time="0.000"]/skipped')
