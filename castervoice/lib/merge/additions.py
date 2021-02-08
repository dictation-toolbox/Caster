from dragonfly import ShortIntegerRef
from dragonfly.grammar.elements import Choice

IntegerRefST = ShortIntegerRef
# Compatibility shim for older grammars that use IntegerRefST.
# IntegerRefST and Integer Remap has deprecated.
# Use dragonfly ShortIntegerRef


class Boolean(Choice):
    def __init__(self, spec):
        Choice.__init__(self, spec, {spec: True})
