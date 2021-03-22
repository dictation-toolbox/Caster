import sys
import six
if six.PY2:
    from SimpleXMLRPCServer import SimpleXMLRPCServer  # pylint: disable=import-error
    import Tkinter as tk # pylint: disable=import-error
    from Tkinter import Label, Text # pylint: disable=import-error
else:
    from xmlrpc.server import SimpleXMLRPCServer # pylint: disable=no-name-in-module
    from tkinter import Label, Text
    import tkinter as tk
import signal, os
from threading import Timer

try:  # Style C -- may be imported into Caster, or externally
    BASE_PATH = os.path.realpath(__file__).rsplit(os.path.sep + "castervoice", 1)[0]
    if BASE_PATH not in sys.path:
        sys.path.append(BASE_PATH)
finally:
    from castervoice.lib import settings
    from castervoice.lib.merge.communication import Communicator


class Homunculus(tk.Tk):
    def __init__(self, htype, data=None):
        tk.Tk.__init__(self, baseName="")
        self.setup_xmlrpc_server()
        self.htype = htype
        self.completed = False
        self.max_after_completed = 10

        self.title(settings.HOMUNCULUS_VERSION)
        self.geometry("300x200+" + str(int(self.winfo_screenwidth()/2 - 150)) + "+" +
                      str(int(self.winfo_screenheight()/2 - 100)))
        self.wm_attributes("-topmost", 1)
        self.protocol("WM_DELETE_WINDOW", self.xmlrpc_kill)

        #
        if self.htype == settings.QTYPE_DEFAULT:
            Label(
                self, text="Enter response then say 'complete'", name="pathlabel").pack()
            self.ext_box = Text(self, name="ext_box")
            self.ext_box.pack(side=tk.LEFT)
            self.data = [0, 0]
        elif self.htype == settings.QTYPE_INSTRUCTIONS:
            self.data = data.split("|")
            Label(
                self,
                text=" ".join(self.data[0].split(settings.HMC_SEPARATOR)), # pylint: disable=no-member
                name="pathlabel").pack()
            self.ext_box = Text(self, name="ext_box")
            self.ext_box.pack(side=tk.LEFT)

        # start server, tk main loop
        def start_server():
            while not self.server_quit:
                self.server.handle_request()

        Timer(1, start_server).start()
        Timer(0.05, self.start_tk).start()
        # backup plan in case for whatever reason Dragon doesn't shut it down:
        Timer(300, self.xmlrpc_kill).start()

    def start_tk(self):
        self.mainloop()

    def setup_xmlrpc_server(self):
        self.server_quit = 0
        comm = Communicator()
        self.server = SimpleXMLRPCServer(
            (Communicator.LOCALHOST, comm.com_registry["hmc"]),
            logRequests=False, allow_none=True)
        self.server.register_function(self.xmlrpc_do_action, "do_action")
        self.server.register_function(self.xmlrpc_complete, "complete")
        self.server.register_function(self.xmlrpc_get_message, "get_message")
        self.server.register_function(self.xmlrpc_kill, "kill")

    def xmlrpc_kill(self):
        self.server_quit = 1
        self.destroy()
        os.kill(os.getpid(), signal.SIGTERM)

    def xmlrpc_complete(self):
        self.completed = True
        self.after(10, self.withdraw)
        Timer(self.max_after_completed, self.xmlrpc_kill).start()

    def xmlrpc_get_message(self):
        '''override this for every new child class'''
        if self.completed:
            Timer(1, self.xmlrpc_kill).start()
            return [self.ext_box.get("1.0", tk.END), self.data]
        else:
            return None

    def xmlrpc_do_action(self, action, details=None):
        '''override'''
