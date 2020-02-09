class NoPronunciationError(Exception):
    """
    This error should NEVER actually be thrown since rules without
    pronunciations should get rejected by loading safety checks.
    """

    def __init__(self, rcn):
        super(NoPronunciationError, self).__init__(
            "Rule has no pronunciation: {}.".format(rcn))
