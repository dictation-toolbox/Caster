'''
Created on Sep 6, 2015

@author: synkarius
'''

from dragonfly.actions.action_function import Function
from dragonfly.actions.action_playback import Playback

from caster.lib import control
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.mergerule import MergeRule
from caster.lib.dfplus.state.actions import AsynchronousAction
from caster.lib.dfplus.state.short import L, S, R


def _f(n):
    if len(control.nexus().history) > 0:
        utterance = [str(x) for x in " ".join(control.nexus().history[len(control.nexus().history) - 1]).split()]
        if utterance[0] == "again": return
        def repeat():
            u = utterance
            Playback([(u, 0.0)]).execute()
            return False
        forward = [L(S(["cancel"], repeat))]
        AsynchronousAction(forward, rdescript="Repeat Last Action", time_in_seconds=0.2, repetitions=int(n), blocking=False).execute()
            
            

class Again(MergeRule):  
    
    mapping = { "again (<n> [(times|time)] | do)":  R(Function(_f), show=False) }
    extras = [ IntegerRefST("n", 1, 50) ]
    defaults = { "n": 1 }

