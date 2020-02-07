import os, traceback
import inspect
from castervoice.lib import printer


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
        stack = inspect.stack(0)
        self._filepath = RuleDetails._calculate_filepath_from_frame(stack, 1)

    @staticmethod
    def _calculate_filepath_from_frame(stack, index):
        try:
            frame = stack[index]
            module = inspect.getmodule(frame[0])
            filepath = module.__file__.replace("\\", "/")  
            if filepath.endswith("pyc"):
                filepath = filepath[:-1]
            return filepath
        except AttributeError as e:
            if not os.path.isfile(frame[1]):
                printer.out("\n {} \n File does not exist. A stale .pyc file is in the same dir."
                "\n Delete the .pyc file that has the same name in the file path.\n".format(frame[1]))
            else:
                traceback.print_exc()

    def get_filepath(self):
        return self._filepath
