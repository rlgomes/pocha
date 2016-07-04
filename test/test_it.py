# coding: utf-8

import sh

from robber import expect

from pocha import describe, it
from test import util
util.init()

@describe('@it tests')
def pocha_cli():

    @describe('spec reporter', tags=['spec'])
    def spec():
        @it('can run a test with a single passing @it')
        def _():
            cmd = sh.python('pocha/cli.py',
                            'test/input/single_passing_it.py',
                            _tty_out=False)
            expect(cmd.stdout).to.match('''
  ✓ can run a single passing it

  1 passing \(\d+ms\)

''')


        @it('can run a test with a single failing @it')
        def _():
            cmd = sh.python('pocha/cli.py',
                            'test/input/single_failing_it.py',
                            _ok_code=[1],
                            _tty_out=False)
            expect(cmd.stdout).to.match('''
  1\) can run a single failing it

  0 passing \(\d+ms\)
  1 failing

  1\) can run a single failing it:
     Exception: failing on purpose
     File "test/input/single_failing_it.py", line 6, in failing
       raise Exception\('failing on purpose'\)

''')

        @it('can run a test with mixed @its')
        def _():
            cmd = sh.python('pocha/cli.py',
                            'test/input/mixed_its.py',
                            _ok_code=[1],
                            _tty_out=False)
            expect(cmd.stdout).to.match('''
  ✓ can run a passing it
  1\) can run a failing it
  ✓ can run another passing it

  2 passing \(\d+ms\)
  1 failing

  1\) can run a failing it:
     Exception: failing on purpose
     File "test/input/mixed_its.py", line 10, in _
       raise Exception\('failing on purpose'\)

''')

    @describe('dot reporter', tags=['dot'])
    def spec():
        @it('can run a test with a single passing @it')
        def _():
            cmd = sh.python('pocha/cli.py',
                            '--reporter', 'dot',
                            'test/input/single_passing_it.py',
                            _tty_out=False)
            expect(cmd.stdout).to.match('''
  .

  1 passing \(\d+ms\)

''')

        @it('can run a test with a single failing @it')
        def _():
            cmd = sh.python('pocha/cli.py',
                            '--reporter', 'dot',
                            'test/input/single_failing_it.py',
                            _ok_code=[1],
                            _tty_out=False)
            expect(cmd.stdout).to.match('''
  .

  0 passing \(\d+ms\)
  1 failing

  1\) can run a single failing it:
     Exception: failing on purpose
     File "test/input/single_failing_it.py", line 6, in failing
       raise Exception\('failing on purpose'\)

''')

        @it('can run a test with mixed @its')
        def _():
            cmd = sh.python('pocha/cli.py',
                            '--reporter', 'dot',
                            'test/input/mixed_its.py',
                            _ok_code=[1],
                            _tty_out=False)
            expect(cmd.stdout).to.match('''
  ...

  2 passing \(\d+ms\)
  1 failing

  1\) can run a failing it:
     Exception: failing on purpose
     File "test/input/mixed_its.py", line 10, in _
       raise Exception\('failing on purpose'\)

''')

        @it('can run dynamically created @its')
        def _():
            cmd = sh.python('pocha/cli.py',
                            '--reporter', 'dot',
                            'test/input/dynamically_created_its.py',
                            _tty_out=False)
            expect(cmd.stdout).to.match('''
  .....

  5 passing \(\d+ms\)

''')

    @describe('xunit reporter', tags=['xunit'])
    def spec():
        @it('can run a test with a single passing @it')
        def _():
            cmd = sh.python('pocha/cli.py',
                            '--reporter', 'xunit',
                            'test/input/single_passing_it.py',
                            _tty_out=False)

            expect(cmd.stdout).to.have.xpath('./testsuite[' +
                                             '@name="Pocha Tests" and ' +
                                             '@tests="1" and ' +
                                             '@errors="0" and ' +
                                             '@failures="0" and ' +
                                             '@skip="0"]')

            expect(cmd.stdout).to.have.xpath('./testsuite/testcase[' +
                                             '@name="can run a single passing it" and ' +
                                             '@classname="" and ' +
                                             '@time="0.000"]')


        @it('can run a test with a single failing @it')
        def _():
            cmd = sh.python('pocha/cli.py',
                            '--reporter', 'xunit',
                            'test/input/single_failing_it.py',
                            _ok_code=[1],
                            _tty_out=False)

            expect(cmd.stdout).to.have.xpath('./testsuite[' +
                                             '@name="Pocha Tests" and ' +
                                             '@tests="1" and ' +
                                             '@errors="0" and ' +
                                             '@failures="1" and ' +
                                             '@skip="0"]')

            # XXX: should find a way to validate the stacktrace
            expect(cmd.stdout).to.have.xpath('./testsuite/testcase[' +
                                             '@name="can run a single failing it" and ' +
                                             '@classname=""]/error')

        @it('can run a test with mixed @its')
        def _():
            cmd = sh.python('pocha/cli.py',
                            '--reporter', 'xunit',
                            'test/input/mixed_its.py',
                            _ok_code=[1],
                            _tty_out=False)
            expect(cmd.stdout).to.have.xpath('./testsuite[' +
                                             '@name="Pocha Tests" and ' +
                                             '@tests="3" and ' +
                                             '@errors="0" and ' +
                                             '@failures="1" and ' +
                                             '@skip="0"]')

            expect(cmd.stdout).to.have.xpath('./testsuite/testcase[' +
                                             '@name="can run a passing it" and ' +
                                             '@classname=""]')

            # XXX: should find a way to validate the stacktrace
            expect(cmd.stdout).to.have.xpath('./testsuite/testcase[' +
                                             '@name="can runa a failing it" and ' +
                                             '@classname=""]/error')

            expect(cmd.stdout).to.have.xpath('./testsuite/testcase[' +
                                             '@name="can run another passing it" and ' +
                                             '@classname=""]')


        @it('can run dynamically created @its')
        def _():
            cmd = sh.python('pocha/cli.py',
                            '--reporter', 'xunit',
                            'test/input/dynamically_created_its.py',
                            _tty_out=False)

            expect(cmd.stdout).to.have.xpath('./testsuite[' +
                                             '@name="Pocha Tests" and ' +
                                             '@tests="5" and ' +
                                             '@errors="0" and ' +
                                             '@failures="0" and ' +
                                             '@skip="0"]')

            for index in range(1, 6):
                expect(cmd.stdout).to.have.xpath('./testsuite/testcase[' +
                                                 '@name="passing it #%d" and ' % index+
                                                 '@classname=""]')
