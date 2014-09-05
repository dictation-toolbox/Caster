import Tkinter as tk
import tkFileDialog
from threading import Timer
import signal
from Tkinter import (StringVar, OptionMenu, Scrollbar, Frame, Label, Entry)
import os, re, sys, json
from lib import paths, utilities, settings
import bottle
from bottle import run, request  # , post,response




class Dispel:
    def __init__(self):
        
        
        # setup tk
        self.root = tk.Tk()
        self.root.title("Dispel")
#         self.root.geometry("200x" + str(self.root.winfo_screenheight() - 100) + "-1+20")
#         self.root.wm_attributes("-topmost", 1)
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

        # directory drop-down label
        Label(self.root, text="Directory, File:", name="pathlabel").pack()
        

        # file extension label and box
        ext_frame = Frame(self.root)
        Label(ext_frame, text="Ext(s):", name="extensionlabel").pack(side=tk.LEFT)
        self.ext_box = Entry(ext_frame, name="ext_box")
        self.ext_box.pack(side=tk.LEFT)
        ext_frame.pack()
        
        
        # update active file
        self.update_interval = 100
        self.root.after(self.update_interval, self.update_active_file)
        
        # start bottle server, tk main loop
        Timer(1, self.start_server).start()
#         self.root.after(self.interval, self.start_server)
        bottle.route('/process', method="POST")(self.process_request)
        self.root.mainloop()

    def on_exit(self):
        self.root.destroy()
        os.kill(os.getpid(), signal.SIGTERM)
    
    def start_server(self):
        run(host='localhost', port=1338, debug=True, server='cherrypy')
    
    def process_request(self):
        request_object = json.loads(request.body.read())
        action_type = request_object["action_type"]

        
        if action_type == "delay":
            self.root.after(10, self.search_box.focus_set)
        elif action_type == "extensions":
            self.root.after(10, self.ext_box.focus_set)
        elif action_type == "trigger_directory_box":
            self.root.after(10, self.dropdown.focus_set)
        elif action_type == "rescan":
            self.rescan_directory()

        return "c"


app = Dispel()  
