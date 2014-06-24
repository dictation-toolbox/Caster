#http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
import Tkinter as tk
import tkFileDialog
import os
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
    
    def move_to_top(self,name):
        self.all_names.remove(name)
        self.all_names=[name]+self.all_names
        
    def get_new(self,event):
        self.scan_directory(self.ask_directory())
        
    def scan_directory(self,directory):
        acceptable_extensions=[".py"]# this is hardcoded for now, will read from a box later
        for base, dirs, files in os.walk(directory):# traverse base directory, and list directories as dirs and files as files
            path = base.split('/')
            print (len(path) - 1) *'---' , os.path.basename(base)       
            for file in files:
                extension="."+file.split(".")[-1]
                if extension in acceptable_extensions:
                    print len(path)*'---', file
                
    def scan_file(self, path, language):
        f = open(path)
        lines = f.readlines()
        f.close()
        for line in lines:
            print line#this is where we do language-based syntax scanning
        
    def ask_directory(self):# returns a string of the directory name
        return tkFileDialog.askdirectory(**self.dir_opt)
        



app=VariablesHelper()