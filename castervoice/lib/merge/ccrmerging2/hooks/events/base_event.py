class BaseHookEvent(object):
    """
    Hook events provide information to examples.
    """

    def __init__(self, event_type):
        self._type = event_type

    def get_type(self):
        return self._type
