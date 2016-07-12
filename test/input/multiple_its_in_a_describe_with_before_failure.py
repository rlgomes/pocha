from pocha import before, describe, it


@describe('a describe')
def suite():
    @before
    def teardown():
        raise Exception('doing it on purpose')

    @it('can run a passing it')
    def _():
        pass

    @it('can run another passing it')
    def _():
        pass
