from pocha import it


@it('first it', tags=['first', 'edge'])
def _():
    pass

@it('second it', tags=['second', 'middle'])
def _():
    pass

@it('third it', tags=['third', 'edge'])
def _():
    pass
