import os
import traceback

from dragonfly import Grammar

from castervoice.lib import printer
from castervoice.lib.ctrl.mgr.errors.invalid_companion_configuration_error import InvalidCompanionConfigurationError
from castervoice.lib.ctrl.mgr.errors.not_a_module import NotAModuleError
from castervoice.lib.ctrl.mgr.loading.load.content_request import ContentRequest
from castervoice.lib.ctrl.mgr.loading.load.content_type import ContentType
from castervoice.lib.ctrl.mgr.managed_rule import ManagedRule
from castervoice.lib.ctrl.mgr.rule_formatter import _set_rdescripts
from castervoice.lib.ctrl.mgr.rules_enabled_diff import RulesEnabledDiff
from castervoice.lib.merge.ccrmerging2.hooks.events.activation_event import RuleActivationEvent
from castervoice.lib.merge.ccrmerging2.hooks.events.on_error_event import OnErrorEvent
from castervoice.lib.merge.ccrmerging2.hooks.events.rules_loaded_event import RulesLoadedEvent
from castervoice.lib.merge.ccrmerging2.sorting.config_ruleset_sorter import ConfigBasedRuleSetSorter
from castervoice.lib.util.ordered_set import OrderedSet


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
                 ccr_toggle,
                 smrc,
                 t_runner,
                 companion_config,
                 combo_validator):
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
        :param smrc: grants limited access to other parts of framework to selfmod rules- don't keep reference
        :param t_runner: a reference is kept to it so can instantly activate its activation rule
        :param companion_config: a config which controls which rules can be enabled/disabled instantly by other rules
        :param combo_validator: validates all (ccr/non-ccr) rule+detail combinations
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
        self._ccr_toggle = ccr_toggle
        self._transformers_runner = t_runner
        self._companion_config = companion_config
        self._combo_validator = combo_validator

        # rules: (class name : ManagedRule}
        self._managed_rules = {}
        #
        self._reload_observable.register_listener(self)
        '''The passed method references below would be a good place to start splitting the GM apart.'''
        #
        self._activator.set_activation_fn(lambda rcn, active: self._change_rule_enabled(rcn, active))
        #
        smrc.set_reload_fn(lambda rcn: self._delegate_enable_rule(rcn, True))
        #
        self._initial_activations_complete = False

    def initialize(self):
        if self._initial_activations_complete:
            return

        loaded_enabled_rcns = set(self._managed_rules.keys())
        enabled_ordered_rcns = self._config.get_enabled_rcns_ordered()
        for rcn in enabled_ordered_rcns:
            if rcn in loaded_enabled_rcns:
                rd = self._managed_rules[rcn].get_details()
                if rd.declared_ccrtype is None:
                    self._delegate_enable_rule(rcn, True)
            else:
                msg = "Skipping rule {} because it is enabled but not loaded."
                printer.out(msg.format(rcn))
        if self._ccr_toggle.is_active():
            self._remerge_ccr_rules(enabled_ordered_rcns)

        is_timer_based_reload_observable = hasattr(self._reload_observable, "start")
        if is_timer_based_reload_observable:
            self._reload_observable.start()

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

        _set_rdescripts(rule_class.mapping, class_name)
        '''
        rule should be safe for loading at this point: register it
        but do not load here -- this method only registers
        '''
        managed_rule = ManagedRule(rule_class, details)
        self._managed_rules[class_name] = managed_rule
        # set up de/activation command
        self._activator.register_rule(managed_rule)
        # watch this file for future changes
        if not details.watch_exclusion:
            self._reload_observable.register_watched_file(details.get_filepath())

    def _change_rule_enabled(self, class_name, enabled, tail=True):
        """
        This is called by the GrammarActivator. The necessity of this function
        means something is designed wrong. Correct this in the future.

        :param class_name: str
        :param enabled: boolean
        :param tail: (boolean) whether this is the tail call, since this fn is recursive
        :return:
        """

        # load it
        enabled_diff = self._delegate_enable_rule(class_name, enabled)
        # run activation hooks
        self._hooks_runner.execute(RuleActivationEvent(class_name, enabled))

        if tail:
            enabled_diff = self._handle_companion_rules(enabled_diff)
            self._rewrite_config_file(enabled_diff)

        '''
        Roadmap:
        8. See about pointing everything at `_change_rule_enabled` which is currently pointed to `delegate_rule_enabled`
            -> "everything" is 3 functions out of the 7 which point at both functions combined. This makes
            `_change_rule_enabled` the center of the GM, rather than having two centers.
        '''

    def _rewrite_config_file(self, enabled_diff):
        """
        :param enabled_diff:
        :return:
        """
        if len(enabled_diff.newly_enabled) + len(enabled_diff.newly_disabled) > 0:
            result = OrderedSet(self._config.get_enabled_rcns_ordered())
            result.remove_all(enabled_diff.newly_disabled)
            result.add_all(enabled_diff.newly_enabled)
            self._config.replace_enabled(result.to_list())
            self._config.save()

    def _handle_companion_rules(self, enabled_diff):
        newly_enabled = list()
        newly_disabled = set()
        diff = [(rcn, True) for rcn in enabled_diff.newly_enabled] + \
               [(rcn, False) for rcn in enabled_diff.newly_disabled]
        for difference in diff:
            rcn = difference[0]
            enabled = difference[1]
            for companion_rcn in self._companion_config.get_companions(rcn):
                if companion_rcn in self._managed_rules:
                    mr = self._managed_rules[companion_rcn]
                    is_ccr = mr.get_details().declared_ccrtype is not None
                    if is_ccr:
                        raise InvalidCompanionConfigurationError(companion_rcn)

                    self._change_rule_enabled(companion_rcn, enabled, False)
                    if enabled:
                        newly_enabled.append(companion_rcn)
                    else:
                        newly_disabled.add(companion_rcn)
                else:
                    invalid_msg = "Invalid companion rule (not loaded): {}"
                    printer.out(invalid_msg.format(companion_rcn))

        return RulesEnabledDiff(enabled_diff.newly_enabled + newly_enabled,
                                enabled_diff.newly_disabled | newly_disabled)

    def _delegate_enable_rule(self, class_name, enabled):
        """
        Either creates a standalone Dragonfly rule or
        delegates to the CCRMerger to create the merged rule(s).

        The created rule is then loaded and its grammar saved in the GrammarContainer.
        If a rule of the same class name was already in the GrammarContainer, that
        rule and its grammar are destroyed first, by the GrammarContainer.

        :param class_name: str
        :param enabled: boolean
        :return: RulesEnabledDiff
        """

        managed_rule = self._managed_rules[class_name]

        if managed_rule.get_details().declared_ccrtype is None:
            return self._enable_non_ccr_rule(managed_rule, enabled)
        else:
            rcn = managed_rule.get_rule_class_name()
            enabled_rules = OrderedSet(self._config.get_enabled_rcns_ordered())
            enabled_rules.update(rcn, enabled)
            enabled_diff = self._remerge_ccr_rules(enabled_rules.to_list())
            place = enabled_diff.newly_enabled.append if enabled else enabled_diff.newly_disabled.add
            place(rcn)
            return enabled_diff

    def _remerge_ccr_rules(self, enabled_rcns):
        """
        :return: RulesEnabledDiff
        """
        # if the global ccr toggle was off, activating a ccr rule turns it back on
        self._ccr_toggle.set_active(True)

        # handle CCR: get all active ccr rules after de/activating one
        loaded_enabled_rcns = set(self._managed_rules.keys())
        active_rule_class_names = [rcn for rcn in enabled_rcns if rcn in loaded_enabled_rcns]
        active_mrs = [self._managed_rules[rcn] for rcn in active_rule_class_names]
        active_ccr_mrs = [mr for mr in active_mrs if mr.get_details().declared_ccrtype is not None]
        self._hooks_runner.execute(RulesLoadedEvent(rules=active_ccr_mrs))
        '''
        The merge may result in 1 to n+1 rules where n is the number of ccr app rules
        which are in the active rules list.
        For instance, if you have 1 app rule, you'll end up with two ccr rules. This is because
        the merger has to make the global one, plus an app rule with the app stuff plus all the
        global stuff.
        '''
        sorter = ConfigBasedRuleSetSorter(enabled_rcns)
        merge_result = self._merger.merge_rules(active_ccr_mrs, sorter)
        grammars = []
        for rule_and_context in merge_result.ccr_rules_and_contexts:
            rule = rule_and_context[0]
            context = rule_and_context[1]
            grammar = Grammar(name="ccr-" + GrammarManager._get_next_id(), context=context)
            grammar.add_rule(rule)
            grammars.append(grammar)
        self._grammars_container.set_ccr(grammars)
        for grammar in grammars:
            grammar.load()

        return merge_result.rules_enabled_diff

    def _enable_non_ccr_rule(self, managed_rule, enabled):
        """
        :param managed_rule:
        :param enabled:
        :return: RulesEnabledDiff
        """
        rcn = managed_rule.get_rule_class_name()
        if enabled:
            grammar = self._mapping_rule_maker.create_non_ccr_grammar(managed_rule)
            self._grammars_container.set_non_ccr(rcn, grammar)
            grammar.load()
            return RulesEnabledDiff([rcn], frozenset())
        else:
            self._grammars_container.set_non_ccr(rcn, None)
            return RulesEnabledDiff(frozenset(), [rcn])

    def receive(self, file_path_changed):
        """
        This being called indicates that the file at file_path_changed has been updated
        and that it should be reloaded and potentially replace the old copy.

        DO NOT CALL THIS MANUALLY. Should only be called by the reload observable.

        :param file_path_changed: str
        :return:
        """
        try:
            module_dir = GrammarManager._get_module_package(file_path_changed)
            module_name = GrammarManager._get_module_name_from_file_path(file_path_changed)
            # request class name not needed here -- only needed on initial load
            request = ContentRequest(ContentType.GET_RULE, module_dir, module_name, None)
            rule_class, details = self._content_loader.idem_import_module(request)
            # re-register:
            self.register_rule(rule_class, details)

            class_name = rule_class.__name__
            if class_name in self._config.get_enabled_rcns_ordered():
                self._delegate_enable_rule(class_name, True)
        except Exception as error:
            printer.out('Grammar Manager: {} - See error message above'.format(error))
            self._hooks_runner.execute(OnErrorEvent())

    def _get_invalidation(self, rule_class, details):
        """
        Attempts to find a reason to invalidate the rule. Return reason if can find one.
        :param rule_class:
        :param details: RuleDetails
        :return:
        """

        class_name = rule_class.__name__

        '''validate details configuration before anything else'''
        details_invalidation = self._details_validator.validate_details(details)
        if details_invalidation is not None:
            return "{} rejected due to detail validation errors: {}".format(class_name, details_invalidation)

        '''attempt to instantiate the rule'''
        test_instance = None
        try:
            test_instance = rule_class()
        except:  # ignore warnings on this line-- it's supposed to be broad
            traceback.print_exc()
            return "{} rejected due to instantiation errors".format(class_name)

        '''if ccr, validate the rule'''
        if details.declared_ccrtype is not None:
            error = self._ccr_rules_validator.validate_rule(test_instance, details.declared_ccrtype)
            if error is not None:
                return "{} rejected due to rule validation errors: {}".format(class_name, error)

        '''do combo validations'''
        combo_invalidation = self._combo_validator.validate(test_instance, details)
        if combo_invalidation is not None:
            return "{} rejected due to rule/details combination errors: {}".format(class_name, combo_invalidation)

        return None

    def load_activation_grammars(self):
        """
        Caster core mechanisms should follow the same process as everything
        else. This should lead to much greater consistency, but also the
        ability to shut off core Caster mechanisms more easily if desired.
        """
        rules = [self._activator.construct_activation_rule(),
                 self._hooks_runner.construct_activation_rule(),
                 self._transformers_runner.construct_activation_rule()]
        rules = [rule for rule in rules if len(rule[0].mapping) > 0]  # there might not be *any* transformers/hooks
        if hasattr(self._reload_observable, "get_loadable"):
            rules.append(self._reload_observable.get_loadable())

        for rc, d in rules:
            self.register_rule(rc, d)
            self._change_rule_enabled(rc.__name__, True)

    def set_ccr_active(self, active):
        self._ccr_toggle.set_active(active)
        if not self._ccr_toggle.is_active():
            self._grammars_container.wipe_ccr()
        else:
            self._change_rule_enabled("Numbers", True)

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
    def _get_module_package(module_path):
        return module_path[:module_path.rindex(os.sep)]

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
