#http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
import Tkinter as tk
import tkFileDialog
from threading import (Timer, Thread)
import signal
from Tkinter import (StringVar, OptionMenu, Scrollbar, Frame)
import os, re, sys, json
import paths, utilities

import bottle
from bottle import run, post, request, response

"""
- 1 to 10 sticky list at the top
X    - Automatically figures out which file is open by continually scanning the top-level window and looking for something with the file extension
X    - it scans an entire directory, creating an XML file for that directory, which contains the names of all imports and things which follow a single
       = operator, or other language specific traits
- It also has a drop-down box for manually switching files, and associated hotkey
- It has hotkeys for everything, and so can be voice controlled
- Each name also has a hotkey/button to delete it and to make it sticky
- It can also take the highlighted text and add it to the list
X    - It remembers what folder was opened last, maybe save this to the json file
- A  rescan directory command
- Make it longer and docked on the right

- Create better patterns than the generic pattern
"""




class Element:
    def __init__(self):
        
        # setup stuff that were previously globals
        self.JSON_PATH=paths.get_element_json_path()
        self.TOTAL_SAVED_INFO={}
        self.GENERIC_PATTERN=re.compile("([A-Za-z0-9._]+\s*=)|(import [A-Za-z0-9._]+)")

        
        # setup tk
        self.all_names=[]
        self.root=tk.Tk()
        self.root.title("Element v.01")
        self.root.geometry("200x500")
        self.root.wm_attributes("-topmost", 1)
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)
        
        # setup hotkeys
        self.root.bind_all("1", self.get_new)
        
        
        # setup options for directory ask
        self.dir_opt = {}
        self.dir_opt['initialdir'] = 'C:\\natlink\\natlink\\macrosystem\\'
        self.dir_opt['mustexist'] = False
        self.dir_opt['parent'] = self.root
        self.dir_opt['title'] = 'Please select directory'
        
        # setup drop-down box
        self.dropdown_selected=StringVar(self.root)
        self.default_dropdown_message="Please select a scanned folder"
        self.dropdown_selected.set(self.default_dropdown_message)
        self.dropdown=OptionMenu(self.root, self.dropdown_selected, self.default_dropdown_message)
        self.dropdown.pack()
        self.populate_dropdown()
        if len(self.TOTAL_SAVED_INFO)==0:# if this is being run for the first time:
            self.TOTAL_SAVED_INFO["directories"]={}
            self.TOTAL_SAVED_INFO["config"]={}
        else:
            self.dropdown_selected.set(self.TOTAL_SAVED_INFO["config"]["last_directory"])
        
        # set up list
        label1 = tk.Label(text="Variable Names", name="label1")
        label1.pack()
        listframe= Frame(self.root)
        scrollbar = Scrollbar(listframe, orient=tk.VERTICAL)
        self.listbox_index=0
        self.listbox_numbering = tk.Listbox(listframe, yscrollcommand=scrollbar.set)
        self.listbox_content = tk.Listbox(listframe, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.scroll_lists)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_numbering.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        lbn_opt={}
        lbn_opt["width"]=4
        self.listbox_numbering.config(lbn_opt)
        self.listbox_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        for item in ["e one", "e two", "e three", "e four"]:
            self.add_to_list(item)
        listframe.pack()
        
        # setup search box
        self.search_box = tk.Entry(name="search_box")
        self.search_box.pack()
        
        # update active file every n seconds
        self.interval=1
        self.filename_pattern=re.compile(r"[/\\]([\w]+\.[\w]+)")
        self.old_active_window_title=""
        Timer(self.interval, self.update_active_file).start()
        
        # start bottle server, tk main loop
        Timer(self.interval, self.start_server).start()
        bottle.route('/process',method="POST")(self.process_request)
        self.root.mainloop()
    
    def on_exit(self):
        utilities.report("Element: shutting down")
        self.root.destroy()
        os.kill(os.getpid(), signal.SIGTERM)
    
    def start_server(self):
        run(host='localhost', port=1337, debug=True)
    
    def update_active_file(self):
        
        active_window_title=utilities.get_active_window_title()
        if not self.old_active_window_title==active_window_title:
            
            filename=""
            
            match_objects=self.filename_pattern.findall(active_window_title)
            if not len(match_objects)==  0:# if we found variable name in the line
                filename=match_objects[0]
             
            if not filename=="":
                self.old_active_window_title=active_window_title# only update were on a new file, not just a new window
                self.populate_list(filename)
        Timer(self.interval, self.update_active_file).start()
        
    def add_to_list(self, item):
        self.listbox_index+=1    
        self.listbox_numbering.insert(tk.END, str(self.listbox_index))
        self.listbox_content.insert(tk.END, item)
    
    def scroll_lists(self, *args):
        apply(self.listbox_numbering.yview, args)
        apply(self.listbox_content.yview, args)
    
    def clear_lists(self):
        self.listbox_numbering.delete(0, tk.END)
        self.listbox_content.delete(0, tk.END)
    
    #FOR MANIPULATING THE     LIST    
    def move_to_top(self,name):
        self.all_names.remove(name)
        self.all_names=[name]+self.all_names
    
    #FOR LOADING 
    def populate_dropdown(self):
        self.TOTAL_SAVED_INFO = utilities.load_json_file(self.JSON_PATH)
        menu = self.dropdown["menu"]
        menu.delete(0, tk.END)
        if "directories" in self.TOTAL_SAVED_INFO:
            for key in self.TOTAL_SAVED_INFO["directories"]:
                menu.add_command(label=key, command=lambda key=key: self.select_from_dropdown(key))
    
    def select_from_dropdown(self, key):
        self.TOTAL_SAVED_INFO["config"]["last_directory"]=key
        utilities.save_json_file(self.TOTAL_SAVED_INFO, self.JSON_PATH)
        self.dropdown_selected.set(key)
    
    def populate_list(self, file_to_activate):
        """
        target behavior:
        Takes a filename (either from scan or from a second drop-down), 
        and searches for it in the selected folder. 
        Later on,  add an option to allow it to search in non-selected folders as well
        """
        
        selected_directory=self.dropdown_selected.get()
        file_record=None
        if selected_directory==self.default_dropdown_message:
            return#  if a scanned for hasn't been selected, there's no need to go any further
        self.clear_lists()
        for absolute_path in self.TOTAL_SAVED_INFO["directories"][selected_directory]["files"]:
            if absolute_path.endswith(file_to_activate):
                file_record=self.TOTAL_SAVED_INFO["directories"][selected_directory]["files"][absolute_path]
                break
        if not file_record==None:
            self.reload_list(file_record["names"])
    
    def reload_list(self, list):
        self.listbox_index=0# reset index upon reload
        for name in list:
            self.add_to_list(name)
                
    #FOR SCANNING AND SAVING FILES    
    def get_new(self,event):
        directory=self.ask_directory()
        self.scan_directory(directory)
        utilities.save_json_file(self.TOTAL_SAVED_INFO, self.JSON_PATH)
        self.populate_dropdown()
        
    def scan_directory(self,directory):
        pattern_being_used=self.GENERIC_PATTERN# later on, can add code to choose which pattern to use
        
        scanned_directory={}
        acceptable_extensions=[".py"]# this is hardcoded for now, will read from a box later
        try:
            for base, dirs, files in os.walk(directory):# traverse base directory, and list directories as dirs and files as files
                utilities.report(base)
                for fname in files:
                    extension="."+fname.split(".")[-1]
                    if extension in acceptable_extensions:
                        scanned_file={}
                        scanned_file["filename"]=fname
                        absolute_path=base+"/"+fname
                        scanned_file["names"]=[]
                        f = open(base+"\\"+fname, "r")
                        lines = f.readlines()
                        f.close()
                        
                        for line in lines:
                            match_objects=pattern_being_used.findall(line)
                            if not len(match_objects)==  0:# if we found variable name in the line
                                mo=match_objects[0][0]
                                result=""
                                if "." in mo:# figure out whether it's an import#----- to do: this check doesn't work right
                                    result=mo.split(".")[-1]
                                else:# Or not an import
                                    result=mo.replace(" ", "").split("=")[0]
                                # also to do: scan for function names
                                
                                if not result in scanned_file["names"] and not result=="":
                                    scanned_file["names"].append(result)
                        
                        scanned_directory[absolute_path]=scanned_file
        except Exception:
            utilities.report(utilities.list_to_string(sys.exc_info()))
        meta_information={}
        meta_information["files"]=scanned_directory
        meta_information["extensions"]=acceptable_extensions
        self.TOTAL_SAVED_INFO["directories"][directory]=meta_information
        

        
    def ask_directory(self):# returns a string of the directory name
        return tkFileDialog.askdirectory(**self.dir_opt)
    
    def get_name(self, index):
        return self.listbox_content.get(index, index+1)[0]

    def process_request(self):#GENERIC_PATTERN=listbox_numbering =
        request_object = json.loads(request.body.read())
        action_type=request_object["action_type"]
        if "index" in request_object:
            index=int(request_object["index"])
            if action_type=="retrieve":
                return self.get_name(index)
            elif action_type=="sticky":
                return "mode not ready yet"
                # here you need a third piece of data, to let you know whether this word was already in the non-sticky list, or if it's new
            elif action_type=="delete":
                return "mode not ready yet"
            elif action_type=="unsticky":
                return "mode not ready yet"
        elif "name" in request_object:
            name=request_object["name"]
            if action_type=="add":
                if name not in self.all_names:
                    self.all_names.append(name)
                    #save json
                    # reload list- you want to make sure that all_names is being used in the first place
            return "mode not ready yet"
        return 'unrecognized request received: '+request_object["action_type"]


app=Element()  
