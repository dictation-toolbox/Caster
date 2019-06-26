class RecognitionHistoryForWSR(list):
    '''
    Copied verbatim from Dragonfly, but doesn't require Natlink
    '''

    def __init__(self, length=10):
        list.__init__(self)

        usable_length = isinstance(length, int) and length >= 1
        if length is None or usable_length:
            self._length = length
        else:
            raise ValueError("length must be a positive int or None,"
                             " received %r." % length)

    def on_recognition(self, words):
        self._complete = True
        self.append(self._recognition_to_item(words))
        if self._length:
            while len(self) > self._length:
                self.pop(0)

    def _recognition_to_item(self, words):
        return tuple(words)
