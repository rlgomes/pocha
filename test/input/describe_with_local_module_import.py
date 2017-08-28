from pocha import describe, it

import util

@describe('top level describe')
def describe1():

    @it('can call out to a local module')
    def _():
        assert util.add(1, 1) == 2
