# Pocha - mocha for python

[![Build Status](https://travis-ci.org/rlgomes/pocha.svg?branch=master)](https://travis-ci.org/rlgomes/pocha)

*pocha* was created after spending sometime working in nodejs and finding
that [mocha](https://github.com/mochajs/mocha) made testing very easy in
*nodejs* and there wasn't a similar option for python. `pocha` isn't an
exact clone but has the various features I felt made writing tests in
python easier and cleaner.

# Installation

## Latest build on pypi

```bash
pip install pocha
```

## From source

```bash
pip install -e http://github.com/rlgomes/pocha
```
# Basic usage
## Writing your first test case

Writing a test case is a simple as decorator an existing method with `it`
decorator. Lets write our first test which verifies that the builtin `abs`
function works as desired:

```python
from pocha import it

@it('can verify that abs works for negative numbers')
def negative_numbers():
    assert abs(-1) == 1
```

The above is all you'd have to do to make a python method become a `pocha`
test. With the above in a file called `test.py` you can then run your test
by using the `pocha` cli like so:

```bash
> pocha test.py

  ✓ can verify that abs works for negative numbers

  1 passing (0ms)

```

That was your first test case and it couldn't have been simpler. The correct
way to use pocha though is to split up your tests into test suites and use the
`@describe` decorator like so:

```python
from pocha import describe, it

@describe('abs tests')
def _():

    @it('can verify that abs works for negative numbers')
    def negative_numbers():
        assert abs(-1) == 1
```

Which produces the following output:

```bash
> pocha test.py

  abs tests
    ✓ can verify that abs works for negative numbers

  1 passing (0ms)

```

## Using before and after hooks

There are decorators for running a method before/after all the tests have
executed in a suite or also to run before/after each test in a suite. The
`@before` and `@after` decorators are used to provide hooks to run before and
after a whole suite and generally used for setting up or tearing down some
fixture used by all the tests in suite.

As an example the following:

```python
from pocha import after, before, describe, it

@before
def _():
    print('before hook')

@after
def _():
    print('after hook')

@describe('suite')
def _():

    @it('test1')
    def test1():
        print('from test1')
```

Which as expected would produce the following when executed:

```bash
> pocha foo.py

before hook
  suite
from test1
    ✓ test1
after hook

  1 passing (0ms)
```

Then there are the `@before_each` and `@after_each` decorators which create
hooks that will run before/after each test in a suite.

# Builtin reporters

You can currently choose from 3 different builtin reporters. Here are the
currently available ones and their output for the previous example test:

## spec reporter (default)

The default reporter which mimics the same output that `mochajs` does with a few
tweaks that should make all white space around elements the same.

```bash
> pocha test.py --reporter spec

  abs tests
    ✓ can verify that abs works for negative numbers

  1 passing (0ms)

```

## dot reporter

The `dot` reporter is a minimalist reporter that can be quite useful if you have
a lot of test cases and want to minimize the amount of output from `pocha`.

```bash
> pocha test.py --reporter dot

  .

  1 passing (0ms)

```

## xunit reporter

The `xunit` reporter is of course for any continuous integration system to
consume in order to report test results at a higher level.

```bash
> pocha test.py --reporter xunit
<?xml version="1.0" ?>
<test suite errors="0" failures="0" name="Pocha Tests" skip="0" tests="1">
  <test case classname="abs tests" name="can verify that abs works for negative numbers" time="0.000"/>
</test suite>
```

# Tagging and filtering tests

`pocha` has the ability to tag tests and then allow the end user to run only
tests that satisfy a given filter expression. As an example lets first extend
the previous `abs` test example to something a bit more elaborate:

```python
from pocha import describe, it

@describe('abs tests')
def _():

    @it('can verify that abs works for negative numbers', tags=['negative'])
    def _():
        assert abs(-1) == 1

    @it('can verify that abs works for zero', tags=['zero'])
    def _():
        assert abs(0) == 0

    @it('can verify that abs works for positive numbers', tags=['positive'])
    def _():
        assert abs(1) == 1
```

As you can see tagging is straightforward and running a specific test with a
tag is also very straightforward:

```bash
> pocha test.py --filter negative

  abs tests
    ✓ can verify that abs works for negative numbers

  1 passing (0ms)
```

# Skipping tests

`pocha` has the ability to skip tests easily by setting the `skip=True` flag
on the `describe` or `it` decorator and then that test suite or test case will
simply not execute or appear in the output. The tagging itself would look like
so:

```python
from pocha import describe, it

@describe('abs tests')
def _():

    @it('can verify that abs works for negative numbers', tags=['negative'])
    def _():
        assert abs(-1) == 1

    @it('can verify that abs works for zero', tags=['zero'], skip=True)
    def _():
        assert abs(0) == 0

    @it('can verify that abs works for positive numbers', skip=True)
    def _():
        assert abs(1) == 1
```

The output of running the above test would look like so:

```bash
  abs tests
    ✓ can verify that abs works for negative numbers

  1 passing (0ms)
```

# Debugging tests

When debugging tests sometimes you simply want to run a single test suite or
test case and instead of tagging the test and then proceeding to specify the
exact tag on the command line you want to simply mark that test unit as the
"only" thing to execute. So there's an `only` keyword you can set to True and
`pocha` will run just that test suite or test case. Here's what the usage looks
like:

```python
from pocha import describe, it

@describe('abs tests')
def _():

    @it('can verify that abs works for negative numbers', only=True)
    def _():
        assert abs(-1) == 1

    @it('can verify that abs works for zero')
    def _():
        assert abs(0) == 0

    @it('can verify that abs works for positive numbers')
    def _():
        assert abs(1) == 1
```

Executing the above even when specifying a filter expression on the command
line will always result in the following output:

```bash
  abs tests
    ✓ can verify that abs works for negative numbers

  1 passing (0ms)
```

# Development

You can easily run the existing unittests by installing the test dependencies:

```bash
pip install -r test-requirements.txt

```
Then using `pocha` to run the unittests like so:

```bash
pocha
```

Also be aware that `python setup.py test` works without having to install the
test dependencies in your python virtualenv.

If you have any issues to report please feel free to open a new issue
[here](https://github.com/rlgomes/pocha/issues). Also feel free to open PR's
and submit patches to make `pocha` better for others.
