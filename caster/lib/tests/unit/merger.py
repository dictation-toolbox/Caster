from caster.apps import eclipse
from caster.apps.eclipse import EclipseCCR
from caster.lib.ccr.java.java import Java
from caster.lib.ccr.python.python import Python
from caster.lib.ccr.recording.alias import ChainAlias
from caster.lib.dfplus.merge.ccrmerger import CCRMerger
from caster.lib.tests.unit.state import TestState


class TestMerger(TestState):
    
    def setUp(self):
        TestState.setUp(self)
        self.nexus.merger.add_global_rule(Python())
        self.nexus.merger.add_global_rule(Java())
        self.nexus.merger.add_selfmodrule(ChainAlias(self.nexus))
        self.nexus.merger.add_app_rule(EclipseCCR(), eclipse.context)
        self.nexus.merger.update_config()

class TestConfig(TestMerger):
    
    def test_config_defaults(self):
        self.assertTrue(CCRMerger._GLOBAL in self.nexus.merger._config)
        self.assertTrue(CCRMerger._SELFMOD in self.nexus.merger._config)
        self.assertTrue(CCRMerger._APP in self.nexus.merger._config)
    
    def test_config_placement(self):
        self.assertTrue("Python" in self.nexus.merger._config[CCRMerger._GLOBAL])
        self.assertTrue(ChainAlias.pronunciation in self.nexus.merger._config[CCRMerger._SELFMOD])
        self.assertTrue(EclipseCCR.pronunciation in self.nexus.merger._config[CCRMerger._APP])
        