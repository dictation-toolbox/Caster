'''
Created on Oct 7, 2015

@author: synkarius
'''
from caster.lib import settings, utilities


class StatusIntermediary:
    def __init__(self, c):
        self.communicator = c
    def hint(self, message):
        if settings.SETTINGS["miscellaneous"]["status_window_enabled"]:
            self.communicator.get_com("status").hint(message)
        else:
            utilities.report(message)
    def text(self, message):
        if settings.SETTINGS["miscellaneous"]["status_window_enabled"]:
            self.communicator.get_com("status").text(message)
        else:
            utilities.report(message)
    def kill(self):
        if utilities.window_exists(None, settings.STATUS_WINDOW_TITLE):
            self.communicator.get_com("status").kill()