'''
Created on Sep 2, 2015

@author: Gerrish
'''

from castervoice.lib.actions import Text
from castervoice.lib.ctrl.mgr import rdcommon
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


class Prolog(MergeRule):
    pronunciation = "prolog"

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


def get_rule():
    return Prolog, rdcommon.ccr_global()
