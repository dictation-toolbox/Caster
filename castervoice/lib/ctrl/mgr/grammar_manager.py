import os

from dragonfly import Grammar

from castervoice.lib import printer
from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.errors.not_a_module import NotAModuleError
from castervoice.lib.ctrl.mgr.loading.content_type import ContentType
from castervoice.lib.ctrl.mgr.managed_rule import ManagedRule
from castervoice.lib.dfplus.ccrmerging2.hooks.events.activation_event import RuleActivationEvent

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
                 content_loader,
                 ccr_rules_validator,
                 details_validator,
                 reload_observable,
                 activator,
                 mapping_rule_maker,
                 grammars_container,
                 hooks_runner,
                 always_global_ccr_mode):
        """
        Holds both the current merged ccr rules and the most recently instantiated/validated
        copies of all ccr and non-ccr rules.
        Loads all previously acti TODO this description

        TODO: this is a god object; it should be broken apart

        :param config: config impl which externally tracks which rules are activated
        :param merger: The CCRMerger
        :param ccr_rules_validator: validation for ccr rules
        :param details_validator: validation of rule details configuration objects
        :param reload_observable: the thing that signals that a file or files have changed
        :param activator: manages the "enable/disable X" grammar
        :param mapping_rule_maker: instantiates
        :param grammars_container: holds and destroys grammars
        :param hooks_runner: runs all hooks at different events
        :param always_global_ccr_mode: an option which forces every rule to be treated as a global ccr rule
        """
        self._config = config
        self._merger = merger
        self._content_loader = content_loader
        self._ccr_rules_validator = ccr_rules_validator
        self._details_validator = details_validator
        self._reload_observable = reload_observable
        self._activator = activator
        self._mapping_rule_maker = mapping_rule_maker
        self._grammars_container = grammars_container
        self._hooks_runner = hooks_runner
        self._always_global_ccr_mode = always_global_ccr_mode

        # rules: (class name : ManagedRule}
        self._managed_rules = {}
        # companion rules -- when a rule is activated, it can have 0-n companion rules auto activated with it
        self._companion_rules = {}
        #
        self._reload_observable.register_listener(self)
        #
        self._activator.set_activation_fn(self._change_rule_active)
        #
        '''
        TODO: shouldn't put the content loader inside of here b/c it's hard to 
        disentangle the merger from the grammar manager 
        '''

    def register_rule(self, rule_class, details):
        """
        Takes a newly loaded copy of a rule (MappingRule or MergeRule),
        validates it, stores it for later instantiation, and adds it to the
        file tracking list.

        :param rule_class:
        :param details:
        :return:
        """
        class_name = rule_class.__name__

        # do not load or watch invalid rules
        invalidation = self._get_invalidation(rule_class, details)
        if invalidation is not None:
            printer.out(invalidation)
            return

        '''
        rule should be safe for loading at this point: register it
        but do not load here -- this method only registers
        '''
        managed_rule = ManagedRule(rule_class, details)
        self._managed_rules[class_name] = managed_rule
        # set up de/activation command
        self._activator.register_rule(managed_rule)
        # watch this file for future changes
        file_path = self._get_file_path(rule_class, details)
        self._reload_observable.register_watched_file(file_path)


    """
        THIS IS COMPLETELY UNUSED SO FAR --- moved to companion_rule_hook.py

        Both rules must be registered before registering the companion.
        self._companion_rules is {rule: [companions]}

        TODO: -- should this just happen in a config file???
    """
    def _register_companion_rule(self, rule_class, companion_rule_class):
        rule_class_name = rule_class.__name__
        companion_rule_class_name = companion_rule_class.__name__

        if rule_class_name in self._managed_rules and \
                companion_rule_class_name in self._managed_rules:
            companions_list = [] if rule_class_name not in self._companion_rules \
                else self._companion_rules[rule_class_name]
            companions_list.append(companion_rule_class_name)
            self._companion_rules[rule_class_name] = companions_list

    def _change_rule_active(self, class_name, active):
        """
        This is called by the GrammarActivator.

        :param class_name: str
        :param active: boolean
        :return:
        """
        # update config, save
        self._config.update(class_name, active)
        self._config.save()

        # load it
        self._load_rule(class_name, active)
        # run activation hooks
        self._hooks_runner.execute(RuleActivationEvent(class_name, active))

    def _load_rule(self, class_name, active):
        """
        Either creates a standalone Dragonfly rule or
        delegates to the CCRMerger to create the merged rule(s).

        The created rule is then loaded and its grammar saved in the GrammarContainer.
        If a rule of the same class name was already in the GrammarContainer, that
        rule and its grammar are destroyed first, by the GrammarContainer.

        :param class_name: str
        :param active: boolean
        :return:
        """

        managed_rule = self._managed_rules[class_name]

        ccrtype = managed_rule.details.declared_ccrtype
        ''' 
        This setting controls "RDP Mode". "RDP Mode" forces any rule 
        to load as a global ccr rule and ignore validation.
        '''
        if self._always_global_ccr_mode:
            ccrtype = CCRType.GLOBAL

        if ccrtype is not None:
            '''
            handle CCR:
            get all active ccr rules after de/activating one'''
            active_rule_class_names = self._config.get_active_rule_class_names()
            active_rules = [self._managed_rules[rcn] for rcn in active_rule_class_names]
            active_ccr_rules = [mr for mr in active_rules if mr.details.declared_ccrtype is not None]

            '''
            The merge may result in 1 to n+1 rules where n is the number of ccr app rules
            which are in the active rules list.
            For instance, if you have 1 app rule, you'll end up with two ccr rules. This is because
            the merger has to make the global one, plus an app rule with the app stuff plus all the
            global stuff.
            '''
            ccr_rules = self.merger.merge(active_ccr_rules)
            grammars = []
            for rule in ccr_rules:
                grammar = Grammar(name="ccr-" + GrammarManager._get_next_id())
                grammar.add_rule(rule)
                grammars.append(grammar)
            self._grammars_container.set_ccr(grammars)
            for grammar in grammars:
                grammar.load()
        else:
            if active:
                grammar = self._mapping_rule_maker.create_non_ccr_grammar(
                    managed_rule.get_rule_class(), managed_rule.get_details())
                self._grammars_container.set_non_ccr(self, managed_rule.get_rule_class_name(), grammar)
                grammar.load()
            else:
                self._grammars_container.set_non_ccr(self, managed_rule.get_rule_class_name(), None)

    def receive(self, file_path_changed):
        """
        This being called indicates that the file at file_path_changed has been updated
        and that it should be reloaded and potentially replace the old copy.

        DO NOT CALL THIS MANUALLY. Should only be called by the reload observable.

        :param file_path_changed: str
        :return:
        """

        module_name = GrammarManager._get_module_name_from_file_path(file_path_changed)
        rule_class, details = self._content_loader.idem_import_module(module_name, ContentType.GET_RULE)
        self.register_rule(rule_class, details)

        class_name = rule_class.__name__
        if class_name in self._config.get_active_rule_class_names():
            self._load_rule(class_name, True)

    def _get_invalidation(self, rule_class, details):
        """
        Attempts to find a reason to invalidate the rule. Return reason if can find one.
        :param rule_class:
        :param details: RuleDetails
        :return:
        """

        '''skip validations if forcing everything to be global ccr:'''
        if self._always_global_ccr_mode:
            return None

        class_name = rule_class.__name__

        '''validate details configuration before anything else'''
        details_invalidation = self._details_validator.validate_details(details)
        if details_invalidation is not None:
            return class_name + " rejected due to detail validation errors: " + details_invalidation

        '''attempt to instantiate the rule'''
        test_instance = None
        try:
            test_instance = rule_class()
        except: #ignore warnings on this line-- it's supposed to be broad
            return class_name + " rejected due to instantiation errors"

        '''if ccr, validate the rule'''
        if details.declared_ccrtype is not None:
            error = self._ccr_rules_validator.validate(test_instance, details.declared_ccrtype)
            if error is not None:
                return class_name + " rejected due to rule validation errors: " + error

        return None

    def load_activation_grammar(self):
        self._activator.construct_activation_rule()

    @staticmethod
    def _get_file_path(rule_class, details):
        if details.declared_ccrtype is not None:
            instance = rule_class()
            return instance.location
        else:
            return details.file_path

    @staticmethod
    def _get_module_name_from_file_path(file_path):
        """
        Used by receive(), converts full file path to module name.
        :param file_path: str
        :return: str
        """
        if file_path.startswith("__") or not file_path.endswith(".py"):
            raise NotAModuleError(file_path)
        return os.path.basename(file_path).replace(".py", "")

    @staticmethod
    def _get_next_id():
        """
        Returns a unique id for grammar names. Used to name new CCR grammars.
        :return: str
        """
        if not hasattr(GrammarManager._get_next_id, "id"):
            GrammarManager._get_next_id.id = 0
        GrammarManager._get_next_id.id += 1
        return str(GrammarManager._get_next_id.id)

