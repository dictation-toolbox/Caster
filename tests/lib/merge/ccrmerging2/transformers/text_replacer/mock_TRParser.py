from castervoice.lib.merge.ccrmerging2.transformers.text_replacer.tr_definitions import TRDefinitions

MOCK_SPECS = {}
MOCK_EXTRAS = {}
MOCK_DEFAULTS = {}


class MockTRParser(object):

    def create_definitions(self):
        return TRDefinitions(MOCK_SPECS, MOCK_EXTRAS, MOCK_DEFAULTS)