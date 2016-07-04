from pocha import describe, it


@describe('top level describe')
def describe1():

    @it('can run a failing it')
    def _():
        raise Exception('failing on purpose')

    @it('can run another failing it')
    def _():
        raise Exception('failing on purpose again')
