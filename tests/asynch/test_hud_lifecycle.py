from unittest import TestCase
from unittest.mock import MagicMock, patch
import subprocess

from castervoice.asynch import hud_support


class TestHudLifecycle(TestCase):

    def setUp(self):
        hud_support._HUD_PROCESS = None

    def tearDown(self):
        hud_support._HUD_PROCESS = None

    @patch("castervoice.lib.settings.SETTINGS", {"paths": {"PYTHONW": "pythonw.exe", "HUD_PATH": "hud.py"}})
    @patch("castervoice.lib.control.nexus")
    @patch("subprocess.Popen")
    def test_start_hud_spawns_process_when_ping_fails(self, mock_popen, mock_nexus):
        mock_hud = MagicMock()
        mock_hud.ping.side_effect = Exception("Not running")
        mock_nexus.return_value.comm.get_com.return_value = mock_hud

        mock_proc = MagicMock()
        mock_popen.return_value = mock_proc

        hud_support.start_hud()

        mock_popen.assert_called_once()
        self.assertEqual(hud_support._HUD_PROCESS, mock_proc)

    @patch("castervoice.lib.control.nexus")
    @patch("subprocess.Popen")
    def test_start_hud_does_not_spawn_when_already_running(self, mock_popen, mock_nexus):
        mock_hud = MagicMock()
        mock_hud.ping.return_value = 0
        mock_nexus.return_value.comm.get_com.return_value = mock_hud

        hud_support.start_hud()

        mock_popen.assert_not_called()
        self.assertIsNone(hud_support._HUD_PROCESS)

    @patch("castervoice.lib.control.nexus")
    def test_stop_hud_calls_kill_and_waits_for_process(self, mock_nexus):
        mock_hud = MagicMock()
        mock_nexus.return_value.comm.get_com.return_value = mock_hud

        mock_proc = MagicMock()
        hud_support._HUD_PROCESS = mock_proc

        hud_support.stop_hud()

        mock_hud.kill.assert_called_once()
        mock_proc.wait.assert_called_once_with(timeout=1.5)
        self.assertIsNone(hud_support._HUD_PROCESS)

    @patch("castervoice.lib.control.nexus")
    def test_stop_hud_force_kills_on_timeout(self, mock_nexus):
        mock_hud = MagicMock()
        mock_nexus.return_value.comm.get_com.return_value = mock_hud

        mock_proc = MagicMock()
        mock_proc.wait.side_effect = subprocess.TimeoutExpired(cmd="pythonw", timeout=1.5)
        hud_support._HUD_PROCESS = mock_proc

        hud_support.stop_hud()

        mock_hud.kill.assert_called_once()
        mock_proc.wait.assert_called_once_with(timeout=1.5)
        mock_proc.kill.assert_called_once()
        self.assertIsNone(hud_support._HUD_PROCESS)

    @patch("castervoice.asynch.hud_support.stop_hud")
    @patch("castervoice.asynch.hud_support.start_hud")
    @patch("time.sleep")
    def test_restart_hud_sequence(self, mock_sleep, mock_start, mock_stop):
        hud_support.restart_hud()

        mock_stop.assert_called_once()
        mock_sleep.assert_called_once_with(0.5)
        mock_start.assert_called_once()

    @patch("castervoice.lib.control.nexus")
    def test_show_hud_calls_rpc_when_running(self, mock_nexus):
        mock_hud = MagicMock()
        mock_nexus.return_value.comm.get_com.return_value = mock_hud

        hud_support.show_hud()

        mock_hud.show_hud.assert_called_once()

    @patch("castervoice.asynch.hud_support.start_hud")
    @patch("castervoice.lib.control.nexus")
    def test_show_hud_auto_launches_when_not_running(self, mock_nexus, mock_start):
        mock_hud = MagicMock()
        mock_hud.show_hud.side_effect = Exception("HUD process is down")
        mock_nexus.return_value.comm.get_com.return_value = mock_hud

        hud_support.show_hud()

        mock_start.assert_called_once()
