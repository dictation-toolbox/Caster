from castervoice.lib.tests.mocks import (eclipse_context, EclipseCCR, Text, Bash,
        Java, Python)
from castervoice.lib.dfplus.merge.ccrmerger import CCRMerger
from castervoice.lib.dfplus.merge.filter import (make_filter, there_is_spec_overlap,
        incoming_gets_priority)
from castervoice.lib.dfplus.merge.mergepair import MergeInf
from castervoice.lib.tests.unit.nexus import TestNexus


class TestFilterFunctions(TestNexus):

    def setUp(self):
        TestNexus.setUp(self)
        self.nexus.merger.add_global_rule(Python())
        self._python2 = "Python2"
        self.nexus.merger.add_global_rule(Python(name=self._python2))
        self.nexus.merger.add_global_rule(Java())
        self.nexus.merger.add_global_rule(Bash())
        self.nexus.merger.add_app_rule(EclipseCCR(), eclipse_context)
        self.nexus.merger.update_config()
        self.set_global = self.nexus.merger.global_rule_changer()
        self.set_selfmod = self.nexus.merger.selfmod_rule_changer()

    def tearDown(self):
        self.nexus.merger.wipe()
        TestNexus.tearDown(self)


class TestFilterNonBootTime(TestFilterFunctions):
    def setUp(self):
        TestFilterFunctions.setUp(self)
        self.nexus.merger.merge(MergeInf.BOOT)
        self.set_global("Python", True, True)

    def test_runtime_global_spec_replace(self):
        ff = make_filter(lambda mp: incoming_gets_priority(mp),
                         lambda mp: there_is_spec_overlap(mp), MergeInf.RUN,
                         MergeInf.GLOBAL)
        self.nexus.merger.add_filter(ff)
        python = Python()
        '''attempt to emerge in an identical rule with a filter that allows it:'''
        self.set_global(self._python2, True, True)
        self.assertTrue(self.nexus.merger._config[CCRMerger._GLOBAL]["Python"])
        self.assertTrue(self.nexus.merger._config[CCRMerger._GLOBAL][self._python2])
        '''this is minus one because of the "show available commands" command: '''
        merged_specs = len(self.nexus.merger._base_global.mapping_actual().keys()) - 1
        python_specs = len(python.mapping_actual().keys())
        self.assertEqual(merged_specs, python_specs)
        '''make sure were not deleting from the Python class mapping: '''
        self.assertNotEqual(python_specs, 0)
        '''clear filters, clean up'''
        self.nexus.merger._filters = []
        self.set_global(self._python2, False, True)

    def test_runtime_global_action_replace(self):
        def replace_if_action(mp):
            if mp.rule1 is not None:
                mp.rule1.mapping_actual()["iffae"] = Text("test")
            mp.rule2.mapping_actual()["iffae"] = Text("test")

        ff = make_filter(lambda mp: replace_if_action(mp), None, MergeInf.RUN,
                         MergeInf.GLOBAL)
        self.nexus.merger.add_filter(ff)

        self.set_global("Java", True, True)
        self.set_global("Python", True, True)

        self.assertTrue(
            isinstance(self.nexus.merger._base_global.mapping_actual()["iffae"],
                       Text))

        self.nexus.merger._filters = []

        self.set_global("Java", True, True)
        self.set_global("Python", True, True)
        '''make sure originals weren't changed'''
        self.assertFalse(
            isinstance(self.nexus.merger._base_global.mapping_actual()["iffae"],
                       Text))
