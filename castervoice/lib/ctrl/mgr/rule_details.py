import inspect


class RuleDetails(object):
    """
    A per-rule instantiation configuration.
    """

    def __init__(self, name=None, executable=None, title=None, grammar_name=None,
                 ccrtype=None, transformer_exclusion=False,
                 watch_exclusion=False):
        """
        :param name: Dragonfly rule name
        :param executable: Dragonfly AppContext executable
        :param title: Dragonfly AppContext title
        :param grammar_name: Dragonfly grammar name
        :param ccrtype: global, app, selfmod, or none
        :param transformer_exclusion: exclude from transformations
        :param watch_exclusion: should not be watched for changes ("system" rules)
        """
        self.name = name
        self.executable = executable
        self.title = title
        self.grammar_name = grammar_name
        self.declared_ccrtype = ccrtype
        self.transformer_exclusion = transformer_exclusion
        self.watch_exclusion = watch_exclusion

        # Python black magic to determine which file to track:
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        self._filepath = module.__file__.replace("\\", "/")
        if self._filepath.endswith("pyc"):
            self._filepath = self._filepath[:-1]

    def get_filepath(self):
        return self._filepath
