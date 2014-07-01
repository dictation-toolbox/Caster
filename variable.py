#http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
import Tkinter as tk
import tkFileDialog
from threading import (Timer, Thread)
import signal
from Tkinter import (StringVar, OptionMenu, Scrollbar, Frame)
import os, re, sys, json
import paths, utilities


from bottle import run, post, request, response

"""
- 1 to 10 sticky list at the top
- Automatically figures out which file is open by continually scanning the top-level window and looking for something with the file extension
 - it scans an entire directory, creating an XML file for that directory, which contains the names of all imports and things which follow a single
   = operator, or other language specific traits
- It also has a drop-down box for manually switching files, and associated hotkey
- It has hotkeys for everything, and so can be voice controlled
- Each word also has a hotkey/button to delete it and to make it sticky
- It can also take the highlighted text and add it to the list



- Create better patterns than the generic pattern
"""

SCANNED_FOLDERS_PATH=paths.get_scanned_folders_path()
SCANNED_FILES={}

GENERIC_PATTERN=re.compile("([A-Za-z0-9._]+\s*=)|(import [A-Za-z0-9._]+)")

class ScannedFile:
    def __init__(self):
        self.filename=""
        self.absolute_path=""
        self.variables=[]

class Element:
    def __init__(self):

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
        selected=StringVar(self.root)
        selected.set("Please select a scanned folder")
        self.dropdown=OptionMenu(self.root, selected, "Please select a scanned folder")
        self.dropdown.pack()
        
        # set up list
        label1 = tk.Label(text="Variable Names", name="label1")
        label1.pack()
        listframe= Frame(self.root)
        scrollbar = Scrollbar(listframe, orient=tk.VERTICAL)
        self.listbox_numbering = tk.Listbox(listframe, yscrollcommand=scrollbar.set)
        self.listbox_content = tk.Listbox(listframe, yscrollcommand=scrollbar.set)
        
        scrollbar.config(command=self.scroll_lists)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_numbering.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        lbn_opt={}
        lbn_opt["width"]=2
        self.listbox_numbering.config(lbn_opt)
        self.listbox_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        for item in ["e one", "e two", "e three", "e four"]:
            self.add_to_list(item)
        listframe.pack()
        
        # setup search box
        self.search_box = tk.Entry(name="search_box")
        self.search_box.pack()
        
        # update active file every n seconds
        self.interval=5
        self.filename_pattern=re.compile(r"[/\\]([\w]+\.[\w]+)")
        Timer(self.interval, self.update_active_file).start()
        
        # start bottle server, tk main loop
        Timer(self.interval, self.start_server).start()
        self.root.mainloop()
    
    def on_exit(self):
        print "Element: shutting down"
        self.root.destroy()
        os.kill(os.getpid(), signal.SIGTERM)
    
    def start_server(self):
        run(host='localhost', port=8080, debug=True)
    
    def update_active_file(self):
        active_window_title=utilities.get_active_window_title()
        filename=""
#         
        match_objects=self.filename_pattern.findall(active_window_title)
        if not len(match_objects)==  0:# if we found variable name in the line
            filename=match_objects[0]
         
        if not filename=="":
            print filename
        Timer(self.interval, self.update_active_file).start()
        
    def add_to_list(self, item):
        self.listbox_numbering.insert(tk.END, str(self.listbox_numbering.size()+1))
        self.listbox_content.insert(tk.END, item)
    
    def scroll_lists(self, *args):
        apply(self.listbox_numbering.yview, args)
        apply(self.listbox_content.yview, args)
    
    
    #FOR MANIPULATING THE     LIST    
    def move_to_top(self,name):
        self.all_names.remove(name)
        self.all_names=[name]+self.all_names
    
    
    #FOR SCANNING AND SAVING FILES    
    def get_new(self,event):
        global SCANNED_FILES
        global SCANNED_FOLDERS_PATH
        directory=self.ask_directory()
        self.scan_directory(directory)
        scan_data = json.dumps(SCANNED_FILES, sort_keys=True, indent=4,
            ensure_ascii=False)
        with open(SCANNED_FOLDERS_PATH, "w+") as f:
            f.write(scan_data)  # Save config to file.
            f.close()
        
    def scan_directory(self,directory):
        global GENERIC_PATTERN
        global SCANNED_FILES
        pattern_being_used=GENERIC_PATTERN# later on, can add code to choose which pattern to use
        
        
        try:
            acceptable_extensions=[".py"]# this is hardcoded for now, will read from a box later
            for base, dirs, files in os.walk(directory):# traverse base directory, and list directories as dirs and files as files
                path = base.split('/')
                
                print (len(path) - 1) *'---' , base       
                for file in files:
                    extension="."+file.split(".")[-1]
                    if extension in acceptable_extensions:
                        scanned_file={}
                        scanned_file["filename"]=file
                        scanned_file["absolute_path"]=base+"/"+file
                        scanned_file["variables"]=[]
                        f = open(base+"\\"+file, "r")
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
                                
                                if not result in scanned_file["variables"] and not result=="":
                                    scanned_file["variables"].append(result)
                        
                        SCANNED_FILES[scanned_file["absolute_path"]]=scanned_file
        except Exception:
            print "Unexpected error:", sys.exc_info()[0]
            print "Unexpected error:", sys.exc_info()[1]
        
    def scan_file(self, path, language):
        f = open(path)
        lines = f.readlines()
        f.close()
        for line in lines:
            print line#this is where we do language-based syntax scanning
        
    def ask_directory(self):# returns a string of the directory name
        return tkFileDialog.askdirectory(**self.dir_opt)
    
    @staticmethod    
    @post('/process')
    def my_process():
        req_obj = json.loads(request.body.read())
        # do something with req_obj
        # ...
        return 'All done'

# app= None


# print " gottoservercode"
app=Element()



