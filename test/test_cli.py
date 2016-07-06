# coding: utf-8

import sh

from robber import expect
from pocha import describe, it


@describe('cli tests')
def cli_tests():

    @it('fails when provided an inexistent path')
    def _():
        cmd = sh.python('pocha/cli.py',
                        'inexistent_path',
                        _ok_code=[2],
                        _tty_out=False)
        stderr = cmd.stderr.decode('utf-8')
        expect(stderr).to.eq('''Usage: cli.py [OPTIONS] [PATH]

Error: Invalid value for path: "inexistent_path" not found
''')
        stdout = cmd.stdout.decode('utf-8')
        expect(stdout).to.eq('')


    @it('fails when provided an invalid reporter')
    def _():
        cmd = sh.python('pocha/cli.py',
                        '--reporter', 'bananas',
                        _ok_code=[2],
                        _tty_out=False)
        stderr = cmd.stderr.decode('utf-8')
        expect(stderr).to.eq('''Usage: cli.py [OPTIONS] [PATH]

Error: Invalid value for "--reporter" / "-r": invalid choice: bananas. (choose from spec, dot, xunit)
''')
        stdout = cmd.stdout.decode('utf-8')
        expect(stdout).to.eq('')

    @it('can display the help menu')
    def _():
        cmd = sh.python('pocha/cli.py',
                        '--help',
                        _ok_code=[0],
                        _tty_out=False)
        stdout = cmd.stdout.decode('utf-8')
        expect(stdout).to.contain('''Usage: cli.py [OPTIONS] [PATH]

Options:
  -r, --reporter [spec|dot|xunit]
  -f, --filter TEXT
  --version                       Show the version and exit.
  --help                          Show this message and exit.
''')
        stderr = cmd.stderr.decode('utf-8')
        expect(stderr).to.eq('')

    @it('can run a test suite')
    def _():
        cmd = sh.python('pocha/cli.py',
                        'test/input/describe_with_multiple_passing_it.py',
                        _ok_code=[0],
                        _tty_out=False)
        stdout = cmd.stdout.decode('utf-8')
        expect(stdout).to.eq(u'''
  top level describe
    ✓ can run a passing it
    ✓ can run another passing it

  2 passing (0ms)

''')
        stderr = cmd.stderr.decode('utf-8')
        expect(stderr).to.eq('')
