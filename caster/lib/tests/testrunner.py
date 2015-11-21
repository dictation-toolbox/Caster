import unittest

from caster.lib.tests.unit import merger, mergerule, filter


# from caster.lib.tests.integration import output
# from caster.lib.tests.integration import stack
# from caster.lib.tests.integration.testutils import get_notepad, notepad_message, \
#     get_output
def run_tests():
    '''set up'''
#     get_notepad()
#     notepad_message("\nStarting Tests")
#     notepad_message("\nPlease Do Not Close Notepad")
#     for i in range(0, 3): notepad_message("\n.", 25)
#     get_output()
    
    test_cases = [merger.TestMerger, 
                  mergerule.TestMergeRule, 
                  filter.TestFilterNonBootTime]
    master_suite = unittest.TestSuite()
    
    for test_case in test_cases:
        suite = unittest.TestLoader().loadTestsFromTestCase(test_case)
        master_suite.addTests(suite)
    
    unittest.TextTestRunner(verbosity=2).run(master_suite)


