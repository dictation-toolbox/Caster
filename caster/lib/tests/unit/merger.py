from dragonfly.actions.action_key import Key
from dragonfly.grammar.rule_mapping import MappingRule

from caster.apps import eclipse
from caster.apps.eclipse import EclipseCCR
from caster.lib.ccr.bash.bash import Bash
from caster.lib.ccr.java.java import Java
from caster.lib.ccr.python.python import Python
from caster.lib.ccr.recording.alias import ChainAlias
from caster.lib.ccr.standard import SymbolSpecs
from caster.lib.dfplus.merge.ccrmerger import CCRMerger
from caster.lib.dfplus.merge.mergepair import MergeInf
from caster.lib.tests.unit.state import TestNexus


def demo_filter(_):
    ''' delete conflicting specs out of the base rule '''
    if _.type == MergeInf.GLOBAL and _.time != MergeInf.BOOT \
    and _.rule1 is not None and _.rule2.get_pronunciation()=="Bash":
        for spec in _.rule1.mapping_actual().keys():
            if spec in _.rule2.mapping_actual().keys():
                del _.rule1.mapping_actual()[spec]
        _.check_compatibility = False


class DemoMappingRule(MappingRule):
    mapping = {
        "test": Key("a"),
    }


class TestMerger(TestNexus):
    def setUp(self):
        TestNexus.setUp(self)
        self.PYTHON_ID = 100
        self.nexus.merger.add_global_rule(Python(ID=self.PYTHON_ID))
        self.nexus.merger.add_global_rule(Java())
        self.nexus.merger.add_global_rule(Bash())
        self.nexus.merger.add_selfmodrule(ChainAlias(self.nexus))
        self.nexus.merger.add_app_rule(EclipseCCR(), eclipse.context)
        self.nexus.merger.add_filter(demo_filter)
        self.nexus.merger.update_config()
        self.nexus.merger.merge(MergeInf.BOOT)
        self.set_global = self.nexus.merger.global_rule_changer()
        self.set_selfmod = self.nexus.merger.selfmod_rule_changer()

    def tearDown(self):
        self.nexus.merger.wipe()
        TestNexus.tearDown(self)

    def test_config_defaults(self):
        '''make sure the config is set up correctly'''
        self.assertTrue(CCRMerger._GLOBAL in self.nexus.merger._config)
        self.assertTrue(CCRMerger._SELFMOD in self.nexus.merger._config)
        self.assertTrue(CCRMerger._APP in self.nexus.merger._config)

    def test_config_placement(self):
        '''make sure the config is set up correctly'''
        self.assertTrue("Python" in self.nexus.merger._config[CCRMerger._GLOBAL])
        self.assertTrue(
            ChainAlias.pronunciation in self.nexus.merger._config[CCRMerger._SELFMOD])
        self.assertTrue(
            EclipseCCR.pronunciation in self.nexus.merger._config[CCRMerger._APP])
        self.assertEqual(len(self.nexus.merger.global_rule_names()), 3)
        self.assertEqual(len(self.nexus.merger.selfmod_rule_names()), 1)
        self.assertEqual(len(self.nexus.merger.app_rule_names()), 1)
        self.assertRaises(Exception, lambda: self.nexus.merger.add_global_rule(Java()))

    def test_rule_activation(self):
        bash = Bash()
        self.set_global("Python", True, True)
        self.assertTrue(self.PYTHON_ID in self.nexus.merger._base_global.composite)
        self.assertFalse(self.nexus.merger._base_global.mapping_actual()[SymbolSpecs.IF]\
                        ==bash.mapping_actual()[SymbolSpecs.IF])
        self.set_global("Java", True, True)
        self.assertFalse(self.nexus.merger._config[CCRMerger._GLOBAL]["Python"])
        self.assertTrue(self.nexus.merger._config[CCRMerger._GLOBAL]["Java"])
        self.assertFalse(self.PYTHON_ID in self.nexus.merger._base_global.composite)
        self.set_global("Bash", True, True)
        self.assertTrue(self.nexus.merger._config[CCRMerger._GLOBAL]["Bash"])
        self.assertTrue(self.nexus.merger._config[CCRMerger._GLOBAL]["Java"])
        self.set_selfmod(ChainAlias.pronunciation, True, True)
        self.assertTrue(self.nexus.merger._config[CCRMerger._GLOBAL]["Java"])
        self.assertFalse(
            ChainAlias.pronunciation in self.nexus.merger._config[CCRMerger._GLOBAL])
        self.assertTrue(
            self.nexus.merger._config[CCRMerger._SELFMOD][ChainAlias.pronunciation])
        self.set_global("Java", False, True)
        self.assertTrue(SymbolSpecs.IF in self.nexus.merger._base_global.mapping_actual())
        self.assertTrue(self.nexus.merger._base_global.mapping_actual()[SymbolSpecs.IF]\
                        ==bash.mapping_actual()[SymbolSpecs.IF])
        self.set_selfmod(ChainAlias.pronunciation, False, True)
        self.assertFalse("chain alias" in self.nexus.merger._base_global.mapping_actual())

    def test_reject_mapping_rules(self):

        self.assertRaises(AttributeError,
                          lambda: self.nexus.merger.add_global_rule(DemoMappingRule()))
