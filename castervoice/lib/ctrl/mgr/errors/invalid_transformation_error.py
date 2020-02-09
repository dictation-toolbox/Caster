class ITMessage(object):
    BAD_TYPE = "{} rejected because it no longer descends from its original parent class."
    CLASS_KEY = "{} rejected because its class name changed."


class InvalidTransformationError(Exception):

    def __init__(self, msg, rcn):
        super(InvalidTransformationError, self).__init__(msg.format(rcn))
