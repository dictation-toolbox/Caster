from unittest import TestCase

from castervoice.rules.core.alphabet_rules.alphabet import Alphabet
from castervoice.rules.core.navigation_rules.nav import Navigation
from castervoice.lib.merge.ccrmerging2.sorting.config_ruleset_sorter import ConfigBasedRuleSetSorter
from castervoice.rules.core.utility_rules.caster_rule import CasterRule

class TestConfigBasedRuleSetSorter(TestCase):
    def test_sort_rules(self):
        sorter = ConfigBasedRuleSetSorter(["CasterRule", "Navigation", "Alphabet"])
        a = Alphabet()
        c = CasterRule()
        n = Navigation()
        rules = [a, c, n]
        sorted_rules = sorter.sort_rules(rules)
        self.assertEqual(0, sorted_rules.index(c))
        self.assertEqual(1, sorted_rules.index(n))
        self.assertEqual(2, sorted_rules.index(a))
