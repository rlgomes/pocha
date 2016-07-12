# coding: utf-8

import sh

from robber import expect
from pocha import describe, it

from test import util
util.init()


@describe('@before_each and @after_each tests')
def pocha_cli():

    @it('fails on every @it with the @before_each that fails')
    def _():
        cmd = sh.python('pocha/cli.py',
                        'test/input/multiple_its_with_before_each_failure.py',
                        _ok_code=[1],
                        _tty_out=False)
        stdout = cmd.stdout.decode('utf-8')
        expect(stdout).to.match(u'''
  1\) "before each" hook for "can run a passing it"
  2\) "before each" hook for "can run another passing it"

  0 passing \(\d+ms\)
  2 failing

  1\) "before each" hook for "can run a passing it":
     Exception: doing it on purpose
     File "test/input/multiple_its_with_before_each_failure.py", line 6, in setup
       raise Exception\('doing it on purpose'\)

  2\) "before each" hook for "can run another passing it":
     Exception: doing it on purpose
     File "test/input/multiple_its_with_before_each_failure.py", line 6, in setup
       raise Exception\('doing it on purpose'\)

''')

    @it('fails on every failing @after_each but the @it succeeds')
    def _():
        cmd = sh.python('pocha/cli.py',
                        'test/input/multiple_its_with_after_each_failure.py',
                        _ok_code=[1],
                        _tty_out=False)
        stdout = cmd.stdout.decode('utf-8')
        expect(stdout).to.match(u'''
  ✓ can run a passing it
  1\) "after each" hook for "can run a passing it"
  ✓ can run another passing it
  2\) "after each" hook for "can run another passing it"

  2 passing \(\d+ms\)
  2 failing

  1\) "after each" hook for "can run a passing it":
     Exception: doing it on purpose
     File "test/input/multiple_its_with_after_each_failure.py", line 6, in setup
       raise Exception\('doing it on purpose'\)

  2\) "after each" hook for "can run another passing it":
     Exception: doing it on purpose
     File "test/input/multiple_its_with_after_each_failure.py", line 6, in setup
       raise Exception\('doing it on purpose'\)

''')
