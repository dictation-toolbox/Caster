class RuleDetails(object):
    """
    A per-rule instantiation configuration.
    """

    def __init__(self, file_path=None, name=None, executable=None, grammar_name=None,
                 enabled=True, ccrtype=None, rdp_mode_exclusion=False, transformer_exclusion=False):
        self.file_path = file_path
        self.name = name
        self.executable = executable
        self.grammar_name = grammar_name
        self.enabled = enabled
        self.declared_ccrtype = ccrtype
        self.rdp_mode_exclusion = rdp_mode_exclusion # TODO: use these last two properties in grammar_manager
        self.transformer_exclusion = transformer_exclusion
