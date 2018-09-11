'''
Created on Sep 11, 2018

@author: Mike Roberts
'''
from dragonfly import Function

from caster.lib import control
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R
from caster.lib.ccr.hearthstone import key
from caster.lib import settings

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
        "end turn":
            R(Function(key.end_turn)),
        "store mouse position":
            R(Function(key.get_mouse_position)),
    }

    extras = [
        IntegerRefST("boardn", 1, 13),
        IntegerRefST("handn", 1, 10),
    ]
    defaults = {
    }


control.nexus().merger.add_global_rule(Hearthstone())
