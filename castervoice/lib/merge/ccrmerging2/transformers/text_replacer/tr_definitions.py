class TRDefinitions(object):
    def __init__(self, specs, extras, defaults):
        self.specs = specs
        self.extras = extras
        self.defaults = defaults

    def __len__(self):
        return len(self.specs) + len(self.extras) + len(self.defaults)
