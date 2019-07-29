class BaseHook(object):

    def __init__(self, event_type):
        self._type = event_type

    def run(self):
        pass

    def match(self, event_type):
        return self._type == event_type
