'''
Created on Sep 11, 2018

@author: Mike Roberts
'''
from dragonfly import Function, Mouse

from caster.lib import control
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R
from caster.lib.ccr.hearthstone import key
from caster.lib import settings

import time

class Hearthstone(MergeRule):
    pronunciation = "hearth stone"
    mapping = {
        "my <boardn>":
            R(Function(key.my_minions)),
        "hero":
            R(Function(key.hero)),
        "his <boardn>":
            R(Function(key.his_minions)),
        "face":
            R(Function(key.face)),
        "hand <handn>":
            R(Function(key.hand)),
        "tap":
            R(Function(key.tap)),
        "end this turn":
            R(Function(key.end_turn)),
        "board":
            R(Function(key.click_board)),
    }

    extras = [
        IntegerRefST("boardn", 1, 14),
        IntegerRefST("handn", 1, 11),
    ]
    defaults = {
    }


control.nexus().merger.add_global_rule(Hearthstone())
