from pocha import it


@it('first it', tags=['first', 'edge'], skip=True)
def _():
    pass

@it('second it', tags=['second', 'middle'])
def _():
    pass

@it('third it', tags=['third', 'edge'], skip=True)
def _():
    pass
