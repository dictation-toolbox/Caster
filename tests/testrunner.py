import os
import sys
import unittest
from tests.test_util import settings_mocking


# from dragonfly.engines import _engines_by_name, get_engine
#
# if not _engines_by_name:
#     engine = get_engine("text")
#     engine.connect()

def get_master_suite():
    return unittest.defaultTestLoader.discover(os.path.dirname(__file__))


def run_tests():
    settings_mocking.prevent_initialize()
    return unittest.TextTestRunner(verbosity=2).run(get_master_suite())


if __name__ == '__main__':
    result = run_tests()
    sys.exit(len(result.failures) + len(result.errors) + len(result.unexpectedSuccesses))
