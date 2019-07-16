'''
Created on Sep 2, 2015

@author: Gerrish
'''
from castervoice.lib.imports import *

class PrologNon(MappingRule):
    mapping = {
        "Rule":
            R(Text("() :-.") + Key("left/6")),
        SymbolSpecs.IF:
            R(Text("( ") + Key("enter") + Text(";") + Key("enter") + Text(")")),
    }


class Prolog(MergeRule):
    pronunciation = "prolog"

    non = PrologNon

    mapping = {
        "implies": R(Text(":-")),
        "comment": R(Text("%")),
        "Open Block comment": R(Text("/* ")),
        "Close Block comment": R(Text("*\ ")),
        "Anonymous": R(Text("_")),
        "Not": R(Text("\+")),
        "cut": R(Text("!")),
        "Or": R(Text(";")),
        "Fail": R(Text("Fail"))
    }

    extras = []
    defaults = {}


control.global_rule(Prolog())
