from castervoice.lib.merge.ccrmerging2.transformers.text_replacer.tr_definitions import TRDefinitions


class MockTRParser(object):

    def __init__(self, specs, extras, defaults):
        self.specs = specs
        self.extras = extras
        self.defaults = defaults

    def create_definitions(self):
        return TRDefinitions(self.specs, self.extras, self.defaults)