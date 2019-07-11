'''
A hook for the loading/unloading of CCR 'non'
(affiliated but non-ccr) rules.
'''
from castervoice.lib.ctrl.mgr import grammar_manager
from castervoice.lib.dfplus.ccrmerging2.hooks.base_hook import BaseHook

'''{ccr rule class name: nonccr rule class name}'''
nons = {}


class MergeRuleNonCCRRuleHook(BaseHook):
    def run(self, event):
        if event.activate:
            event.ccr_rule_class_name
            gm = grammar_manager.GrammarManager.get_instance()
