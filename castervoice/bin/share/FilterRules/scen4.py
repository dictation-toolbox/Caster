'''
Created on Sep 27, 2015

@author: synkarius
'''

from castervoice.lib.actions import Text
from castervoice.lib.dfplus.merge.mergepair import MergeInf
from castervoice.lib.dfplus.state.short import R

# Uncomment a function and place this file in your '.caster\filters' folder to activate filter.


def scenario_1(mp):
    '''manually handle a conflicting spec'''
    if mp.type == MergeInf.APP and mp.rule1 is not None:
        print("doing merge for apps")
        for spec in mp.rule1.mapping_actual().keys():
            if spec in mp.rule2.mapping_actual().keys():
                '''this filter function gives priority to
                global  rules over app rules'''
                print("deleting conflicting spec " + spec)
                del mp.rule2.mapping_actual()[spec]


# def get_filter():
#     return scenario_1()


def replace_spec(rule, target, replacement):
    if target in rule.mapping_actual().keys():
        action = rule.mapping_actual()[target]
        del rule.mapping_actual()[target]
        rule.mapping_actual()[replacement] = action


def scenario_2(mp):
    '''replacing a spec'''
    if mp.time == MergeInf.BOOT:
        # at merge time, the base rule can be None, so make sure to check
        target = "[go to] line <n>"
        replacement = "travel to line <n>"

        if mp.rule1 is not None:
            replace_spec(mp.rule1, target, replacement)
        replace_spec(mp.rule2, target, replacement)


# def get_filter():
#     return scenario_2()


def update_python(rule):
    if "shells" in rule.mapping_actual().keys():
        rule.mapping_actual()["shells"] = R(Text("not allowed to use 'else'"),
                                            rdescript="Troll Replacement")


def scenario_3(mp):
    ''' replacing an action '''
    if mp.time == MergeInf.RUN and mp.type == MergeInf.GLOBAL:
        # Inf.RUN means any time except boot or SelfModifyingRule updates
        # Ing.GLOBAL means during global rule de/activation
        if mp.rule1 is not None and mp.rule1.get_pronunciation() == "Python":
            update_python(mp.rule1)
        if mp.rule2.get_pronunciation() == "Python":
            update_python(mp.rule2)


# def get_filter():
#     return scenario_3()


def add_is_to_python(rule):
    if rule.get_pronunciation() == "Python":
        rule.mapping_actual()["identity is"] = R(Text(" is "), rdescript="Python: Is")


def scenario_4(mp):
    ''' adding an action '''
    if mp.time == MergeInf.BOOT:
        if mp.rule1 is not None:
            add_is_to_python(mp.rule1)
        add_is_to_python(mp.rule2)


# def get_filter():
#     return scenario_4()
