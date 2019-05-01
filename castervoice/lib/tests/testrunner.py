import unittest
from dragonfly.engines import _engines_by_name, get_engine
if not _engines_by_name:
    engine = get_engine("text")
    engine.connect()
from castervoice.lib.tests.unit import merger, mergerule, filter, state, stack, node, textformat


def get_master_suite():
    test_cases = [
        merger.TestMerger, mergerule.TestMergeRule, filter.TestFilterNonBootTime,
        stack.TestStack, state.TestState, node.TestNode, node.TestNodeRule, textformat.TestTextFormat
    ]
    master_suite = unittest.TestSuite()

    for test_case in test_cases:
        suite = unittest.TestLoader().loadTestsFromTestCase(test_case)
        master_suite.addTests(suite)

    return master_suite


def run_tests():
    
    unittest.TextTestRunner(verbosity=2).run(get_master_suite())

if __name__ == '__main__':
    run_tests()