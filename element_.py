import Tkinter as tk
import tkFileDialog
from threading import Timer
import signal
from Tkinter import (StringVar, OptionMenu, Scrollbar, Frame, Label, Entry)
import os, re, sys, json
import paths, utilities, settings

import bottle
from bottle import run, request#, post,response

"""
New Future Features List:


"""




class Element:
    def __init__(self):
       
        # setup basics
        self.JSON_PATH=paths.get_element_json_path()
        self.TOTAL_SAVED_INFO=utilities.load_json_file(self.JSON_PATH)

        self.first_run=True
        if "config" in self.TOTAL_SAVED_INFO and "last_directory" in self.TOTAL_SAVED_INFO["config"]:
            self.first_run=False
        else:
            self.TOTAL_SAVED_INFO["config"]={}
            self.TOTAL_SAVED_INFO["directories"]={}
        self.current_file=None
        self.last_file_loaded=None
        
        
        # REGULAR EXPRESSION PATTERNS
        self.GENERIC_PATTERN=re.compile("([A-Za-z0-9._]+\s*=)|(import [A-Za-z0-9._]+)")
        # python language
        self.PYTHON_IMPORTS=re.compile("((\bimport\b|\bfrom\b|\bas\b)(\(|,| )*[A-Za-z0-9._]+)")# capture group index 3
        self.PYTHON_FUNCTIONS=re.compile("(\bdef \b([A-Za-z0-9_]+)\()|(\.([A-Za-z0-9_]+)\()")# cgi 1 or 3
        self.PYTHON_VARIABLES=re.compile("(([A-Za-z0-9_]+)[ ]*=)|((\(|,| )([A-Za-z0-9_]+)(\)|,| ))")# 1 or 4
        # java language
        self.JAVA_IMPORTS=re.compile("")# don't forget things following the word "new"
        self.JAVA_METHODS=re.compile("")
        # to do: add detection for parameters in methods
        self.JAVA_VARIABLES=re.compile("([ \.]*([A-Za-z0-9_]+)[ ]*=)|((\bpublic\b|\bprivate\b|\binternal\b|\bfinal\b|\bstatic\b)[ ]+[A-Za-z0-9_]+[ ]+([A-Za-z0-9_]+)[ ]*[;=])")#1 or 4
        
        # setup tk
        self.root=tk.Tk()
        self.root.title(settings.ELEMENT_VERSION)
        self.root.geometry("200x"+str(self.root.winfo_screenheight()-100)+"-1+20")
        self.root.wm_attributes("-topmost", 1)
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)
        
        # setup hotkeys
        self.root.bind_all("<Home>", self.scan_new)
        
        
         
        # setup options for directory ask
        self.dir_opt = {}
        self.dir_opt['initialdir'] = os.environ["HOME"]+'\\'
        self.dir_opt['mustexist'] = False
        self.dir_opt['parent'] = self.root
        self.dir_opt['title'] = 'Please select directory'

        # directory drop-down label
        Label(self.root, text="Directory, File:", name="pathlabel").pack()
        
        # setup drop-down box
        self.dropdown_selected=StringVar(self.root)
        self.default_dropdown_message="Please select a scanned folder"
        self.dropdown_selected.set(self.default_dropdown_message)
        self.dropdown=OptionMenu(self.root, self.dropdown_selected, self.default_dropdown_message)
        self.dropdown.pack()
        if not self.first_run:
            self.populate_dropdown()

        # setup drop-down box for files manual selection
        self.file_dropdown_selected=StringVar(self.root)
        self.file_default_dropdown_message="Select file"
        self.file_dropdown_selected.set(self.file_default_dropdown_message)
        self.file_dropdown=OptionMenu(self.root, self.file_dropdown_selected, self.file_default_dropdown_message)
        self.file_dropdown.pack()


        # file extension label and box
        ext_frame= Frame(self.root)
        Label(ext_frame, text="Ext(s):", name="extensionlabel").pack(side=tk.LEFT)
        self.ext_box= Entry(ext_frame, name="ext_box")
        self.ext_box.pack(side=tk.LEFT)
        ext_frame.pack()

        # fill in remembered information  if it exists
        if not self.first_run:
            last_dir=self.TOTAL_SAVED_INFO["config"]["last_directory"]
            self.dropdown_selected.set(last_dir)
            self.ext_box.insert(0, ",".join(self.TOTAL_SAVED_INFO["directories"][last_dir]["extensions"]))
                
        # sticky label
        Label(text="Sticky Box", name="label1").pack()

        # setup search box
        search_frame= Frame(self.root)
        Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_box = tk.Entry(search_frame, name="search_box")
        self.search_box.pack(side=tk.LEFT)
        
        # set up lists
        stickyframe=Frame(self.root)
        stickyscrollbar =  Scrollbar(stickyframe, orient=tk.VERTICAL)
        self.sticky_listbox_numbering = tk.Listbox(stickyframe, yscrollcommand=stickyscrollbar.set)
        self.sticky_listbox_content = tk.Listbox(stickyframe, yscrollcommand=stickyscrollbar.set)

        self.sticky_listbox_index=0
        s_lbn_opt={}
        s_lbn_opt_height=10
        s_lbn_opt["height"]=s_lbn_opt_height
        s_lbn_opt["width"]=4
        s_lbn_opt2={}
        s_lbn_opt2["height"]=s_lbn_opt_height
        
        stickyscrollbar.config(command=self.sticky_scroll_lists)
        stickyscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.sticky_listbox_numbering.config(s_lbn_opt)
        self.sticky_listbox_numbering.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.sticky_listbox_content.config(s_lbn_opt2)
        self.sticky_listbox_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        stickyframe.pack()
        #-------
        search_frame.pack()
        #-------
        listframe= Frame(self.root)
        scrollbar = Scrollbar(listframe, orient=tk.VERTICAL)
        self.listbox_numbering = tk.Listbox(listframe, yscrollcommand=scrollbar.set)
        self.listbox_content = tk.Listbox(listframe, yscrollcommand=scrollbar.set)
        
        self.listbox_index=0
        lbn_opt={}
        lbn_opt_height=30
        lbn_opt["height"]=lbn_opt_height
        lbn_opt["width"]=4
        lbn_opt2={}
        lbn_opt2["height"]=lbn_opt_height
        
        scrollbar.config(command=self.scroll_lists)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_numbering.config(lbn_opt)
        self.listbox_numbering.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.listbox_content.config(lbn_opt2)
        self.listbox_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        listframe.pack()
        
        # update active file
        self.update_interval= 100
        self.filename_pattern=re.compile(r"[/\\]([\w]+\.[\w]+)")
        self.old_active_window_title=""
        self.root.after(self.update_interval, self.update_active_file)
        
        # start bottle server, tk main loop
        Timer(1, self.start_server).start()
#         self.root.after(self.interval, self.start_server)
        bottle.route('/process',method="POST")(self.process_request)
        self.root.mainloop()

    def on_exit(self):
        self.root.destroy()
        os.kill(os.getpid(), signal.SIGTERM)
    
    def start_server(self):
        run(host='localhost', port=1337, debug=True, server='cherrypy')
    
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
                self.last_file_loaded=filename

        self.root.after(self.update_interval, self.update_active_file)
    
    def rescan_directory(self):
        self.scan_directory(self.dropdown_selected.get())
        self.old_active_window_title="Directory has been rescanned"
        
            
    def scroll_to(self, index):#don't need this for sticky list
        self.scroll_lists(index)
    
    def scroll_lists(self, *args):# synchronizes  numbering list and  content list with a single scrollbar
        apply(self.listbox_numbering.yview, args)
        apply(self.listbox_content.yview, args)
    
    def sticky_scroll_lists(self, *args):
        apply(self.sticky_listbox_numbering.yview, args)
        apply(self.sticky_listbox_content.yview, args)
        
    def clear_lists(self):# used when changing files
        self.listbox_numbering.delete(0, tk.END)
        self.listbox_content.delete(0, tk.END)
        self.sticky_listbox_numbering.delete(0, tk.END)
        self.sticky_listbox_content.delete(0, tk.END)
    
    #FOR LOADING 
    
    
    
    
    def populate_list(self, file_to_activate):

        selected_directory=self.dropdown_selected.get()
        self.current_file=None
        if selected_directory==self.default_dropdown_message:
            return#  if a scanned for hasn't been selected, there's no need to go any further
        self.clear_lists()
        for absolute_path in self.TOTAL_SAVED_INFO["directories"][selected_directory]["files"]:
            if absolute_path.endswith("/"+file_to_activate) or absolute_path.endswith("\\"+file_to_activate):
                self.current_file=self.TOTAL_SAVED_INFO["directories"][selected_directory]["files"][absolute_path]
                break
        if not self.current_file==None:
            self.reload_list(self.current_file["names"],self.current_file["sticky"])
    
    def reload_list(self, namelist, stickylist):
        self.listbox_index=0# reset index upon reload
        for sticky in stickylist:
            self.add_to_stickylist(sticky)
        for name in namelist:
            self.add_to_list(name)

    def add_to_list(self, item):
        self.listbox_index+=1    
        self.listbox_numbering.insert(tk.END, str(self.listbox_index))
        self.listbox_content.insert(tk.END, item)
    
    def add_to_stickylist(self, sticky):
        self.listbox_index+=1
        self.sticky_listbox_numbering.insert(tk.END, str(self.listbox_index))
        self.sticky_listbox_content.insert(tk.END, sticky)
    
    def trigger_directory_box(self, event):
        self.dropdown.focus_set()
    
    #FOR SCANNING AND SAVING FILES    
    def scan_new(self, event):
        directory=self.ask_directory()
        if not directory=="":
            self.scan_directory(directory)
            utilities.save_json_file(self.TOTAL_SAVED_INFO, self.JSON_PATH)
            self.populate_dropdown()
            self.select_from_dropdown(directory)
            
    def select_from_dropdown(self, key, save=True):
        self.TOTAL_SAVED_INFO["config"]["last_directory"]=key
        if save:
            utilities.save_json_file(self.TOTAL_SAVED_INFO, self.JSON_PATH)
        self.dropdown_selected.set(key)
        
    def populate_dropdown(self):
        self.TOTAL_SAVED_INFO=utilities.load_json_file(self.JSON_PATH)
        menu = self.dropdown["menu"]
        menu.delete(0, tk.END)
        for key in self.TOTAL_SAVED_INFO["directories"]:
            if not key=="":
                menu.add_command(label=key, command=lambda key=key: self.select_from_dropdown(key))
        
    def get_acceptable_extensions(self):
        ext_text=self.ext_box.get().replace(" ", "")
        return ext_text.split(",")       
        
    def scan_directory(self,directory):
        
        scanned_directory={}
        acceptable_extensions=self.get_acceptable_extensions()
        
        try:
            for base, dirs, files in os.walk(directory):# traverse base directory, and list directories as dirs and files as files
                utilities.report(base)
                for fname in files:
                    extension="."+fname.split(".")[-1]
                    if extension in acceptable_extensions:
                        absolute_path=base+"/"+fname
                        
                        # check for old information on the same file, save it if it exists
                        old_sticky_list=[]
                        old_added_list=[]
                        if "directories" in self.TOTAL_SAVED_INFO:
                            if base in self.TOTAL_SAVED_INFO["directories"]:
                                if absolute_path in self.TOTAL_SAVED_INFO["directories"][base]["files"]:
                                    old_sticky_list=self.TOTAL_SAVED_INFO["directories"][base]["files"][absolute_path]["sticky"]
                                    old_added_list=self.TOTAL_SAVED_INFO["directories"][base]["files"][absolute_path]["added"]

                        
                        # set up dictionary for new scan      
                        scanned_file={}
                        scanned_file["filename"]=fname
                        scanned_file["names"]=[]
                        scanned_file["sticky"]=["","","","","","","","","",""]
                        scanned_file["added"]=[]
                        
                        # add old sticky list back in
                        if len(filter(lambda i: not i=="",old_sticky_list))>0:# if there are any nonblank values in old_sticky_list
                            scanned_file["sticky"]=old_sticky_list
                        
                        #search out imports, function names, variable names
                        f = open(base+"/"+fname, "r")
                        lines = f.readlines()
                        f.close()
                        for line in lines:
                            filter_results=self.filter(line, extension)
                            for result in filter_results:                                
                                if not (result in scanned_file["names"] or result in scanned_file["sticky"] or result in old_sticky_list) and not result=="":
                                    scanned_file["names"].append(result)
                        
                        # re-add stuff that was manually added before
                        scanned_file["added"]=old_added_list
                        for added_name in scanned_file["added"]:
                            if not (added_name in scanned_file["names"] or added_name in scanned_file["sticky"] or added_name in old_sticky_list) and not added_name=="":
                                scanned_file["names"].append(added_name)
                        
                        
                        scanned_file["names"].sort()
                        scanned_directory[absolute_path]=scanned_file
        except Exception:
            utilities.report(utilities.list_to_string(sys.exc_info()))
        meta_information={}
        meta_information["files"]=scanned_directory
        meta_information["extensions"]=acceptable_extensions
        self.TOTAL_SAVED_INFO["directories"][directory]=meta_information
        
    def filter(self, line, extension):
        #  handle the case that a regular expression hasn't been made  for this language yet
        if not extension in [".py",".java"]:
            results=[]
            generic_match_object=self.GENERIC_PATTERN.findall(line)# for languages without specific regular expressions made yet
            if len(generic_match_object)>0:
                results=self.process_match(generic_match_object, [0], results)
            return results
        
        # setup        
        import_match_object=None
        function_match_object=None
        variable_match_object=None
        import_indices=None
        function_indices=None
        variable_indices=None
        
        # Python        
        if extension==".py":
            import_match_object=self.PYTHON_IMPORTS.findall( line )
            function_match_object=self.PYTHON_FUNCTIONS.findall( line )
            variable_match_object=self.PYTHON_VARIABLES.findall( line )
            import_indices=[3]
            function_indices=[1,3]
            variable_indices=[1,4]
        elif extension==".java":
            import_match_object=self.JAVA_IMPORTS.findall( line )
            function_match_object=self.JAVA_METHODS.findall( line )
            variable_match_object=self.JAVA_VARIABLES.findall( line )
            import_indices=[]
            function_indices=[]
            variable_indices=[1,4]
        
        results=[]
        if len(import_match_object)>0:
                results=self.process_match(import_match_object, import_indices, results)
        if len(function_match_object)>0:
                results=self.process_match(function_match_object, function_indices, results)
        if len(variable_match_object)>0:
            results=self.process_match(variable_match_object, variable_indices, results)
        return results
    
    def process_match(self, match_object, desired_indices, results):
        for match_tuple in match_object:
            for index in desired_indices:
                match=match_tuple[index]
                if not (match=="" or match.isdigit() or match in results):
                    results.append(match)
        return results
        
         
    def ask_directory(self):# returns a string of the directory name
        return tkFileDialog.askdirectory(**self.dir_opt)
    
    def process_request(self):
        request_object = json.loads(request.body.read())
        action_type=request_object["action_type"]
        if self.current_file==None and (not action_type in ["extensions","trigger_directory_box","scan_new"]):#only these are allowed when no file is loaded
            return "No file is currently loaded."
        if "index" in request_object:
            index=int(request_object["index"])
            if action_type=="scroll":
                if index<self.listbox_content.size():
                    self.root.after(10, lambda: self.scroll_to(index-10))# now thread safe
                return "c"
            elif action_type=="retrieve":
                index_plus_one=index+1
                if index<10:# if sticky
                    return self.sticky_listbox_content.get(index, index_plus_one)[0]#
                else:
                    return self.listbox_content.get(index-10, index_plus_one-10)[0]
            elif action_type=="sticky":# requires sticky_index,auto_sticky regardless of what mode it's in
                sticky_index=request_object["sticky_index"]# the index of the slot on the sticky list to be overwritten
                sticky_previous=self.current_file["sticky"][sticky_index]
                if not sticky_previous=="":# if you overwrite an old sticky entry, move it back down to the unordered list
                    self.current_file["names"].append(sticky_previous)
                    self.current_file["names"].sort()
                # now, either replace the slot with a string or a word from the unordered list, first a string:                
                if not request_object["auto_sticky"]=="":
                    self.current_file["sticky"][sticky_index]=request_object["auto_sticky"]
                else:
                    index_plus_one= index+1
                    target_word=self.listbox_content.get(index-10, index_plus_one-10)[0]
                    self.current_file["sticky"][sticky_index]=target_word
                    self.current_file["names"].remove(target_word)

                utilities.save_json_file(self.TOTAL_SAVED_INFO, self.JSON_PATH)
                self.root.after(10, lambda: self.populate_list(self.last_file_loaded))
                return "c"
            elif action_type=="remove":
                index_plus_one= index+1
                target_word=None
                if index<10:
                    target_word=self.current_file["sticky"][index]
                    self.current_file["sticky"][index]=""
                else:
                    target_word=self.listbox_content.get(index-10, index_plus_one-10)[0]# unordered
                    self.current_file["names"].remove(target_word)
                if target_word in self.current_file["added"]:
                    self.current_file["added"].remove(target_word)
                utilities.save_json_file(self.TOTAL_SAVED_INFO, self.JSON_PATH)
                self.root.after(10, lambda: self.populate_list(self.last_file_loaded))
                return "c"
        elif "name" in request_object:
            self.current_file["names"].append(request_object["name"])
            self.current_file["added"].append(request_object["name"])
            self.current_file["names"].sort()
            utilities.save_json_file(self.TOTAL_SAVED_INFO, self.JSON_PATH)
            self.root.after(10, lambda: self.populate_list(self.last_file_loaded))
            return "c"
        else:
            if action_type=="search":
                self.root.after(10, self.search_box.focus_set)
            elif action_type=="extensions":
                self.root.after(10, self.ext_box.focus_set)
            elif action_type=="trigger_directory_box":
                self.root.after(10, self.dropdown.focus_set)
            elif action_type=="rescan":
                self.rescan_directory()
            return "c"
        
        return 'unrecognized request received: '+request_object["action_type"]


app=Element()  