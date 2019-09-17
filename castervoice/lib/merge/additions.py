from dragonfly import (IntegerRef, Integer)
from dragonfly.grammar.elements import RuleWrap, Choice
from dragonfly.language.base.integer_internal import MapIntBuilder
from dragonfly.language.loader import language
from dragonfly.language.en.short_number import ShortIntegerContent

from castervoice.lib import settings, alphanumeric

'''
Integer Remap feature needs to be rewritten:
    - allow customization
    - make it language sensitive (can this be done without eval?)
''' 
if not settings.settings(["miscellaneous", "integer_remap_crash_fix"]):
    class IntegerRefST(RuleWrap):
        def __init__(self, name, min, max, default=None):
            if not settings.settings(["miscellaneous", "short_integer_opt_out"]):
                content = language.ShortIntegerContent
            else:
                content = language.IntegerContent
                
            if "en" in language.language_map and settings.settings(["miscellaneous", "integer_remap_opt_in"]):
                content.builders[1] = MapIntBuilder(alphanumeric.numbers_map_1_to_9())

            element = Integer(None, min, max, content=content)
            RuleWrap.__init__(self, name, element, default=default)
            
else:
    print("Integer Remap switch: OFF")

    class IntegerRefST(IntegerRef):
        ''''''


class Boolean(Choice):
    def __init__(self, spec):
        Choice.__init__(self, spec, {spec: True})
