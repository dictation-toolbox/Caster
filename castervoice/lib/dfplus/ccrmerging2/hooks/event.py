'''
Hook events provide read-only information to hooks.
'''


class BaseHookEvent(object):
    def __init__(self, info):
        self.info = info
