from pocha import describe, it


@describe('top level describe')
def describe1():

    @it('can run a passing it')
    def _():
        pass
    
    @it('can run another passing it')
    def _():
        pass
