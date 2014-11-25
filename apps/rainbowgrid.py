"""
Command-module for RainbowGrid

"""

from dragonfly import (Grammar, AppContext, CompoundRule,
                       IntegerRef,Repeat,
                       Key, Choice)

from lib import utilities


class GridControlRule(CompoundRule):

    spec = "[<pre>] <color> <n>"
    extras = [IntegerRef("pre", 0, 9),
              Choice("color", {
                              "red": "0",
                              "(orange | tan | brown)": "1",
                              "yellow": "2",
                              "green": "3",
                              "blue": "4",
                              "purple": "5"
                             }
                    ),
              IntegerRef("n", 0, 100),
             ]
    defaults = {
                "pre": 0,
               }

    def _process_recognition(self, node, extras):
        Key("p")._execute()
        utilities.press_digits(0)
        utilities.press_digits(extras["pre"])
        Key("c")._execute()
        utilities.press_digits(0)
        utilities.press_digits(extras["color"])
        Key("n")._execute()
        if int(extras["n"]<10):
            utilities.press_digits(0)
        utilities.press_digits(extras["n"])

class ExitRule(CompoundRule):

    spec = "exit"
    extras = []
    defaults = {}

    def _process_recognition(self, node, extras):
        for i in range(0, 2):
            Key("x")._execute()
#---------------------------------------------------------------------------

context = AppContext(title="rainbowgrid")
grammar = Grammar("rainbowgrid", context=context)
grammar.add_rule(GridControlRule())
grammar.add_rule(ExitRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
