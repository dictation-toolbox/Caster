class TextReplacementExtraData(object):
    def __init__(self, name, required):
        self.name = name  # the name of the extra: what's inside <these>
        self.required = required  # indicates whether this is a required extra
