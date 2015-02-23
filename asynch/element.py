import SimpleXMLRPCServer
from SimpleXMLRPCServer import *
from Tkinter import (StringVar, OptionMenu, Scrollbar, Frame, Label, Entry)
import signal
from threading import Timer
import tkFileDialog
import tkFont
import Tkinter as tk

BASE_PATH = sys.argv[0].split("MacroSystem")[0] + "MacroSystem"
if BASE_PATH not in sys.path:
    sys.path.append(BASE_PATH)
    from lib import  settings, utilities
else:
    from lib import  settings, utilities

class Element:
    def __init__(self):
        self.setup_regexes()
        self.setup_UI()
        self.setup_XMLRPC_server()
         
        # update active file
        self.update_interval = 100
        self.filename_pattern = re.compile(r"[/\\]([\w]+\.[\w]+)")
        self.old_active_window_title = ""
        self.root.after(self.update_interval, self.update_active_file)
         
        # start server, tk main loop
        def start_server():
            while not self.server_quit:
                self.server.handle_request()  
        Timer(1, start_server).start()
        self.root.mainloop()
    
    def setup_regexes(self):
        '''print '''
    
    def setup_XMLRPC_server(self): 
        self.server_quit = 0
        self.server = SimpleXMLRPCServer(("127.0.0.1", settings.ELEMENT_LISTENING_PORT), allow_none=True)
        self.server.register_function(self.xmlrpc_kill, "kill")


    
    def xmlrpc_kill(self):  #
        self.server_quit = 1
        self.root.destroy()
        os.kill(os.getpid(), signal.SIGTERM)
        
   
    


        
            
    def scroll_to(self, index):  # don't need this for sticky list
        self.scroll_lists(index)
    
    def scroll_lists(self, *args):  # synchronizes  numbering list and  content list with a single scrollbar
        apply(self.listbox_numbering.yview, args)
        apply(self.listbox_content.yview, args)

        
    def clear_lists(self):  # used when changing files
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
        # setup basics
        self.JSON_PATH = settings.SETTINGS["paths"]["ELEMENT_JSON_PATH"]
        self.TOTAL_SAVED_INFO = settings.load_json_file(self.JSON_PATH)
 
        self.first_run = True
        if "config" in self.TOTAL_SAVED_INFO and "last_directory" in self.TOTAL_SAVED_INFO["config"]:
            self.first_run = False
        else:
            self.TOTAL_SAVED_INFO["config"] = {}
            self.TOTAL_SAVED_INFO["directories"] = {}
        self.current_file = None
        self.last_file_loaded = None
         
        # setup tk
        self.root = tk.Tk()
        self.root.title(settings.ELEMENT_VERSION)
        self.root.geometry("180x" + str(self.root.winfo_screenheight() - 100) + "-50+20")
        self.root.wm_attributes("-topmost", 1)
        self.root.protocol("WM_DELETE_WINDOW", self.xmlrpc_kill)
        self.customFont = tkFont.Font(family="Helvetica", size=8)
        
          
        # setup options for directory ask
        
         
        # setup drop-down box
        self.dropdown_selected = StringVar(self.root)
        self.default_dropdown_message = "Please select a scanned folder"
        self.dropdown_selected.set(self.default_dropdown_message)
        self.dropdown = OptionMenu(self.root, self.dropdown_selected, self.default_dropdown_message)
        self.dropdown.pack()
        if not self.first_run:
            self.populate_dropdown()
 
        # file extension label and box
        ext_frame = Frame(self.root)
        Label(ext_frame, text="Ext(s):", name="extensionlabel", font=self.customFont).pack(side=tk.LEFT)
        self.ext_box = Entry(ext_frame, name="ext_box", font=self.customFont)
        self.ext_box.pack(side=tk.LEFT)
        ext_frame.pack()
 
        # fill in remembered information  if it exists
        if not self.first_run:
            last_dir = self.TOTAL_SAVED_INFO["config"]["last_directory"]
            self.dropdown_selected.set(last_dir)
            self.ext_box.insert(0, ",".join(self.TOTAL_SAVED_INFO["directories"][last_dir]["extensions"]))

        # set up lists
        stickyframe = Frame(self.root)
        stickyscrollbar = Scrollbar(stickyframe, orient=tk.VERTICAL)
        self.sticky_listbox_numbering = tk.Listbox(stickyframe, yscrollcommand=stickyscrollbar.set, font=self.customFont)
        self.sticky_listbox_content = tk.Listbox(stickyframe, yscrollcommand=stickyscrollbar.set, font=self.customFont)
 
        self.sticky_listbox_index = 0
        s_lbn_opt = {}
        s_lbn_opt_height = 10
        s_lbn_opt["height"] = s_lbn_opt_height
        s_lbn_opt["width"] = 4
        s_lbn_opt2 = {}
        s_lbn_opt2["height"] = s_lbn_opt_height
         
        stickyscrollbar.config(command=self.sticky_scroll_lists)
        stickyscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.sticky_listbox_numbering.config(s_lbn_opt)
        self.sticky_listbox_numbering.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.sticky_listbox_content.config(s_lbn_opt2)
        self.sticky_listbox_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        stickyframe.pack()
        #-------
        listframe = Frame(self.root)
        scrollbar = Scrollbar(listframe, orient=tk.VERTICAL)
        self.listbox_numbering = tk.Listbox(listframe, yscrollcommand=scrollbar.set, font=self.customFont)
        self.listbox_content = tk.Listbox(listframe, yscrollcommand=scrollbar.set, font=self.customFont)
         
        self.listbox_index = 0
        lbn_opt = {}
        lbn_opt_height = 39
        lbn_opt["height"] = lbn_opt_height
        lbn_opt["width"] = 4
        lbn_opt2 = {}
        lbn_opt2["height"] = lbn_opt_height
         
        scrollbar.config(command=self.scroll_lists)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_numbering.config(lbn_opt)
        self.listbox_numbering.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.listbox_content.config(lbn_opt2)
        self.listbox_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
         
        listframe.pack()


if __name__ == '__main__':
    app = Element()
    
