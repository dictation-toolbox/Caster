import os

from dragonfly import Grammar

from castervoice.lib import printer
from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.errors.not_a_module import NotAModuleError
from castervoice.lib.ctrl.mgr.loading.load.content_type import ContentType
from castervoice.lib.ctrl.mgr.managed_rule import ManagedRule
from castervoice.lib.merge.ccrmerging2.hooks.events.activation_event import RuleActivationEvent


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
                 always_global_ccr_mode,
                 ccr_toggle,
                 smrc):
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
        :param smrc: grants limited access to other parts of framework to selfmod rules- don't keep reference
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
        self._ccr_toggle = ccr_toggle

        # rules: (class name : ManagedRule}
        self._managed_rules = {}
        #
        self._reload_observable.register_listener(self)
        '''The passed method references below would be a good place to start splitting the GM apart.'''
        #
        self._activator.set_activation_fn(self._change_rule_active)
        #
        smrc.set_reload_fn(lambda rcn: self._activate_rule(rcn, True))
        #
        self._initial_activations_complete = False

    def initialize(self):
        if self._initial_activations_complete:
            return

        for rcn in self._config.get_active_rule_class_names():
            is_ccr = self._managed_rules[rcn].declared_ccrtype is not None
            if is_ccr and not self._ccr_toggle.is_active():
                continue
            self._activate_rule(rcn, True)

        self._initial_activations_complete = True

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
        self._reload_observable.register_watched_file(details.get_filepath())

    def _change_rule_active(self, class_name, active):
        """
        This is called by the GrammarActivator.

        :param class_name: str
        :param active: boolean
        :return:
        """
        # update config, save
        self._config.put(class_name, active)
        self._config.save()

        # load it
        self._activate_rule(class_name, active)
        # run activation hooks
        self._hooks_runner.execute(RuleActivationEvent(class_name, active))

    def _activate_rule(self, class_name, active):
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
        if self._always_global_ccr_mode and not managed_rule.details.rdp_mode_exclusion:
            ''' 
            This setting controls "RDP Mode". "RDP Mode" forces any rule 
            to load as a global ccr rule and ignore validation.
            '''
            ccrtype = CCRType.GLOBAL

        if ccrtype is not None:
            # if the global ccr toggle was off, activating a ccr rule turns it back on
            self._ccr_toggle.set_active(True)

            # handle CCR: get all active ccr rules after de/activating one
            active_rule_class_names = self._config.get_active_rule_class_names()
            active_mrs = [self._managed_rules[rcn] for rcn in active_rule_class_names]
            active_ccr_mrs = [mr for mr in active_mrs if mr.details.declared_ccrtype is not None]

            '''
            The merge may result in 1 to n+1 rules where n is the number of ccr app rules
            which are in the active rules list.
            For instance, if you have 1 app rule, you'll end up with two ccr rules. This is because
            the merger has to make the global one, plus an app rule with the app stuff plus all the
            global stuff.
            '''
            ccr_rules_and_contexts = self.merger.merge(active_ccr_mrs)
            grammars = []
            for rule_and_context in ccr_rules_and_contexts:
                rule = rule_and_context[0]
                context = rule_and_context[1]
                grammar = Grammar(name="ccr-" + GrammarManager._get_next_id(), context=context)
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
            self._activate_rule(class_name, True)

    def _get_invalidation(self, rule_class, details):
        """
        Attempts to find a reason to invalidate the rule. Return reason if can find one.
        :param rule_class:
        :param details: RuleDetails
        :return:
        """

        '''skip validations if forcing everything to be global ccr:'''
        if self._always_global_ccr_mode and not details.rdp_mode_exclusion:
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
        except:  # ignore warnings on this line-- it's supposed to be broad
            return class_name + " rejected due to instantiation errors"

        '''if ccr, validate the rule'''
        if details.declared_ccrtype is not None:
            error = self._ccr_rules_validator.validate(test_instance, details.declared_ccrtype)
            if error is not None:
                return class_name + " rejected due to rule validation errors: " + error

        return None

    def load_activation_grammar(self):
        self._activator.construct_activation_rule()

    def set_ccr_active(self, active):
        self._ccr_toggle.set_active(active)
        if not self._ccr_toggle.is_active():
            self._grammars_container.wipe_ccr()
        else:
            self._change_rule_active("Numbers", True)

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

