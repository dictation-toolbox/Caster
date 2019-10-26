class TreeRuleConfigurationError(Exception):
    def __init__(self, msg):
        super(TreeRuleConfigurationError, self).__init__(msg)