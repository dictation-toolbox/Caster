class GuidanceRejectionException(Exception):

    _MSG = "Unit tests should not write files unless they clean them up too."

    def __init__(self):
        super(GuidanceRejectionException, self).__init__(GuidanceRejectionException._MSG)