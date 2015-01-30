import SimpleXMLRPCServer
from SimpleXMLRPCServer import *
from Tkinter import (Label, Text)
import os, sys
import signal
from threading import Timer

import Tkinter as tk
if __name__ == "__main__":
    BASE_PATH = sys.argv[0].split("MacroSystem")[0] + "MacroSystem"
    if BASE_PATH not in sys.path:
        sys.path.append(BASE_PATH)
    from lib import  settings
else:
    from lib import  settings

def communicate():
    return xmlrpclib.ServerProxy("http://127.0.0.1:" + str(settings.HMC_LISTENING_PORT))

class Homunculus(tk.Tk):
    def __init__(self, htype, data=None):
        tk.Tk.__init__(self, baseName="")
        self.setup_XMLRPC_server()
        self.htype = htype
        self.completed = False
        

        self.title(settings.HOMUNCULUS_VERSION)
        self.geometry("300x200+" + str(int(self.winfo_screenwidth() / 2 - 150)) + "+" + str(int(self.winfo_screenheight() / 2 - 100)))
        self.wm_attributes("-topmost", 1)
        self.protocol("WM_DELETE_WINDOW", self.xmlrpc_kill)
 
        # 
        if self.htype == settings.QTYPE_DEFAULT:
            Label(self, text="Enter Response", name="pathlabel").pack()
            self.ext_box = Text(self, name="ext_box")
            self.ext_box.pack(side=tk.LEFT)
        elif self.htype == settings.QTYPE_INSTRUCTIONS:
            Label(self, text=" ".join(data.split("_")), name="pathlabel").pack()
            self.ext_box = Text(self, name="ext_box")
            self.ext_box.pack(side=tk.LEFT)
        # 
        self.bind("<Return>", self.complete)
        
        
        # start server, tk main loop
        def start_server():
            while not self.server_quit:
                self.server.handle_request()  
        Timer(1, start_server).start()
        Timer(0.05, self.start_tk).start()
        # backup plan in case for whatever reason Dragon doesn't shut it down:
        Timer(300, self.xmlrpc_kill).start()
        

    def xmlrpc_kill(self):
        self.server_quit = 1
        self.destroy()
        os.kill(os.getpid(), signal.SIGTERM)
    
    
    def start_tk(self):
        self.mainloop()
    
    def setup_XMLRPC_server(self): 
        self.server_quit = 0
        self.server = SimpleXMLRPCServer(("127.0.0.1", settings.HMC_LISTENING_PORT), allow_none=True)
        self.server.register_function(self.xmlrpc_kill, "kill")
        self.server.register_function(self.xmlrpc_get_message, "get_message")
        
    def complete(self, e):
        self.completed = True
        
    def xmlrpc_get_message(self):
        '''override this for every new child class'''
        if self.completed:
            Timer(1, self.xmlrpc_kill).start()
            self.after(10, self.withdraw)
            return self.ext_box.get("1.0", tk.END).replace("\n", "")
        else:
            return None
