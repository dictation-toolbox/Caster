import os, traceback

from dragonfly import Grammar

from castervoice.lib import printer
from castervoice.lib.ctrl.mgr.errors.invalid_companion_configuration_error import InvalidCompanionConfigurationError
from castervoice.lib.ctrl.mgr.errors.not_a_module import NotAModuleError
from castervoice.lib.ctrl.mgr.loading.load.content_type import ContentType
from castervoice.lib.ctrl.mgr.managed_rule import ManagedRule
from castervoice.lib.ctrl.mgr.rules_enabled_diff import RulesEnabledDiff
from castervoice.lib.merge.ccrmerging2.hooks.events.activation_event import RuleActivationEvent
from castervoice.lib.merge.ccrmerging2.sorting.config_ruleset_sorter import ConfigBasedRuleSetSorter


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
        for rcn in self._config.get_enabled_rcns_ordered():
            if rcn in loaded_enabled_rcns:
                rd = self._managed_rules[rcn].get_details()
                if rd.declared_ccrtype is None:
                    self._delegate_enable_rule(rcn, True)
            else:
                msg = "Skipping rule {} because it is enabled but not loaded."
                printer.out(msg.format(rcn))
        if self._ccr_toggle.is_active():
            self._remerge_ccr_rules()

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

    def _change_rule_enabled(self, class_name, enabled, companions=True):
        """
        This is called by the GrammarActivator. The necessity of this function
        means something is designed wrong. Correct this in the future.

        :param class_name: str
        :param enabled: boolean
        :param companions: (boolean) whether to load companion rules of the 'class_name' rule
        :return:
        """
        # update config, save
        self._config.put(class_name, enabled)
        self._config.save()

        # load it
        enabled_diff = self._delegate_enable_rule(class_name, enabled)
        # run activation hooks
        self._hooks_runner.execute(RuleActivationEvent(class_name, enabled))


        '''
        Problems:
        1. Can't just do companion rules here after the normal process b/c don't have enough information.
            If there were no KOs, it would be fine. But if something gets KO'd, its companions should too.
            Can't just cycle through rules and remove companions of rules not activated though, b/c user could enable
            companion rules independently of host rules.
        2. Save after merge is broken. It always wipes all non-ccr rules b/c it is unaware of non-ccr-rules entirely.
        
        Solutions:
        1. `_delegate_enable_rule` needs to return a diff of what got added/removed -- then can handle companions here
            - this is messily implemented on the main branch -- salvage what you can and start clean here
        2. The diff handles this problem too.
            - prevent companion rules from being CCR to avoid that mess (THIS IS THE ONLY CHANGE ON THIS BRANCH);
            - then, calling `_change_rule_active` for each companion, removes first, then adds, should cause the correct
              rules to get written to rules.toml
            - MUST also remove the `_save_after_remerge` method-- 
                - ideally we want to pass the enabled_ordered to the merger instead of letting it use the config
                    - this lets us not need to save before calling `remerge`, I THINK, check this
                - either way, we want to save according to the diff, not via the current failing `_save_after_remerge` method 
        
        Roadmap:
        DO THIS STUFF IN CLEAN STEPS, DISTINCT COMMITS:
        X 1. Save CCR companion prevention, and these comments
        X 2. Take away the merger's access to the config get_ordered_enabled function
        X 3. Bring the diff here.
        4. Get rid of save after merge -- it just doesn't work.
        5. Add a diff-based save which only happens AFTER companions handling.
        6. Remove pre-delegation save.
        X 7. Rename `_change_rule_active` to `_change_rule_enabled`.
        8. See about pointing everything at `_change_rule_enabled` which is currently pointed to `delegate_rule_enabled`
            -> "everything" is 3 functions out of the 7 which point at both functions combined. This makes
            `_change_rule_enabled` the center of the GM, rather than having two centers. 
        9. Remove these comments.
        '''


        if companions:
            self._handle_companion_rules(class_name, enabled)

    # def _rewrite_config_file(self, prev_enabled_rcns, diff):
    #     """
    #     Possibly save results after a merge since KOs may have occurred.
    #     This save does not take companion rules into account. That happens later.
    #
    #     :param prev_enabled_rcns:
    #     :param diff:
    #     :return:
    #     """
    #     if len(diff.newly_enabled) + len(diff.newly_disabled) > 0:
    #         result = list(prev_enabled_rcns)
    #
    #         for rcn in diff.newly_disabled:
    #             result.remove(rcn)
    #         result.extend(diff.newly_enabled)
    #
    #         self._config.replace_enabled(result)
    #         self._config.save()

    def _handle_companion_rules(self, class_name, enabled):
        for companion_rcn in self._companion_config.get_companions(class_name):
            if companion_rcn in self._managed_rules:
                mr = self._managed_rules[companion_rcn]
                is_ccr = mr.get_details.get_details().declared_ccrtype is not None
                if is_ccr:
                    raise InvalidCompanionConfigurationError(companion_rcn)

                self._change_rule_enabled(companion_rcn, enabled, False)

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
            return self._remerge_ccr_rules()

    def _remerge_ccr_rules(self):
        """
        :return: RulesEnabledDiff
        """
        # if the global ccr toggle was off, activating a ccr rule turns it back on
        self._ccr_toggle.set_active(True)

        # handle CCR: get all active ccr rules after de/activating one
        loaded_enabled_rcns = set(self._managed_rules.keys())
        # TODO: the next line relies on the fact that the added rule gets saved previously to this -- change that
        active_rule_class_names = [rcn for rcn in self._config.get_enabled_rcns_ordered()
                                   if rcn in loaded_enabled_rcns]
        active_mrs = [self._managed_rules[rcn] for rcn in active_rule_class_names]
        active_ccr_mrs = [mr for mr in active_mrs if mr.get_details().declared_ccrtype is not None]

        '''
        The merge may result in 1 to n+1 rules where n is the number of ccr app rules
        which are in the active rules list.
        For instance, if you have 1 app rule, you'll end up with two ccr rules. This is because
        the merger has to make the global one, plus an app rule with the app stuff plus all the
        global stuff.
        '''
        sorter = ConfigBasedRuleSetSorter(self._config.get_enabled_rcns_ordered())
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
        self._save_after_remerge(
            [mr.get_rule_class_name() for mr in active_ccr_mrs],
            merge_result.all_rule_class_names
        )

        return merge_result.rules_enabled_diff

    def _save_after_remerge(self, pre_merge_rcns, post_merge_rcns):
        """possibly save results after a merge since KOs may have occurred"""
        if pre_merge_rcns != post_merge_rcns:
            self._config.replace_enabled(post_merge_rcns)
            self._config.save()

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
        module_name = GrammarManager._get_module_name_from_file_path(file_path_changed)
        rule_class, details = self._content_loader.idem_import_module(module_name, ContentType.GET_RULE)
        # re-register:
        self.register_rule(rule_class, details)

        class_name = rule_class.__name__
        if class_name in self._config.get_enabled_rcns_ordered():
            self._delegate_enable_rule(class_name, True)

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
    def _get_next_id():
        """
        Returns a unique id for grammar names. Used to name new CCR grammars.
        :return: str
        """
        if not hasattr(GrammarManager._get_next_id, "id"):
            GrammarManager._get_next_id.id = 0
        GrammarManager._get_next_id.id += 1
        return str(GrammarManager._get_next_id.id)

