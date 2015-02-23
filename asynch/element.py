import SimpleXMLRPCServer
from SimpleXMLRPCServer import *
from Tkinter import (Scrollbar, Frame)
import signal
from threading import Timer
import tkFont
import Tkinter as tk

BASE_PATH = sys.argv[0].split("MacroSystem")[0] + "MacroSystem"
if BASE_PATH not in sys.path:
    sys.path.append(BASE_PATH)
    from lib import  settings, utilities
else:
    from lib import  settings, utilities

class ElementViewer:
    def __init__(self):
        self.setup_UI()
        self.setup_XMLRPC_server()
         
        # start server, tk main loop
        def start_server():
            while not self.server_quit:
                self.server.handle_request()  
        Timer(1, start_server).start()
        self.root.mainloop()
    
    def setup_XMLRPC_server(self): 
        self.server_quit = 0
        self.server = SimpleXMLRPCServer(("127.0.0.1", settings.ELEMENT_LISTENING_PORT), allow_none=True)
        self.server.register_function(self.xmlrpc_kill, "kill")
    def xmlrpc_kill(self):  #
        self.server_quit = 1
        self.root.destroy()
        os.kill(os.getpid(), signal.SIGTERM)
     
            
    def scroll_to(self, index):
        self._scroll_lists(index)
    def _scroll_lists(self, *args):  # synchronizes  numbering list and  content list with a single scrollbar
        apply(self.listbox_numbering.yview, args)
        apply(self.listbox_content.yview, args)
    def _clear_lists(self):  # used when changing files
        self.listbox_numbering.delete(0, tk.END)
        self.listbox_content.delete(0, tk.END)
        self.sticky_listbox_numbering.delete(0, tk.END)
        self.sticky_listbox_content.delete(0, tk.END)
    def reload_list(self, namelist, stickylist):
        self.listbox_index = 0  # reset index upon reload
        for sticky in stickylist:
            self.add_to_stickylist(sticky)
        for name in namelist:
            self.add_to_list(name)
    def add_to_list(self, item):
        self.listbox_index += 1    
        self.listbox_numbering.insert(tk.END, str(self.listbox_index))
        self.listbox_content.insert(tk.END, item)
    
    def setup_UI(self):
        # setup tk
        self.root = tk.Tk()
        self.root.title(settings.ELEMENT_VERSION)
        self.root.geometry("180x" + str(self.root.winfo_screenheight() - 100) + "-50+20")
        self.root.wm_attributes("-topmost", 1)
        self.root.protocol("WM_DELETE_WINDOW", self.xmlrpc_kill)
        self.customFont = tkFont.Font(family="Helvetica", size=8)
         
        # set up lists
        listframe = Frame(self.root)
        scrollbar = Scrollbar(listframe, orient=tk.VERTICAL)
        self.listbox_numbering = tk.Listbox(listframe, yscrollcommand=scrollbar.set, font=self.customFont)
        self.listbox_content = tk.Listbox(listframe, yscrollcommand=scrollbar.set, font=self.customFont)
         
        self.listbox_index = 0
        h = 52
        lbn_opt = {"height":h, "width":4}
        lbn_opt2 = {"height":h}
         
        scrollbar.config(command=self._scroll_lists)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_numbering.config(lbn_opt)
        self.listbox_numbering.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.listbox_content.config(lbn_opt2)
        self.listbox_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
         
        listframe.pack()


if __name__ == '__main__':
    app = ElementViewer()
    
