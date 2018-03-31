'''
Created on Sep 27, 2015

@author: synkarius
'''
from dragonfly.actions.action_key import Key

from caster.lib.dfplus.merge.mergepair import MergeInf
from caster.lib.dfplus.state.short import R


def add_modkeys(rule):
    release = R(Key("shift:up, ctrl:up, alt:up"), rdescript="Mod Keys Up")

    if not hasattr(rule, "marked") and\
    rule.get_pronunciation()[0:6] != "Merged": # don't augment merged rules-- they'd get it twice
        for spec in rule.mapping_actual().keys():
            rule.mapping_actual()[spec] = release + rule.mapping_actual()[spec] + release
        rule.marked = True


def modkeysup(mp):
    if mp.time == MergeInf.BOOT:
        if mp.rule1 is not None:
            add_modkeys(mp.rule1)
        add_modkeys(mp.rule2)


# control.nexus().merger.add_filter(modkeysup)
