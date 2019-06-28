'''
Created on Jun 24, 2019

@author: synkarius
'''

class CCRMerger2(object):
    
    '''
    validators:
        global = mergerule + no_context + pronunciation
        app    = context + pronunciation
        selfmod= selfmod + not_noderule + pronunciation
    
    '''
    def __init__(self, ccr_config, global_rule_validator, 
                 app_rule_validator, selfmod_rule_validator):
        self._config = ccr_config
        self._global_rule_validator = global_rule_validator
        self._app_rule_validator = app_rule_validator
        self._selfmod_rule_validator = selfmod_rule_validator

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
    def add_global_rule(self, rule):
        self._validate_rule(
            rule, 
            self._global_rule_validator, 
            self._get_all_rule_names())
        pass

    '''
    X validates that rule has context
    X validates that rule is a MergeRule
    X (_add_to fn call) validates that pronunciation is not already in hashmap
    
    set default set of rules to merge with to ["alphabet", "navigation", "numbers", "punctuation"] -- do we still want to do this?
    
    compatibility checks against all other rules thus far, caches result (this WAS boot time, maybe not any more w/ live reloading)
    
    save to APP hashmap of {pronunciation: rule}
    '''
    def add_app_rule(self, rule, context):
        self._validate_rule(
            rule, 
            self._app_rule_validator, 
            self._get_all_rule_names())
        pass

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

