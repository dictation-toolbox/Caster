'''
Created on Jun 24, 2019

@author: synkarius

1. Run all transformers over all rules.
2. Use a rule set sorter to sort rules.
3. Use a compatibility checker to calculate incompatibility.
4. Pass the transformed/sorted/checked rules to the merging strategy.
---
5. Return the merged rule.
'''
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails


class CCRMerger2(object):

    def __init__(self, ccr_config,
                 transformers, rule_sorter, compatibility_checker,
                 merging_strategy, grammar_manager_class):
        self._config = ccr_config
        #
        self._transformers = transformers
        self._rule_sorter = rule_sorter
        self._compatibility_checker = compatibility_checker
        self._merging_strategy = merging_strategy
        # D.I. gm module so can defer loading grammars 
        self._grammar_manager_class = grammar_manager_class

    '''
    Consideration: should the CCRMerger be in charge of saving the
    config and storing copies of the rules anymore? That seems like
    the GrammarManager's job.
    
    Rather, it seems like the CCRMerger should just be handed a group
    of unordered, unvalidated rules
    '''

    '''saves the current ccr config for next dragon reboot'''

    def save_config(self):
        self._config.save()

    '''loads the ccr config from disk'''

    def load_config(self):
        self._config.load()

    '''adds new rules to the config in 3 groups:
        - global
        - app
        - selfmod
       also adds "ccr_on" to the config  if not exists
       also saves config if anything changed
    '''

    def update_config(self):
        pass

    '''
    X validates that rule has no context
    X validates that rule is a MergeRule
    X (_add_to fn call) validates that pronunciation is not already in hashmap
    
    compatibility checks against all other rules thus far, caches result (this WAS boot time, maybe not any more w/ live reloading)
    
    save to GLOBAL hashmap of {pronunciation: rule}
    '''
    '''
    This method is deprecated. It now simply defers 
    rule storage to GrammarManager. This is a temporary measure.
    Ultimately, each module should call GrammarManager.get_instance
    to configure its loading.
    '''

    def add_global_rule(self, rule):
        rule_class = rule.__class__
        details = RuleDetails(ccr=True)
        self._grammar_manager_class.get_instance().load(rule_class, details)

    '''
    X validates that rule has context
    X validates that rule is a MergeRule
    X (_add_to fn call) validates that pronunciation is not already in hashmap
    
    set default set of rules to merge with to ["alphabet", "navigation", "numbers", "punctuation"] -- do we still want to do this?
    
    compatibility checks against all other rules thus far, caches result (this WAS boot time, maybe not any more w/ live reloading)
    
    save to APP hashmap of {pronunciation: rule}
    '''

    def add_app_rule(self, rule, context):
        rule_class = rule.__class__
        details = RuleDetails(ccr=True)
        self._grammar_manager_class.get_instance().load(rule_class, details)

    '''
    X validates that is selfmod rule
    X validates that is NOT noderule
    X (_add_to fn call) validates that pronunciation is not already in hashmap
    
    sets the merger for the selfmod rule
    
    save to SELFMOD hashmap
    '''

    def add_selfmodrule(self, rule):
        self._validate_rule(
            rule,
            self._selfmod_rule_validator,
            self._get_all_rule_names())
        pass

    '''adds filter to list of filters if not already added'''

    def add_filter(self, filter_fn):
        pass

    '''adds all user-created rules and filters'''

    def add_user_content(self, user_content_manager):
        pass

    '''disable and delete all grammars'''

    def wipe(self):
        pass

    '''turns off all ccr grammars, sets 'ccr_on'=False and saves'''

    def ccr_off(self):
        pass

    '''does merging -- see the original for details/notes'''

    def merge(self, time, name=None, enable=True, save=False):
        pass

    '''IMPLEMENTATION DETAILS'''

    def _validate_rule(self, rule, validator):
        error_message = validator.validate(rule)
        if error_message is not None:
            raise Exception(rule.get_pronunciation() + " " + error_message)

    def _get_all_rule_names(self):
        '''TODO: this'''
        return []
