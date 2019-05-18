#
# __author__ = "lexxish"
# __license__ = "LGPL"
# __version__ = "3.0"
#


class Phrase:
    def __init__(self, key, description=None):
        self.key = key
        if description is None:
            self.description = key.title()
        else:
            self.description = description

