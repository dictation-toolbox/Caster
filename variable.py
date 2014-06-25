#http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
import Tkinter as tk
import tkFileDialog
import os, re, sys, json
import paths
"""
- 1 to 10 sticky list at the top
- Automatically figures out which file is open by continually scanning the top-level window and looking for something with the file extension
 - it scans an entire directory, creating an XML file for that directory, which contains the names of all imports and things which follow a single
   = operator, or other language specific traits
- It also has a drop-down box for manually switching files, and associated hotkey
- It has hotkeys for everything, and so can be voice controlled
- Each word also has a hotkey/button to delete it and to make it sticky
- It can also take the highlighted text and add it to the list




"""

SCANNED_FOLDERS_PATH=paths.get_scanned_folders_path()
SCANNED_FILES={}

GENERIC_PATTERN=re.compile("([A-Za-z0-9._]+\s*=)|(import [A-Za-z0-9._]+)")

class ScannedFile:
    def __init__(self):
        self.filename=""
        self.absolute_path=""
        self.variables=[]

class VariablesHelper:
    
    def __init__(self):
        self.all_names=[]
        self.root=tk.Tk()
        
        # setup options for directory ask
        self.dir_opt = options = {}
        options['initialdir'] = 'C:\\natlink\\natlink\\macrosystem\\'
        options['mustexist'] = False
        options['parent'] = self.root
        options['title'] = 'Please select directory'

        listbox = tk.Listbox(self.root)
        listbox.pack()
        
        listbox.insert(tk.END, "a list entry")
        
        for item in ["one", "two", "three", "four"]:
            listbox.insert(tk.END, item)
        self.root.bind_all("1", self.get_new)
        label1 = tk.Label(text="Label 1", name="label1")
        entry1 = tk.Entry(name="entry1")

        label1.pack()
        entry1.pack()
        self.root.mainloop()
    
#     def save_to_XML(self, list_of_source_files):
    
    def move_to_top(self,name):
        self.all_names.remove(name)
        self.all_names=[name]+self.all_names
        
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
        



app=VariablesHelper()