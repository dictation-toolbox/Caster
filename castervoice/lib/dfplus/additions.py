from dragonfly import (ActionBase, IntegerRef, Integer)
from dragonfly.grammar.elements import RuleWrap, Choice
from dragonfly.language.base.integer_internal import MapIntBuilder, \
    IntegerContentBase
from dragonfly.language.loader import language

from castervoice.lib import utilities, settings, alphanumeric


class SelectiveAction(ActionBase):
    def __init__(self, action, executables, negate=True):
        '''
        action: another Dragonfly action
        executables: an array of strings, each of which is the name of an executable
        negate: if True, the action should not occur during any of the listed executables, if false the opposite
        '''
        ActionBase.__init__(self)
        self.action = action
        self.executables = executables
        self.negate = negate

    def _execute(self, data=None):
        executable = utilities.get_active_window_path().split("\\")[-1]
        is_executable = executable in self.executables
        if (is_executable and not self.negate) or (self.negate and not is_executable):
            self.action.execute()


'''
Integer Remap feature needs to be rewritten:
    - allow customization
    - make it language sensitive (can this be done without eval?)
'''
if not settings.SETTINGS["miscellaneous"]["integer_remap_crash_fix"]:

    from dragonfly.language.en.number import int_0, int_1_9, int_10_19, int_20_99, \
        int_100s, int_100big, int_1000s, int_1000000s
    # IntegerRefST
    INTEGER_CONTENT = language.IntegerContent

    class IntegerContentST(IntegerContentBase):
        builders = [
            int_0, int_1_9, int_10_19, int_20_99, int_100s, int_100big, int_1000s,
            int_1000000s
        ]

    if "en" in language.language_map and settings.SETTINGS["miscellaneous"]["integer_remap_opt_in"]:
        mapping = alphanumeric.numbers_map_1_to_9()
        IntegerContentST.builders[1] = MapIntBuilder(mapping)
        INTEGER_CONTENT = IntegerContentST

    class IntegerST(Integer):
        def __init__(self,
                     name=None,
                     min=None,
                     max=None,
                     default=None,
                     content=INTEGER_CONTENT):
            Integer.__init__(self, None, min, max, None, content)

    class IntegerRefST(IntegerRef):
        def __init__(self, name, min, max, default=None):
            element = IntegerST(None, min, max)
            RuleWrap.__init__(self, name, element, default=default)
else:
    print("Integer Remap switch: OFF")

    class IntegerRefST(IntegerRef):
        ''''''


class Boolean(Choice):
    def __init__(self, spec):
        Choice.__init__(self, spec, {spec: True})
