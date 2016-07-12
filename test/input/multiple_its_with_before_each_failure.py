from pocha import before_each, it


@before_each
def setup():
    raise Exception('doing it on purpose')

@it('can run a passing it')
def _():
    pass

@it('can run another passing it')
def _():
    pass
