from unittest import TestCase

from castervoice.lib.ctrl.mgr.engine_manager import EngineModesManager


class mockExclusiveManager():
    def set_mode(self, mode, modetype):
        pass


class TestEngineModesManager(TestCase):
    _manager = EngineModesManager(mockExclusiveManager())

    def test_set_engine_mode(self):
        self._manager.set_engine_mode(mode="numbers", state=True)
        self.assertEqual("numbers", self._manager.get_engine_mode())

    def test_get_previous_engine_state(self):
        self._manager.set_engine_mode(mode="spell", state=True)
        self._manager.set_engine_mode(mode="dictation", state=True)
        self.assertEqual("spell", self._manager.previous_engine_state)

    def test_restore_previous_engine_mode(self):
        self._manager.set_engine_mode(mode="spell", state=True)
        self._manager.set_engine_mode(mode="dictation", state=True)
        self._manager.set_engine_mode(state=False)
        self.assertEqual("spell", self._manager.get_engine_mode())

    def test_fail_engine_mode_change(self):
        self._manager.set_engine_mode(mode="numbers", state=True)
        self._manager.set_engine_mode(state=True)
        self.assertEqual("numbers", self._manager.get_engine_mode())

    def test_fail_invalid_mode(self):
        self._manager.set_engine_mode(mode="invalid", state=True)
        self.assertNotEqual("invalid", self._manager.get_engine_mode())

    def test_set_mic_mode(self):
        self._manager.set_mic_mode(mode="sleeping")
        self.assertEqual("sleeping", self._manager.get_mic_mode())
