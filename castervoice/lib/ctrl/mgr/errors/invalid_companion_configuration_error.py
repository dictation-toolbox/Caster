class ICCEMessage(object):
    COMPANION_TYPE = "MergeRules cannot be companion rules; only MappingRules. {} is invalid."


class InvalidCompanionConfigurationError(Exception):
    def __init__(self, rcn, msg=ICCEMessage.COMPANION_TYPE):
        super(InvalidCompanionConfigurationError, self).__init__(msg.format(rcn))
