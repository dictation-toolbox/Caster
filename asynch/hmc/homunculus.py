from Tkinter import (Label, Text)
import json
import os, sys
import signal
from threading import Timer
BASE_PATH = r"C:\NatLink\NatLink\MacroSystem"
if BASE_PATH not in sys.path:
    sys.path.append(BASE_PATH)
import Tkinter as tk
from asynch.bottleserver import BottleServer
from lib import  settings





class HServer(BottleServer):
    def __init__(self, listening_port, kill_fn, htype, lock=None):
        self.response = None
        self.kill_fn = kill_fn
        self.htype = htype
        BottleServer.__init__(self, listening_port, lock=lock)
    
    def receive_request(self):
        '''will only get one kind of request'''
        message = {}
        
        
        if self.response != None:
            with self.lock:
                message["qtype"] = self.htype
                message["response"] = self.response
            Timer(1, self.kill_fn).start()
        return json.dumps(message)
        
            
        

class Homunculus(tk.Tk):
    def __init__(self, htype, data=None):
        tk.Tk.__init__(self, baseName="")
        self.htype = htype
        self.server = None
        

        self.title(settings.HOMUNCULUS_VERSION)
        self.geometry("300x200+" + str(int(self.winfo_screenwidth() / 2 - 150)) + "+" + str(int(self.winfo_screenheight() / 2 - 100)))
        self.wm_attributes("-topmost", 1)
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
 
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
        
        
        # start bottleserver server, tk main loop
        Timer(1, self.start_server).start()
        # backup plan in case for whatever reason Dragon doesn't shut it down:
        Timer(300, self.on_exit).start()
        Timer(0.05, self.start_tk).start()

    def on_exit(self):
        self.destroy()
        os.kill(os.getpid(), signal.SIGTERM)
    
    def start_tk(self):
        self.mainloop()
    
    def start_server(self):
        self.server = HServer(settings.HMC_LISTENING_PORT, self.on_exit, self.htype)
        
    def complete(self, e):
        '''override this for every new child class'''
        with self.server.lock:
            self.server.response = self.ext_box.get("1.0", tk.END)
        self.withdraw()
