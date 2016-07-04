# coding: utf-8

import sh

from robber import expect
from pocha import describe, it

from test import util
util.init()


@describe('@describe tests')
def pocha_cli():

    @describe('spec reporter', tags=['spec'])
    def spec():
        @it('can run an empty @describe')
        def _():
            cmd = sh.python('pocha/cli.py',
                            'test/input/describe_with_no_it.py',
                            _ok_code=[0],
                            _tty_out=False)
            expect(cmd.stdout).to.match('''
  an empty describe

  0 passing \(\d+ms\)

''')

        @it('can run a @describe with a single passing @it')
        def _():
            cmd = sh.python('pocha/cli.py',
                            'test/input/describe_with_single_passing_it.py',
                            _ok_code=[0],
                            _tty_out=False)
            expect(cmd.stdout).to.match('''
  top level describe
    ✓ can run a single passing it

  1 passing \(\d+ms\)

''')

        @it('can run a @describe with multiple passing @it')
        def _():
            cmd = sh.python('pocha/cli.py',
                            'test/input/describe_with_multiple_passing_it.py',
                            _ok_code=[0],
                            _tty_out=False)
            expect(cmd.stdout).to.match('''
  top level describe
    ✓ can run a passing it
    ✓ can run another passing it

  2 passing \(\d+ms\)

''')


        @it('can run a @describe with a single failing @it')
        def _():
            cmd = sh.python('pocha/cli.py',
                            'test/input/describe_with_single_failing_it.py',
                            _ok_code=[1],
                            _tty_out=False)
            expect(cmd.stdout).to.match('''
  top level describe
    1\) can run a single failing it

  0 passing \(\d+ms\)
  1 failing

  1\) can run a single failing it:
     Exception: failing on purpose
     File "test/input/describe_with_single_failing_it.py", line 9, in failing_it
       raise Exception\('failing on purpose'\)

''')

        @it('can run a @describe with multiple failing @it')
        def _():
            cmd = sh.python('pocha/cli.py',
                            'test/input/describe_with_multiple_failing_it.py',
                            _ok_code=[1],
                            _tty_out=False)
            expect(cmd.stdout).to.match('''
  top level describe
    1\) can run a failing it
    2\) can run another failing it

  0 passing \(\d+ms\)
  2 failing

  1\) can run a failing it:
     Exception: failing on purpose
     File "test/input/describe_with_multiple_failing_it.py", line 9, in _
       raise Exception\('failing on purpose'\)

  2\) can run another failing it:
     Exception: failing on purpose again
     File "test/input/describe_with_multiple_failing_it.py", line 13, in _
       raise Exception\('failing on purpose again'\)

''')

    @describe('dot reporter', tags=['dot'])
    def spec():
        @it('can run an empty @describe')
        def _():
            cmd = sh.python('pocha/cli.py',
                            '--reporter', 'dot',
                            'test/input/describe_with_no_it.py',
                            _ok_code=[0],
                            _tty_out=False)
            expect(cmd.stdout).to.match('''
  0 passing \(\d+ms\)

''')

        @it('can run a @describe with a single passing @it')
        def _():
            cmd = sh.python('pocha/cli.py',
                            '--reporter', 'dot',
                            'test/input/describe_with_single_passing_it.py',
                            _ok_code=[0],
                            _tty_out=False)
            expect(cmd.stdout).to.match('''
  .

  1 passing \(\d+ms\)

''')

        @it('can run a @describe with multiple passing @it')
        def _():
            cmd = sh.python('pocha/cli.py',
                            '--reporter', 'dot',
                            'test/input/describe_with_multiple_passing_it.py',
                            _ok_code=[0],
                            _tty_out=False)
            expect(cmd.stdout).to.match('''
  ..

  2 passing \(\d+ms\)

''')


        @it('can run a @describe with a single failing @it')
        def _():
            cmd = sh.python('pocha/cli.py',
                            '--reporter', 'dot',
                            'test/input/describe_with_single_failing_it.py',
                            _ok_code=[1],
                            _tty_out=False)
            expect(cmd.stdout).to.match('''
  .

  0 passing \(\d+ms\)
  1 failing

  1\) can run a single failing it:
     Exception: failing on purpose
     File "test/input/describe_with_single_failing_it.py", line 9, in failing_it
       raise Exception\('failing on purpose'\)

''')

        @it('can run a @describe with multiple failing @it')
        def _():
            cmd = sh.python('pocha/cli.py',
                            '--reporter', 'dot',
                            'test/input/describe_with_multiple_failing_it.py',
                            _ok_code=[1],
                            _tty_out=False)
            expect(cmd.stdout).to.match('''
  ..

  0 passing \(\d+ms\)
  2 failing

  1\) can run a failing it:
     Exception: failing on purpose
     File "test/input/describe_with_multiple_failing_it.py", line 9, in _
       raise Exception\('failing on purpose'\)

  2\) can run another failing it:
     Exception: failing on purpose again
     File "test/input/describe_with_multiple_failing_it.py", line 13, in _
       raise Exception\('failing on purpose again'\)

''')

    @describe('xunit reporter', tags=['xunit'])
    def spec():
        @it('can run an empty @describe')
        def _():
            cmd = sh.python('pocha/cli.py',
                            '--reporter', 'xunit',
                            'test/input/describe_with_no_it.py',
                            _ok_code=[0],
                            _tty_out=False)

            expect(cmd.stdout).to.have.xpath('./testsuite[' +
                                             '@name="Pocha Tests" and ' +
                                             '@tests="0" and ' +
                                             '@errors="0" and ' +
                                             '@failures="0" and ' +
                                             '@skip="0"]')


        @it('can run a @describe with a single passing @it')
        def _():
            cmd = sh.python('pocha/cli.py',
                            '--reporter', 'xunit',
                            'test/input/describe_with_single_passing_it.py',
                            _ok_code=[0],
                            _tty_out=False)
            expect(cmd.stdout).to.have.xpath('./testsuite[' +
                                             '@name="Pocha Tests" and ' +
                                             '@tests="1" and ' +
                                             '@errors="0" and ' +
                                             '@failures="0" and ' +
                                             '@skip="0"]')

            expect(cmd.stdout).to.have.xpath('./testsuite/testcase[' +
                                             '@name="can run a single passing it" and ' +
                                             '@classname=""]')

        @it('can run a @describe with multiple passing @it')
        def _():
            cmd = sh.python('pocha/cli.py',
                            '--reporter', 'xunit',
                            'test/input/describe_with_multiple_passing_it.py',
                            _ok_code=[0],
                            _tty_out=False)
            expect(cmd.stdout).to.have.xpath('./testsuite[' +
                                             '@name="Pocha Tests" and ' +
                                             '@tests="2" and ' +
                                             '@errors="0" and ' +
                                             '@failures="0" and ' +
                                             '@skip="0"]')

            expect(cmd.stdout).to.have.xpath('./testsuite/testcase[' +
                                             '@name="can run a passing it" and ' +
                                             '@classname=""]')

            expect(cmd.stdout).to.have.xpath('./testsuite/testcase[' +
                                             '@name="can run another passing it" and ' +
                                             '@classname=""]')

        @it('can run a @describe with a single failing @it')
        def _():
            cmd = sh.python('pocha/cli.py',
                            '--reporter', 'xunit',
                            'test/input/describe_with_single_failing_it.py',
                            _ok_code=[1],
                            _tty_out=False)
            expect(cmd.stdout).to.have.xpath('./testsuite[' +
                                             '@name="Pocha Tests" and ' +
                                             '@tests="1" and ' +
                                             '@errors="0" and ' +
                                             '@failures="1" and ' +
                                             '@skip="0"]')

            expect(cmd.stdout).to.have.xpath('./testsuite/testcase[' +
                                             '@name="can run a single failing it" and ' +
                                             '@classname=""]/error')

        @it('can run a @describe with multiple failing @it')
        def _():
            cmd = sh.python('pocha/cli.py',
                            '--reporter', 'xunit',
                            'test/input/describe_with_multiple_failing_it.py',
                            _ok_code=[1],
                            _tty_out=False)
            expect(cmd.stdout).to.have.xpath('./testsuite[' +
                                             '@name="Pocha Tests" and ' +
                                             '@tests="1" and ' +
                                             '@errors="0" and ' +
                                             '@failures="2" and ' +
                                             '@skip="0"]')

            expect(cmd.stdout).to.have.xpath('./testsuite/testcase[' +
                                             '@name="can run a failing it" and ' +
                                             '@classname=""]/error')

            expect(cmd.stdout).to.have.xpath('./testsuite/testcase[' +
                                             '@name="can run another failing it" and ' +
                                             '@classname=""]/error')
