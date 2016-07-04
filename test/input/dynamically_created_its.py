from pocha import it


for index in range(1, 6):
    @it('passing it #%d' % index)
    def _():
        pass
