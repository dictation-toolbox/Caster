from unittest import TestCase

from castervoice.lib.ctrl.mgr.rule_details import RuleDetails


class TestRuleDetails(TestCase):

    def test_path_detection(self):
        """
        RuleDetails detects the name of the module it was instantiated
        in. This saves the user the trouble of specifying (and updating)
        module names manually.
        """
        rd = RuleDetails()
        self.assertTrue("test_ruleDetails.py" in rd.get_filepath())
