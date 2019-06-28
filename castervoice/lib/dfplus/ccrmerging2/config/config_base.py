from castervoice.lib.dfplus.ccrmerging2 import const

'''abstract CCRConfig implementation'''
class BaseCCRConfig(object):
    def __init__(self):
        self._config = {}
    
    '''input args are three lists of MergeRules 
        -- expecting get_pronunciation() method on list members to
        generate keys'''
    def update(self, global_rules, app_rules, selfmod_rules):
        changed = False
        '''set up config dict'''
        if not const.CCR_ON in self._config:
            self._config[const.CCR_ON] = True
            changed = True
        for rule_set_name in [const.GLOBAL, const.APP, const.SELFMOD]:
            if not rule_set_name in self._config:
                self._config[rule_set_name] = {}
                changed = True
        
        '''detect and add new rules'''
        for rule_set in [(const.GLOBAL, global_rules), \
                         (const.APP, app_rules), \
                         (const.SELFMOD, selfmod_rules)]:
            changed = changed or self._add_new_rules(rule_set)
            
        if changed: self.save_config()
    
    '''can be used by merger'''
    def is_rule_active(self, ruleset_name, rule_name):
        if self._config[ruleset_name] is not None:
            return self._config[rule_name] == True
        return False
    
    def _add_new_rules(self, rule_set):
        changed = False
        for r in rule_set:
            rule_set_name = r[0]
            rule_names = [rule.get_pronunciation() for rule in r[1]]
            for rule_name in rule_names:
                if not rule_name in self._config[rule_set_name]:
                    default_value = True if rule_set_name != const.GLOBAL else rule_name in const.CORE
                    self._config[rule_set_name][rule_name] = default_value
                    changed = True
        return changed


        
    
            