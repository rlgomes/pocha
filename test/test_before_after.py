# coding: utf-8

import sh

from robber import expect
from pocha import describe, it

from test import util
util.init()


@describe('@before and @after tests')
def pocha_cli():

    @it('fails and stops running as soon as the first @before fails within a few @its')
    def _():
        cmd = sh.python('pocha/cli.py',
                        'test/input/multiple_its_with_before_failure.py',
                        _ok_code=[1],
                        _tty_out=False)
        stdout = cmd.stdout.decode('utf-8')
        expect(stdout).to.match(u'''
  1\) "before all" hook

  0 passing \(\d+ms\)
  1 failing

  1\) "before all" hook:
     Exception: doing it on purpose
     File "test/input/multiple_its_with_before_failure.py", line 6, in setup
       raise Exception\('doing it on purpose'\)

''')

    @it('fails when @after fails within a few @its')
    def _():
        cmd = sh.python('pocha/cli.py',
                        'test/input/multiple_its_with_after_failure.py',
                        _ok_code=[1],
                        _tty_out=False)
        stdout = cmd.stdout.decode('utf-8')
        expect(stdout).to.match(u'''
  ✓ can run a passing it
  ✓ can run another passing it
  1\) "after all" hook

  2 passing \(\d+ms\)
  1 failing

  1\) "after all" hook:
     Exception: doing it on purpose
     File "test/input/multiple_its_with_after_failure.py", line 6, in teardown
       raise Exception\('doing it on purpose'\)

''')

    @it('fails and stops running as soon as the first @before fails within a @describe')
    def _():
        cmd = sh.python('pocha/cli.py',
                        'test/input/multiple_its_in_a_describe_with_before_failure.py',
                        _ok_code=[1],
                        _tty_out=False)
        stdout = cmd.stdout.decode('utf-8')
        expect(stdout).to.match(u'''
  a describe
    1\) "before all" hook

  0 passing \(\d+ms\)
  1 failing

  1\) "before all" hook:
     Exception: doing it on purpose
     File "test/input/multiple_its_in_a_describe_with_before_failure.py", line 8, in teardown
       raise Exception\('doing it on purpose'\)

''')

    @it('fails when @after fails within a @describe')
    def _():
        cmd = sh.python('pocha/cli.py',
                        'test/input/multiple_its_in_a_describe_with_after_failure.py',
                        _ok_code=[1],
                        _tty_out=False)
        stdout = cmd.stdout.decode('utf-8')
        expect(stdout).to.match(u'''
  a describe
    ✓ can run a passing it
    ✓ can run another passing it
  1\) "after all" hook

  2 passing \(\d+ms\)
  1 failing

  1\) "after all" hook:
     Exception: doing it on purpose
     File "test/input/multiple_its_in_a_describe_with_after_failure.py", line 8, in teardown
       raise Exception\('doing it on purpose'\)

''')
