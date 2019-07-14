from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.managed_rule import ManagedRule
from castervoice.lib.ctrl.mgr.managed_rule_multidict import ManagedRuleMultiDict

"""
Jobs of the grammar manager:
1. Keep a copy of the latest stable version of a rule.
2. Know when a rule has changed (make an observer class to compose with this?)
3. Be in charge of loading/unloading via an internal loading grammar 
        -- this also applies to non-CCR grammars
        MappingRules should be enabled with 'enable' + (their name, else their Grammar's 'name', else executable)
"""


class GrammarManager(object):

    def __init__(self, config,
                 merger,
                 ccr_rules_validator,
                 details_validator,
                 reload_observable,
                 activator,
                 mapping_rule_maker,
                 grammars_container,
                 always_global_ccr_mode):
        """
        Holds both the current merged ccr rules and the most recently instantiated/validated
        copies of all ccr and non-ccr rules.
        Loads all previously acti TODO this description
        :param config: config impl which externally tracks which rules are activated
        :param merger: The CCRMerger TODO: consider just passing in a method reference
        :param ccr_rules_validator: validation for ccr rules
        :param details_validator: validation of rule details configuration objects
        :param reload_observable: the thing that signals that a file or files have changed
        :param activator: manages the "enable/disable X" grammar
        :param mapping_rule_maker: instantiates (TODO and clears?) mapping rules
        :param grammars_container: holds and destroys grammars
        :param always_global_ccr_mode: an option which forces every rule to be treated as a global ccr rule
        """
        self._config = config
        self._merger = merger
        self._ccr_rules_validator = ccr_rules_validator
        self._details_validator = details_validator
        self._reload_observable = reload_observable
        self._activator = activator
        self._mapping_rule_maker = mapping_rule_maker
        self._grammars_container = grammars_container
        self._always_global_ccr_mode = always_global_ccr_mode

        # rules: (class name : ManagedRule}
        self._managed_rules = ManagedRuleMultiDict()
        # companion rules -- when a rule is activated, it can have 0-n companion rules auto activated with it
        self._companion_rules = {}
        #
        self._reload_observable.register_listener(self)
        #
        self._activator.set_activation_fn(self._change_rule_active)

    def _change_rule_active(self, class_name, active):
        """
        Either creates a standalone Dragonfly rule or
        delegates to the CCRMerger to create the merged rule(s)

        :param class_name:
        :param active:
        :return:
        """

        # update config, save
        self._config.update(class_name, active)
        self._config.save()

        managed_rule = self._managed_rules.get_by_class_name(class_name)


        ccrtype = managed_rule.details.declared_ccrtype
        ''' 
        This setting controls "RDP Mode". Using "RDP Mode" is not recommended. 
        It forces any rule to load as a global ccr rule and ignores validation.
        '''
        if self._always_global_ccr_mode:
            ccrtype = CCRType.GLOBAL

        if ccrtype is not None:
            '''
            handle CCR:
            get all active ccr rules after de/activating one'''
            active_rule_class_names = self._config.get_active_rule_class_names()
            active_rules = [self._managed_rules.get_by_class_name(rcn) for rcn in active_rule_class_names]
            active_ccr_rules = [mr for mr in active_rules if mr.details.declared_ccrtype is not None]

            '''
            The merge may result in 1 to n+1 rules where n is the number of ccr app rules
            which are in the active rules list.
            For instance, if you have 1 app rule, you'll end up with two ccr rules. This is because
            the merger has to make the global one, plus an app rule with the app stuff plus all the
            global stuff.
            '''
            ccr_rules = self.merger.merge(active_ccr_rules)
            # TODO make Grammar(s)
            '''
            new_managed_rule = ManagedRule(ccr_rule, grammar?, ) --- no, managed rules are the pieces
            -- ccr_rules are the result
            '''
            # TODO: activate grammar
        else:
            # TODO: activate grammar
            '''if activating, have df_maker make it'''
            if active:
                grammar = self._mapping_rule_maker.create_non_ccr_grammar(
                    managed_rule.get_rule_class(), managed_rule.get_details())
                self._grammars_container.set_non_ccr(self, managed_rule.get_rule_class_name(), grammar)
            else:
                self._grammars_container.set_non_ccr(self, managed_rule.get_rule_class_name(), None)


    """
    Do not call this manually. Should only be called by the reload observable.
    """
    def receive(self, file_path_changed):
        '''
        TODO: this
        1. match path to class name -- all rules will have both
        2. call ---... the content loader is in the nexus but not here
            --but call "idem_import_module(module_name, "get_rule")
        3. then take result and send it to self._register_rules_from_content_manager(rs)
        '''
        managed_rule = self._managed_rules.get_by_file_path(file_path_changed)



        pass

    """
    rule_sets: a list of tuples
    """
    def register_rules_from_content_manager(self, rule_sets):
        for rule_set in rule_sets:
            for rd in rule_set:
                rule_class = rd[0]
                rule_details = rd[1]

                invalidation = self._get_invalidation(rule_class, rule_details)
                if invalidation is not None:
                    print(invalidation)
                    continue

                self.register_rule(rule_class, rule_details)
                self._reload_observable.register_watched_file(rule_details.path)

    """
    attempts to find a reason to invalidate the rule
    """
    def _get_invalidation(self, rule_class, details):
        if self._always_global_ccr_mode:
            return None

        name = rule_class.__name__

        '''validate details configuration before anything else'''
        details_invalidation = self._details_validator.validate_details(details)
        if details_invalidation is not None:
            return name + " rejected due to detail validation errors: " + details_invalidation

        '''attempt to instantiate the rule'''
        test_instance = None
        try:
            test_instance = rule_class()
        except: #ignore warnings on this line-- it's supposed to be broad
            return name + " rejected due to instantiation errors"

        '''if ccr, validate the rule'''
        if details.declared_ccrtype is not None:
            error = self._ccr_rules_validator.validate(test_instance, details.declared_ccrtype)
            if error is not None:
                return name + " rejected due to rule validation errors: " + error

        return None


    '''
    If a rule is registered a second time, 
    A. The new version should be attempted to be loaded.
    B. If it loads, the old version should
        1. have its grammar unloaded if there is a grammar
        2. be deleted from the _managed_rules map
    
    TODO:
    Okay, so instantiation errors are one thing, but what if we never make it to
    the "register" call? That is going to have to be handled, maybe in the "loading"
    package.
    -- can't recover if it fails on reboot
    -- can recover afterwards -- if it fails importlib, the crash will not deregister the old version
    '''

    def register_rule(self, rule_class, details):
        name = rule_class.__name__

        '''if already registered, unregister it'''
        if name in self._managed_rules:
            self._unregister(name)

        '''
        rule should be safe for loading at this point: register it
        but do not load here -- this method only registers
        '''
        managed_rule = ManagedRule(rule_class, details)
        self._managed_rules[name] = managed_rule

    """
    Both rules must be registered before registering the companion.
        self._companion_rules is {rule: [companions]}
        
        TODO: -- should this just happen in a config file???
    """
    def _register_companion_rule(self, rule_class, companion_rule_class):
        rule_class_name = rule_class.__name__
        companion_rule_class_name = companion_rule_class.__name__

        if rule_class_name in self._managed_rules and \
                companion_rule_class_name in self._managed_rules:
            companions_list = [] if not rule_class_name in self._companion_rules \
                else self._companion_rules[rule_class_name]
            companions_list.append(companion_rule_class_name)
            self._companion_rules[rule_class_name] = companions_list

    """
    
    """
    def _unregister(self, rule_class_name):
        if rule_class_name in self._managed_rules:
            managed_rule = self._managed_rules[rule_class_name]
            if managed_rule.grammar is not None:
                # disable all rules
                for rule in managed_rule.grammar.rules:
                    rule.disable()
                # disable / unload / delete grammar
                managed_rule.grammar.disable()
                managed_rule.grammar.unload()
            del self._managed_rules[rule_class_name]

