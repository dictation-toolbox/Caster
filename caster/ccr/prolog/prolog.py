'''
Created on Sep 2, 2015

@author: Gerrish
'''
from dragonfly import Dictation, MappingRule

from caster.lib import control
from caster.lib.actions import Key, Text
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R
from caster.ccr.standard import SymbolSpecs


class PrologNon(MappingRule):
    mapping = {
        "Rule":
            R(Text("() :-.") + Key("left/6"), rdescript="Prolog: rule"),
        SymbolSpecs.IF:
            R(Text("( ") + Key("enter") + Text(";") + Key("enter") + Text(")"),
              rdescript="Prolog: IF"),
    }


class Prolog(MergeRule):
    pronunciation = "prolog"

    non = PrologNon

    mapping = {
        "implies": R(Text(":-"), rdescript="Prolog: Select"),
        "comment": R(Text("%"), rdescript="Prolog: Line Comment"),
        "Open Block comment": R(Text("/* "), rdescript="Prolog: Line Comment"),
        "Close Block comment": R(Text("*\ "), rdescript="Prolog: Line Comment"),
        "Anonymous": R(Text("_"), rdescript="Prolog: Anonymous"),
        "Not": R(Text("\+"), rdescript="Prolog: Not"),
        "cut": R(Text("!"), rdescript="Prolog: cut "),
        "Or": R(Text(";"), rdescript="Prolog: Or"),
        "Fail": R(Text("Fail"), rdescript="Prolog: Fail")
    }

    extras = []
    defaults = {}


control.nexus().merger.add_global_rule(Prolog())
