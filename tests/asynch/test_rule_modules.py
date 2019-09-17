from castervoice.asynch.hmc_rules import hmc_settings_rule, hmc_launch_rule, hmc_history_rule, hmc_directory_rule, \
    hmc_confirm_rule, hmc_base_rule
from castervoice.asynch.sikuli import sikuli_gen_rule, sikuli_mgmt_rule
from tests.test_util.modules_testing import ModulesTestCase


class AsynchModulesTestCase(ModulesTestCase):
    def test_modules_get_rule_contents(self):
        modules_to_test = [hmc_base_rule, hmc_confirm_rule, hmc_directory_rule,
                           hmc_history_rule, hmc_launch_rule, hmc_settings_rule,
                           sikuli_gen_rule, sikuli_mgmt_rule]
        self._test_modules_get_rule_contents(modules_to_test)
