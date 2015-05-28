from Tkinter import (Scrollbar, Frame)
import json
import signal
import sys
from threading import Timer
import tkFont

import Tkinter as tk



try: # Style C -- may be imported into Caster, or externally
    BASE_PATH = "C:/NatLink/NatLink/MacroSystem/"
    if BASE_PATH not in sys.path:
        sys.path.append(BASE_PATH)
finally:
    import SimpleXMLRPCServer
    from SimpleXMLRPCServer import *
    from caster.lib import settings
    from caster.lib.dfplus.communication import Communicator

class StickyList:
    def __init__(self):
        self.setup_UI()
        self.setup_XMLRPC_server()
        
        
        # start server, tk main loop
        def start_server():
            while not self.server_quit:
                self.server.handle_request()  
        Timer(0.5, start_server).start()
        Timer(0.5, self.load_from_file).start()
        
        self.root.mainloop()
    
    def setup_XMLRPC_server(self): 
        self.server_quit = 0
        comm = Communicator()
        self.server = SimpleXMLRPCServer(("127.0.0.1", comm.com_registry["sticky_list"]), allow_none=True)
        self.server.register_function(self.xmlrpc_kill, "kill")
        self.server.register_function(self.xmlrpc_add_symbol, "add_symbol")
        self.server.register_function(self.xmlrpc_remove_symbol, "remove_symbol")
        self.server.register_function(self.xmlrpc_clear, "clear")
    
    def xmlrpc_kill(self):  #
        self.server_quit = 1
        self.root.destroy()
        os.kill(os.getpid(), signal.SIGTERM)
    
    def xmlrpc_add_symbol(self, symbol):
        index = self._get_next_available_index()
        self.data.append(symbol)
        self.root.after(10, self.add_to_list, index, symbol)
        return index
    
    def xmlrpc_remove_symbol(self, index):
        if index < 1 or index > len(self.data):
            return -1
        else:
            del self.data[index - 1]
            self._refresh_lists()
    
    def xmlrpc_clear(self):
        self.data = []
        self._refresh_lists()
    
    def _refresh_lists(self):
        self.listbox_numbering.delete(0, tk.END)
        self.listbox_content.delete(0, tk.END)
        for i in range(0, len(self.data)):
            self.add_to_list(i + 1, self.data[i])
    
    def _get_next_available_index(self):
        return len(self.data) + 1
    
    def scroll_to(self, index):
        self._scroll_lists(index)
        
    def _scroll_lists(self, *args):  # synchronizes  numbering list and  content list with a single scrollbar
        apply(self.listbox_numbering.yview, args)
        apply(self.listbox_content.yview, args)
        
    def add_to_list(self, index, item):
        self.listbox_numbering.insert(tk.END, str(index))
        self.listbox_content.insert(tk.END, item)
#         self.data.append(item)
    
    def load_from_file(self):
        self.data = []
        try:
            f = open(settings.SETTINGS["paths"]["S_LIST_JSON_PATH"], "r")
            self.data = json.loads(f.read())
            f.close()
        except IOError:
            print sys.exc_info()
        self._refresh_lists()
            
            
    
    def setup_UI(self):
        # setup tk
        self.root = tk.Tk()
        self.root.title(settings.S_LIST_VERSION)
        self.root.geometry("180x" + str(self.root.winfo_screenheight() - 100) + "-50+20")
        self.root.wm_attributes("-topmost", 1)
        self.root.protocol("WM_DELETE_WINDOW", self.xmlrpc_kill)
        self.customFont = tkFont.Font(family="Helvetica", size=8)
         
        # set up lists
        listframe = Frame(self.root)
        scrollbar = Scrollbar(listframe, orient=tk.VERTICAL)
        self.listbox_numbering = tk.Listbox(listframe, yscrollcommand=scrollbar.set, font=self.customFont)
        self.listbox_content = tk.Listbox(listframe, yscrollcommand=scrollbar.set, font=self.customFont)
        
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
    app = StickyList()
    
