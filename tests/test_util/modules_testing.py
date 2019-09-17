from unittest import TestCase

from dragonfly import MappingRule

from castervoice.lib.ctrl.mgr.rule_details import RuleDetails


class ModulesTestCase(TestCase):
    def _test_modules_get_rule_contents(self, modules_to_test):
        for module in modules_to_test:
            content = module.get_rule()
            self.assertTrue(issubclass(content[0], MappingRule),
                            "MappingRule check failed: {}".format(str(content[0])))
            self.assertTrue(isinstance(content[1], RuleDetails),
                            "RuleDetails check failed: {}".format(str(content[1])))