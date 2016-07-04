from pocha import describe, it


@describe('first describe')
def describe1():

    @it('first it')
    def _():
        pass

    @it('second it')
    def _():
        pass

@describe('second describe', only=True)
def describe1():

    @it('third it')
    def _():
        pass

    @it('fourth it')
    def _():
        pass
