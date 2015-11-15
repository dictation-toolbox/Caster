import unittest

from caster.lib.tests.integration import output
from caster.lib.tests.integration import stack
from caster.lib.tests.integration.testutils import get_notepad, notepad_message, \
    get_output


def run_tests():
    '''set up'''
    get_notepad()
    notepad_message("\nStarting Tests")
    notepad_message("\nPlease Do Not Close Notepad")
    for i in range(0, 3): notepad_message("\n.", 25)
    get_output()
    
    test_cases = [output.TestOutput, stack.TestOutput]
    master_suite = unittest.TestSuite()
#     result = unittest.result.TestResult() 
    
    for test_case in test_cases:
        suite = unittest.TestLoader().loadTestsFromTestCase(test_case)
        master_suite.addTests(suite)
    
#     master_suite.run(result)
    unittest.TextTestRunner(verbosity=2).run(master_suite)
#     print(result.buffer)
#     print(result.wasSuccessful())


