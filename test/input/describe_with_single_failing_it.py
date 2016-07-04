from pocha import describe, it


@describe('top level describe')
def describe1():

    @it('can run a single failing it')
    def failing_it():
        raise Exception('failing on purpose')
