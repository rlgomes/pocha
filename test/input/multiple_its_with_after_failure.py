from pocha import after, it


@after
def teardown():
    raise Exception('doing it on purpose')

@it('can run a passing it')
def _():
    pass

@it('can run another passing it')
def _():
    pass
