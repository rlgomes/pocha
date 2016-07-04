from pocha import describe, it


@describe('top level describe')
def describe1():

    @it('can run a single passing it')
    def passing_it():
        pass
