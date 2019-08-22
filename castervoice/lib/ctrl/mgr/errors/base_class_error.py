class DontUseBaseClassError(Exception):
    def __init__(self, base_instance):
        super(DontUseBaseClassError, self).__init(
            "Do not use base class ({}).".format(base_instance.__class__.__name__))
