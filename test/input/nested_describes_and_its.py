from pocha import describe, it


@describe('level 1 describe')
def describe1():

    @it('level 1 it')
    def it1():
        pass

    @describe('level 2 describe')
    def describe2():

        @it('level 2 it')
        def it2():
            pass
