from unittest import TestCase

from mock import Mock

from castervoice.lib import settings


class SettingsEnabledTestCase(TestCase):

    def _enable_file_writing(self):
        from castervoice.lib.util import guidance
        reject = guidance.offer

        def disable_file_writing():
            guidance.offer = reject

        def do_nothing():
            pass
        guidance.offer = do_nothing
        self.addCleanup(disable_file_writing)

    def _set_setting(self, key_path, value):
        if settings.SETTINGS is None:
            settings.SETTINGS = {}
        s = settings.SETTINGS
        len_kp = len(key_path)
        for i in range(0, len_kp):
            kp = key_path[i]
            if i == len_kp - 1:
                s[kp] = value
            else:
                if kp not in s:
                    s[kp] = {}
                s = s[kp]


def prevent_initialize():
    settings.initialize = Mock()


def prevent_save():
    settings.save_config = Mock()
