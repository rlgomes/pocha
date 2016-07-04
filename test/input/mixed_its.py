from pocha import it


@it('can run a passing it')
def _():
    pass

@it('can run a failing it')
def _():
    raise Exception('failing on purpose')

@it('can run another passing it')
def _():
    pass
