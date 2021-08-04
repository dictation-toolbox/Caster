from dragonfly import ShortIntegerRef
from dragonfly.grammar.elements import Choice
from castervoice.lib import printer


class IntegerRefST(ShortIntegerRef):
    """
    Compatibility shim for older grammars that use IntegerRefST.
    IntegerRefST and Integer Remap has been removed use dragonfly ShortIntegerRef
    """

    def __init__(self, name, min, max, default=None):
        printer.out("\nDetected 'IntegerRefST' import in rules/grammars.\nIntegerRefST and Integer Remap has been removed. \nUpdate your rules to `from dragonfly import ShortIntegerRef` in instead of IntegerRefST\n")
        super(IntegerRefST, self).__init__(name, min, max, default)


class Boolean(Choice):
    def __init__(self, spec):
        Choice.__init__(self, spec, {spec: True})
