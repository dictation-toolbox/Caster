import six
if six.PY2:
    from Tkinter import Label, Entry, StringVar # pylint: disable=import-error
    import tkFileDialog # pylint: disable=import-error
else:
    from tkinter import Label, Entry, StringVar, filedialog as tkFileDialog
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


class HomunculusDirectory(Homunculus):
    def __init__(self, params):
        Homunculus.__init__(self, params[0])
        self.title(settings.HOMUNCULUS_VERSION + settings.HMC_TITLE_DIRECTORY)

        self.geometry("640x50+" + str(int(self.winfo_screenwidth()/2 - 320)) + "+" +
                      str(int(self.winfo_screenheight()/2 - 25)))
        Label(self, text="Enter directory or say 'browse'", name="pathlabel").pack()
        self.content = StringVar()
        self.word_box = Entry(self, name="word_box", width=640, textvariable=self.content)
        self.word_box.pack()

    def xmlrpc_get_message(self):
        if self.completed:
            response = {"mode": "ask_dir"}
            response["path"] = self.word_box.get()

            Timer(1, self.xmlrpc_kill).start()
            self.after(10, self.withdraw)
            return response
        else:
            return None

    def _ask_directory(self):
        dir_opt = {}
        dir_opt['initialdir'] = os.path.expanduser('~')  #os.environ["HOME"]
        dir_opt['mustexist'] = False
        dir_opt['parent'] = self
        dir_opt['title'] = 'Please select directory'
        result = tkFileDialog.askdirectory(**dir_opt)
        self.content.set(result)

    def xmlrpc_do_action(self, action, details=None):
        if action == "dir":
            self.after(10, self._ask_directory)
