import os
import sys
import unittest

if os.path.dirname(os.path.dirname(os.path.abspath(__file__))) not in sys.path:
    sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dragonfly import get_engine

from castervoice.lib.ctrl.mgr.errors.guidance_rejection import GuidanceRejectionException
from castervoice.lib.util import guidance
from tests.test_util import settings_mocking


def reject_file_writing():
    raise GuidanceRejectionException()


def get_master_suite():
    return unittest.defaultTestLoader.discover(os.path.dirname(__file__))


def run_tests():
    get_engine("text")
    settings_mocking.prevent_initialize()
    # utilities_mocking.mock_toml_files() <-- Don't do this. Individual tests should be able to opt in.
    return unittest.TextTestRunner(verbosity=2).run(get_master_suite())


if __name__ == '__main__':
    guidance.offer = reject_file_writing
    result = run_tests()
    sys.exit(len(result.failures) + len(result.errors) + len(result.unexpectedSuccesses))
