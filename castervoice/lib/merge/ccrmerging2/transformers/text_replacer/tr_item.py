class TRItem(object):
    def __init__(self):
        self.original = None  # original spec from Caster
        self.extras = []  # bound extras' words
        self.cleaned = None  # original with bound extras replaced with '?'s
        self.altered = None  # 'cleaned' after replacement process
