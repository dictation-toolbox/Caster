import os
import unittest

from dragonfly.engines import _engines_by_name, get_engine

if not _engines_by_name:
    engine = get_engine("text")
    engine.connect()

def get_master_suite():
    return unittest.defaultTestLoader.discover(os.path.dirname(__file__))

def run_tests():
    unittest.TextTestRunner(verbosity=2).run(get_master_suite())

if __name__ == '__main__':
    run_tests()
