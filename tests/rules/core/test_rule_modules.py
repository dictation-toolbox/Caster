from tests.test_util.modules_testing import ModulesTestCase


class CoreModulesTestCase(ModulesTestCase):
    def _rule_modules(self):
        from castervoice.rules.core.text_manipulation_rules import text_manipulation
        from castervoice.rules.core.numbers_rules import numeric
        from castervoice.rules.core.keyboard_rules import keyboard
        from castervoice.rules.core.navigation_rules import nav
        from castervoice.rules.core.navigation_rules import nav2
        from castervoice.rules.core.navigation_rules import window_mgmt_rule
        from castervoice.rules.core.alphabet_rules import alphabet
        from castervoice.rules.core.punctuation_rules import punctuation
        from castervoice.rules.core.utility_rules import caster_rule
        from castervoice.rules.core.utility_rules import hardware_rule
        from castervoice.rules.core.utility_rules import mouse_alts_rules
        from castervoice.rules.core.engine_manager_rules import mic_rules

        return [alphabet, nav, nav2, window_mgmt_rule, numeric, keyboard, punctuation,
                text_manipulation, caster_rule,
                hardware_rule, mouse_alts_rules, mic_rules]
