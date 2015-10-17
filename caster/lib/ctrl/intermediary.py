'''
Created on Oct 7, 2015

@author: synkarius
'''
import socket
from time import sleep

from caster.lib import settings, utilities


class StatusIntermediary:
    def __init__(self, c):
        self.communicator = c
    @staticmethod
    def attempt(f):
        try: f()
        except socket.error:
            utilities.launch_status()
            sleep(2)
            try: f()
            except Exception:
                utilities.report("problem communicating with status window:")
                utilities.simple_log()
    def hint(self, message):
        if settings.SETTINGS["miscellaneous"]["status_window_enabled"]:
            StatusIntermediary.attempt(lambda: self.communicator.get_com("status").hint(message))
        else:
            utilities.report(message)
    def text(self, message):
        if settings.SETTINGS["miscellaneous"]["status_window_enabled"]:
            StatusIntermediary.attempt(lambda: self.communicator.get_com("status").text(message))
        else:
            utilities.report(message)
    def kill(self):
        if utilities.window_exists(None, settings.STATUS_WINDOW_TITLE):
            self.communicator.get_com("status").kill()