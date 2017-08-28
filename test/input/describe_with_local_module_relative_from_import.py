from pocha import describe, it

from ..input import util


@describe('top level describe')
def describe1():

    @it('can call out to a local module from import')
    def _():
        assert util.add(1, 1) == 2
