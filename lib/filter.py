from natlinkutils import GrammarBase
class Filter(GrammarBase):

    # this spec will catch everything
    gramSpec = """
        <start> exported = {emptyList};
    """

    def initialize(self):
        self.load(self.gramSpec, allResults=1)
        self.activateAll()

    def gotResultsObject(self, recogType, resObj):
        for x in range(0, 100):
            try:
                possible_interpretation = resObj.getWords(x)
                # do whatever sort of filtering you want here
            except Exception:
                break

# FILTER=Filter()
# FILTER.initialize()
# also do cleanup