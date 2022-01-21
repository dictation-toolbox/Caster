import inspect
import os
import traceback
from pathlib import Path

from castervoice.lib import printer


class RuleDetails(object):
    """
    A per-rule instantiation configuration.
    """

    def __init__(self, name=None, function_context=None, executable=None, title=None, grammar_name=None,
                 ccrtype=None, transformer_exclusion=False,
                 watch_exclusion=False):
        """
        :param name: Dragonfly rule name
        :param function_context: Dragonfly FunctionContext bool variable
        :param executable: Dragonfly Context executable
        :param title: Dragonfly Context title
        :param grammar_name: Dragonfly grammar name
        :param ccrtype: global, app, selfmod, or none
        :param transformer_exclusion: exclude from transformations
        :param watch_exclusion: should not be watched for changes ("system" rules)
        """
        self.name = name
        self.function_context = function_context
        self.executable = executable
        self.title = title
        self.grammar_name = grammar_name
        self.declared_ccrtype = ccrtype
        self.transformer_exclusion = transformer_exclusion
        self.watch_exclusion = watch_exclusion

        # Python black magic to determine which file to track:
        stack = inspect.stack(0)
        self._filepath = RuleDetails._calculate_filepath_from_frame(stack, 1)

    def __str__(self):
        return 'ccrtype {}'.format(self.declared_ccrtype if self.declared_ccrtype else '_')

    @staticmethod
    def _calculate_filepath_from_frame(stack, index):
        try:
            frame = stack[index]
            # module = inspect.getmodule(frame[1])
            filepath = str(Path(frame[1]))
            if filepath.endswith("pyc"):
                filepath = filepath[:-1]
            return filepath
        except AttributeError:
            if not os.path.isfile(frame[1]):
                pyc = frame[1] + "c"
                if os.path.isfile(pyc):
                    printer.out('\n {}\n Caster removed a stale .pyc file. Please, restart Caster. \n'.format(pyc))
                    os.remove(pyc)
            else:
                traceback.print_exc()

    def get_filepath(self):
        return self._filepath
