from unittest import TestCase
import importlib
from castervoice.lib.ctrl.mgr.loading.load.modules_access import SysModulesAccessor


class TestSysModulesAccessor(TestCase):

    def setUp(self):
        self.sys_modules_accessor = SysModulesAccessor()

    def test_has_module(self):
        self.assertTrue(self.sys_modules_accessor.has_module("importlib"))

    def test_doesnt_have_unknown_module(self):
        self.assertFalse(self.sys_modules_accessor.has_module("asdf1234"))

    def test_get_module(self):
        self.assertEqual(importlib, self.sys_modules_accessor.get_module("importlib"))

    def test_has_fully_qualified(self):
        self.assertTrue(self.sys_modules_accessor.has_module("castervoice.lib.ctrl.mgr.loading.load.modules_access"))

    def test_doesnt_have_non_fully_qualified(self):
        self.assertFalse(self.sys_modules_accessor.has_module("modules_access"))
