from pocha import it


@it('can run a single failing it')
def failing():
    raise Exception('failing on purpose')
