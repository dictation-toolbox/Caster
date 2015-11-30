import unittest

from caster.lib.tests.unit import merger, mergerule, filter, state, stack


def run_tests():
    test_cases = [merger.TestMerger,
                  mergerule.TestMergeRule,
                  filter.TestFilterNonBootTime, 
                  stack.TestStack, 
                  state.TestState]
    master_suite = unittest.TestSuite()
    
    for test_case in test_cases:
        suite = unittest.TestLoader().loadTestsFromTestCase(test_case)
        master_suite.addTests(suite)
    
    unittest.TextTestRunner(verbosity=2).run(master_suite)


