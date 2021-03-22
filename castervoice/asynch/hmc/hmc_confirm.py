import six
if six.PY2:
    from Tkinter import Label # pylint: disable=import-error
else:
    from tkinter import Label
import os
import sys
from threading import Timer

try:  # Style C -- may be imported into Caster, or externally
    BASE_PATH = os.path.realpath(__file__).rsplit(os.path.sep + "castervoice", 1)[0]
    if BASE_PATH not in sys.path:
        sys.path.append(BASE_PATH)
finally:
    from castervoice.lib import settings
    from castervoice.asynch.hmc.homunculus import Homunculus


class HomunculusConfirm(Homunculus):
    def __init__(self, params):
        Homunculus.__init__(self, params[0])
        self.title(settings.HOMUNCULUS_VERSION + settings.HMC_TITLE_CONFIRM)

        self.geometry("320x50+" + str(int(self.winfo_screenwidth()/2 - 160)) + "+" +
                      str(int(self.winfo_screenheight()/2 - 25)))
        Label(
            self,
            text="Please confirm: " + " ".join(params[1].split(settings.HMC_SEPARATOR)),
            name="i").pack()
        Label(self, text="(say \"confirm\" or \"disconfirm\")", name="i2").pack()

    def xmlrpc_get_message(self):
        if self.completed:
            response = {"mode": "confirm"}
            response["confirm"] = self.value
            Timer(1, self.xmlrpc_kill).start()
            self.after(10, self.withdraw)
            return response
        else:
            return None

    def xmlrpc_do_action(self, action, details=None):
        if isinstance(action, bool):
            self.completed = True
            '''1 is True, 2 is False'''
            self.value = 1 if action else 2
