from unittest import TestCase

from mock import Mock

from castervoice.lib.ctrl.mgr.loading.load.content_request_generator import ContentRequestGenerator
from castervoice.lib.ctrl.mgr.loading.load.content_type import ContentType


class TestContentRequestGenerator(TestCase):
    """
    Tests that irrelevant files are skipped and that the
    module info is retrieved.
    """

    def setUp(self):
        self.crg = ContentRequestGenerator()
        self.crg._walk = Mock()
        self.crg._get_file_lines = Mock()

    def test_get_rule(self):
        self.crg._walk.side_effect = [[("/some/path", [], ["__init__.py", "something.pyc"]),
                                       ("/relevant/path", [], ["some_rule.py"])]]
        self.crg._get_file_lines.side_effect = [["from stuff import *",
                                                 "class Abc(MappingRule):",
                                                 "  mapping={\"test action\":NullAction()}",
                                                 "def get_rule():",
                                                 "  return Abc, RuleDetails(name=\"test\")"]]
        self._do_assertions(ContentType.GET_RULE, "some_rule", "Abc")

    def test_get_transformer(self):
        self.crg._walk.side_effect = [[("/some/path", [], ["__init__.py", "something.pyc"]),
                                       ("/relevant/path", [], ["some_transformer.py"])]]
        self.crg._get_file_lines.side_effect = [["from stuff import *",
                                                 "class XTransformer(BaseRuleTransformer):pass",
                                                 "def get_transformer():",
                                                 "  return XTransformer"]]
        self._do_assertions(ContentType.GET_TRANSFORMER, "some_transformer")

    def test_get_hook(self):
        self.crg._walk.side_effect = [[("/some/path", [], ["__init__.py", "something.pyc"]),
                                       ("/relevant/path", [], ["some_hook.py"])]]
        self.crg._get_file_lines.side_effect = [["from stuff import *",
                                                 "class ZHook(BaseHook):pass",
                                                 "def get_hook():",
                                                 "  return ZHook"]]
        self._do_assertions(ContentType.GET_HOOK, "some_hook")

    def _do_assertions(self, content_type, module_name, class_name=None):
        results = self.crg.get_all_content_modules("test_dir")
        self.assertEqual(1, len(results))
        req = results[0]
        self.assertEqual(content_type, req.content_type)
        self.assertEqual(class_name, req.content_class_name)
        self.assertEqual("/relevant/path", req.directory)
        self.assertEqual(module_name, req.module_name)
