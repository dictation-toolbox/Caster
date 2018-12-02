#Embedded file name: C:\NatLink\NatLink\MacroSystem\caster\lib\tests\unit\mergerule.py
import unittest
from dragonfly.grammar.context import AppContext
from caster.apps.eclipse import EclipseCCR
from caster.ccr.java.java import Java
from caster.ccr.javascript.javascript import Javascript
from caster.ccr.python.python import Python
from caster.ccr.recording.alias import Alias
from caster.lib.dfplus.merge.mergerule import MergeRule


class TestMergeRule(unittest.TestCase):
    def test_name_generation(self):
        size = 10
        names = set()
        for i in range(0, size):
            names.add(MergeRule.get_merge_name())

        self.assertTrue(len(names) == size)

    def test_mcontext(self):
        python = Python()
        eclipse = EclipseCCR(mcontext=AppContext(executable='test'))
        self.assertIsNone(python.get_context())
        self.assertIsNotNone(eclipse.get_context())

    def test_id(self):
        python = Python()
        self.assertIsNotNone(python.ID)

    def test_compatibility(self):
        python_id = 1
        java_id = 2
        javascript_id = 3
        python = Python(ID=python_id)
        java = Java(ID=java_id)
        self.assertFalse(python.compatibility_check(java))
        self.assertTrue(python_id in java.compatible)
        self.assertFalse(java.compatible[python_id])
        self.assertEqual(len(python.compatible), 1)
        self.assertTrue(java_id in python.compatible)
        self.assertFalse(python.compatible[java_id])
        self.assertEqual(len(java.compatible), 1)
        javascript = Javascript(ID=javascript_id)
        self.assertFalse(java.compatibility_check(javascript))
        self.assertEqual(len(python.compatible), 1)
        self.assertEqual(len(javascript.compatible), 1)
        self.assertEqual(len(java.compatible), 2)

    def test_merge(self):
        python = Python()
        python_specs = len(python.mapping_actual().keys())
        java = Java()
        java_specs = len(java.mapping_actual().keys())
        vanilla = Alias(refresh=False)
        vanilla_specs = len(vanilla.mapping_actual().keys())
        _merged = python.merge(java)
        self.assertEqual(python_specs, len(python.mapping_actual().keys()))
        self.assertEqual(java_specs, len(java.mapping_actual().keys()))
        _merged = vanilla.merge(java)
        '''MergeRules get this @ merging:'''
        del _merged.mapping_actual()["display available commands"]
        self.assertEqual(vanilla_specs + java_specs, len(_merged.mapping_actual().keys()))
        self.assertEqual(vanilla_specs, len(vanilla.mapping_actual().keys()))
