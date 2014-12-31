from Tkinter import (StringVar, OptionMenu, Scrollbar, Frame, Label, Entry)
import os, re, sys, json
import signal
from threading import Timer
import tkFileDialog
import tkFont

BASE_PATH = r"C:\NatLink\NatLink\MacroSystem"
if BASE_PATH not in sys.path:
    sys.path.append(BASE_PATH)
from bottle import run, request  # , post,response
import bottle

import Tkinter as tk
from lib import  settings, utilities


ELEMENT_LISTENING_PORT = 1337



class Element:
    def __init__(self):
        self.setup_regexes()
        self.setup_UI()
         
        # update active file
        self.update_interval = 100
        self.filename_pattern = re.compile(r"[/\\]([\w]+\.[\w]+)")
        self.old_active_window_title = ""
        self.root.after(self.update_interval, self.update_active_file)
         
        # start bottleserver server, tk main loop
        Timer(1, self.start_server).start()
        bottle.route('/process', method="POST")(self.process_request)
        self.root.mainloop()
    
    def setup_regexes(self):
        self.GENERIC_PATTERN = re.compile("([A-Za-z0-9._]+\s*=)|(import [A-Za-z0-9._]+)")
        # python language
        self.PYTHON_IMPORTS = re.compile("((\bimport\b|\bfrom\b|\bas\b)(\(|,| )*[A-Za-z0-9._]+)")  # capture group index 3
        self.PYTHON_FUNCTIONS = re.compile("(\bdef \b([A-Za-z0-9_]+)\()|(\.([A-Za-z0-9_]+)\()")  # cgi 1 or 3
        self.PYTHON_VARIABLES = re.compile("(([A-Za-z0-9_]+)[ ]*=)|((\(|,| )([A-Za-z0-9_]+)(\)|,| ))")  # 1 or 4
        # java language
        self.JAVA_IMPORTS = re.compile("import [A-Za-z0-9_\\.]+\.([A-Za-z0-9_]+);|throws ([A-Za-z0-9_]+)|new ([A-Za-z0-9_<>]+)|([A-Za-z0-9_]+)\.")
        self.JAVA_METHODS = re.compile("[ \.]([A-Za-z0-9_]+)\(")
        self.JAVA_VARIABLES = re.compile("([ \.]*([A-Za-z0-9_]+)[ ]*=)|((\bpublic\b|\bprivate\b|\binternal\b|\bfinal\b|\bstatic\b)[ ]+[A-Za-z0-9_]+[ ]+([A-Za-z0-9_]+)[ ]*[;=])|(([A-Za-z0-9_]+)[ ]*[,\)])")  # 1,4,6
        
    
    def on_exit(self):
        self.root.destroy()
        os.kill(os.getpid(), signal.SIGTERM)
    
    def start_server(self):
        global ELEMENT_LISTENING_PORT
        run(host='localhost', port=ELEMENT_LISTENING_PORT, debug=False, server='cherrypy')  # bottle is about a full second faster
        
        
    
    def update_active_file(self):
        active_window_title = utilities.get_active_window_title()
        if not self.old_active_window_title == active_window_title:
            
            filename = ""
            
            match_objects = self.filename_pattern.findall(active_window_title)
            if not len(match_objects) == 0:  # if we found variable name in the line
                filename = match_objects[0]
             
            if not filename == "":
                self.old_active_window_title = active_window_title  # only update were on a new file, not just a new window
                self.populate_list(filename)
                self.last_file_loaded = filename

        self.root.after(self.update_interval, self.update_active_file)
    
    def rescan_directory(self):
        self.scan_directory(self.dropdown_selected.get())
        self.old_active_window_title = "Directory has been rescanned"
        settings.save_json_file(self.TOTAL_SAVED_INFO, self.JSON_PATH)
        
            
    def scroll_to(self, index):  # don't need this for sticky list
        self.scroll_lists(index)
    
    def scroll_lists(self, *args):  # synchronizes  numbering list and  content list with a single scrollbar
        apply(self.listbox_numbering.yview, args)
        apply(self.listbox_content.yview, args)
    
    def sticky_scroll_lists(self, *args):
        apply(self.sticky_listbox_numbering.yview, args)
        apply(self.sticky_listbox_content.yview, args)
        
    def clear_lists(self):  # used when changing files
        self.listbox_numbering.delete(0, tk.END)
        self.listbox_content.delete(0, tk.END)
        self.sticky_listbox_numbering.delete(0, tk.END)
        self.sticky_listbox_content.delete(0, tk.END)
    
    # FOR LOADING 
    
    def populate_list(self, file_to_activate):
        # get the selected directory
        selected_directory = self.dropdown_selected.get()
        if selected_directory == self.default_dropdown_message:
            return  #  if a scanned directory hasn't been selected, there's no need to go any further
        
        # check to see if the focused file in the active window is among those scanned in the selected directory
        # -- if it is, set it to self.current_file
        self.current_file = None
        for absolute_path in self.TOTAL_SAVED_INFO["directories"][selected_directory]["files"]:
            if absolute_path.endswith("/" + file_to_activate) or absolute_path.endswith("\\" + file_to_activate):
                self.current_file = self.TOTAL_SAVED_INFO["directories"][selected_directory]["files"][absolute_path]
                break
        
        # update accordingly
        self.clear_lists()
        if not self.current_file == None:
            self.reload_list(self.current_file["names"], self.current_file["sticky"])
    
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
    
    def add_to_stickylist(self, sticky):
        self.listbox_index += 1
        self.sticky_listbox_numbering.insert(tk.END, str(self.listbox_index))
        self.sticky_listbox_content.insert(tk.END, sticky)
    
    def trigger_directory_box(self, event):
        self.dropdown.focus_set()
    
    # FOR SCANNING AND SAVING FILES    
    def scan_new(self, event):
        directory = self.ask_directory()
        if not directory == "":
            self.scan_directory(directory)
            settings.save_json_file(self.TOTAL_SAVED_INFO, self.JSON_PATH)
            self.populate_dropdown()
            self.select_from_dropdown(directory)
            
    def select_from_dropdown(self, key, save=True):
        self.TOTAL_SAVED_INFO["config"]["last_directory"] = key
        
        if save:
            settings.save_json_file(self.TOTAL_SAVED_INFO, self.JSON_PATH)
        self.dropdown_selected.set(key)
        self.ext_box.delete(0, tk.END)
        self.ext_box.insert(0, ",".join(self.TOTAL_SAVED_INFO["directories"][key]["extensions"]))
        self.clear_lists()
        
    def populate_dropdown(self):
        self.TOTAL_SAVED_INFO = settings.load_json_file(self.JSON_PATH)
        menu = self.dropdown["menu"]
        menu.delete(0, tk.END)
        for key in self.TOTAL_SAVED_INFO["directories"]:
            if not key == "":
                menu.add_command(label=key, command=lambda key=key: self.select_from_dropdown(key))
        
    def get_acceptable_extensions(self):
        ext_text = self.ext_box.get().replace(" ", "")
        return ext_text.split(",")       
        
    def scan_directory(self, directory):
        
        scanned_directory = {}
        acceptable_extensions = self.get_acceptable_extensions()
        
        try:
            for base, dirs, files in os.walk(directory):  # traverse base directory, and list directories as dirs and files as files
#                 utilities.report(base)
                for fname in files:
                    extension = "." + fname.split(".")[-1]
                    if extension in acceptable_extensions:
                        absolute_path = base + "/" + fname
                        
                        # check for old information on the same file, save it if it exists
                        self.old_sticky_list = []
                        self.old_added_list = []
                        self.old_banned_list = []
                        if "directories" in self.TOTAL_SAVED_INFO:
                            if absolute_path in self.TOTAL_SAVED_INFO["directories"][directory]["files"]:
                                self.old_sticky_list = self.TOTAL_SAVED_INFO["directories"][directory]["files"][absolute_path]["sticky"]
                                self.old_added_list = self.TOTAL_SAVED_INFO["directories"][directory]["files"][absolute_path]["added"]
                                self.old_banned_list = self.TOTAL_SAVED_INFO["directories"][directory]["files"][absolute_path]["banned"]

                        
                        # set up dictionary for new scan      
                        scanned_file = {}
                        scanned_file["filename"] = fname
                        scanned_file["names"] = []
                        scanned_file["sticky"] = ["", "", "", "", "", "", "", "", "", ""]
                        scanned_file["added"] = self.old_added_list
                        scanned_file["banned"] = self.old_banned_list
                        if len(filter(lambda i: not i == "", self.old_sticky_list)) > 0:  # if there are any nonblank values in old_sticky_list
                            scanned_file["sticky"] = self.old_sticky_list
                        
                        # search out imports, function names, variable names
                        f = open(base + "/" + fname, "r")
                        lines = f.readlines()
                        f.close()
                        for line in lines:
                            filter_results = self.filter_words(line, extension)
                            for result in filter_results:
                                if self.passes_battery_of_tests(result, scanned_file, check_banlist=True):
                                    scanned_file["names"].append(result)
                        
                        # re-add stuff that was manually added before, The added list can override the ban list
                        for added_name in scanned_file["added"]:
                            if self.passes_battery_of_tests(result, scanned_file):
                                scanned_file["names"].append(added_name)
                        
                        
                        scanned_file["names"].sort()
                        scanned_directory[absolute_path] = scanned_file
        except Exception:
            utilities.simple_log(True)
        
        
        meta_information = {}
        meta_information["files"] = scanned_directory
        meta_information["extensions"] = acceptable_extensions
        self.TOTAL_SAVED_INFO["directories"][directory] = meta_information
        
    def filter_words(self, line, extension):
        #  handle the case that a regular expression hasn't been made  for this language yet
        if not extension in [".py", ".java"]:
            results = []
            generic_match_object = self.GENERIC_PATTERN.findall(line)  # for languages without specific regular expressions made yet
            if len(generic_match_object) > 0:
                results = self.process_match(generic_match_object, [0], results)
            return results
        
        # setup        
        import_match_object = None
        function_match_object = None
        variable_match_object = None
        import_indices = None
        function_indices = None
        variable_indices = None
        
        # determine language and set up regular expressions        
        if extension == ".py":
            import_match_object = self.PYTHON_IMPORTS.findall(line)
            function_match_object = self.PYTHON_FUNCTIONS.findall(line)
            variable_match_object = self.PYTHON_VARIABLES.findall(line)
            import_indices = [3]
            function_indices = [1, 3]
            variable_indices = [1, 4]
        elif extension == ".java":
            import_match_object = self.JAVA_IMPORTS.findall(line)
            function_match_object = self.JAVA_METHODS.findall(line)
            variable_match_object = self.JAVA_VARIABLES.findall(line)
            import_indices = [0, 1, 2, 3]
            function_indices = [0]
            variable_indices = [1, 4, 6]
        
        results = []
        if len(import_match_object) > 0:
            results = self.process_match(import_match_object, import_indices, results)
        if len(function_match_object) > 0:
            results = self.process_match(function_match_object, function_indices, results)
        if len(variable_match_object) > 0:
            results = self.process_match(variable_match_object, variable_indices, results)
        return results
    
    def process_match(self, match_object, desired_indices, results):
        for m in match_object:
            if isinstance(m, tuple):
                for index in desired_indices:
                    match = m[index]
                    if not (match == "" or match.isdigit() or match in results):
                        results.append(match)
            elif isinstance(m, str):
                results.append(m)
        return results
    
    def passes_battery_of_tests(self, word, scanned_file, check_banlist=False):
        # short words can be gotten faster by just spelling them
        too_short = len(word) < 4
        already_in_names = word in scanned_file["names"]
        already_in_sticky = word in scanned_file["sticky"]
        is_empty = word == ""
        is_banned = False
        if check_banlist:
            is_banned = word in scanned_file["banned"]
        if not (already_in_names or already_in_sticky or is_empty or is_banned or too_short):
            return True
        else:
            return False
         
    def ask_directory(self):  # returns a string of the directory name
        return tkFileDialog.askdirectory(**self.dir_opt)
    
    def process_request(self):
        request_object = json.loads(request.body.read())
        action_type = request_object["action_type"]
        if action_type == "kill":
            self.on_exit()
        if self.current_file == None and (not action_type in ["extensions", "trigger_directory_box", "rescan", "scan_new", "search"]):  # only these are allowed when no file is loaded
            return "No file is currently loaded."
        if "index" in request_object:
            index = int(request_object["index"])
            if action_type == "scroll":
                if index < self.listbox_content.size():
                    self.root.after(10, lambda: self.scroll_to(index - 10))  # now thread safe
                return "c"
            elif action_type == "retrieve":
                index_plus_one = index + 1
                if index < 10:  # if sticky
                    return self.sticky_listbox_content.get(index, index_plus_one)[0]  #
                else:
                    return self.listbox_content.get(index - 10, index_plus_one - 10)[0]
            elif action_type == "sticky":  # requires sticky_index,auto_sticky regardless of what mode it's in
                sticky_index = request_object["sticky_index"]  # the index of the slot on the sticky list to be overwritten
                sticky_previous = self.current_file["sticky"][sticky_index]
                if not sticky_previous == "":  # if you overwrite an old sticky entry, move it back down to the unordered list
                    self.current_file["names"].append(sticky_previous)
                    self.current_file["names"].sort()
                # now, either replace the slot with a string or a word from the unordered list, first a string:                
                if not request_object["auto_sticky"] == "":
                    self.current_file["sticky"][sticky_index] = request_object["auto_sticky"]
                else:
                    index_plus_one = index + 1
                    target_word = self.listbox_content.get(index - 10, index_plus_one - 10)[0]
                    self.current_file["sticky"][sticky_index] = target_word
                    self.current_file["names"].remove(target_word)

                settings.save_json_file(self.TOTAL_SAVED_INFO, self.JSON_PATH)
                self.root.after(10, lambda: self.populate_list(self.last_file_loaded))
                return "c"
            elif action_type == "remove":
                index_plus_one = index + 1
                target_word = None
                if index < 10:
                    target_word = self.current_file["sticky"][index]
                    self.current_file["sticky"][index] = ""
                else:
                    target_word = self.listbox_content.get(index - 10, index_plus_one - 10)[0]  # unordered
                    self.current_file["names"].remove(target_word)
                if target_word in self.current_file["added"]:
                    self.current_file["added"].remove(target_word)
                self.current_file["banned"].append(target_word)
                settings.save_json_file(self.TOTAL_SAVED_INFO, self.JSON_PATH)
                self.root.after(10, lambda: self.populate_list(self.last_file_loaded))
                return "c"
        elif "name" in request_object:
            self.current_file["names"].append(request_object["name"])
            self.current_file["added"].append(request_object["name"])
            self.current_file["names"].sort()
            settings.save_json_file(self.TOTAL_SAVED_INFO, self.JSON_PATH)
            self.root.after(10, lambda: self.populate_list(self.last_file_loaded))
            return "c"
        else:
            if action_type == "search":
                self.root.after(10, lambda: self.search(request_object["word"]))
#                 self.root.after(10, self.search_box.focus_set)
            elif action_type == "extensions":
                self.root.after(10, self.ext_box.focus_set)
            elif action_type == "trigger_directory_box":
                self.root.after(10, self.dropdown.focus_set)
            elif action_type == "rescan":
                self.rescan_directory()
            elif action_type == "filter_strict_request_for_data":
                return json.dumps(self.TOTAL_SAVED_INFO["directories"][self.dropdown_selected.get()])
            elif action_type == "filter_strict_return_processed_data":
                self.TOTAL_SAVED_INFO["directories"][self.dropdown_selected.get()] = json.loads(request_object["processed_data"])
                self.old_active_window_title = "Directory has been strict- modified"
                settings.save_json_file(self.TOTAL_SAVED_INFO, self.JSON_PATH)
            return "c"
        
        return 'unrecognized request received: ' + request_object["action_type"]
    
    def search(self, word):
        ''''''
        # get index
        all_symbols = self.listbox_content.get(0, self.listbox_content.size())
        high_score = [0, 0]
        # high_score = index, score
        for i in range(0, self.listbox_content.size()):
            
#             print all_symbols[i] == word, all_symbols[i], ", ", word, i
            score = self.word_similarity_score(all_symbols[i], word)
            print "comparing " + all_symbols[i], score
            if score > high_score[1]:
                high_score = [i, score]
                if score == len(word):
                    break
    
        # scroll and select
        self.scroll_to(high_score[0])
        self.listbox_numbering.selection_set(high_score[0])
    
    def word_similarity_score(self, w1, w2):
        smaller_len = len(w1)
        w2_len = len(w2)
        if w2_len < smaller_len:
            smaller_len = w2_len
        score = 0
        for i in range(0, smaller_len):
            if w1[i] == w2[i]:
                score += 1
            else:
                return score
        return score
    
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
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.customFont = tkFont.Font(family="Helvetica", size=8)
        
        # setup hotkeys
        self.root.bind_all("<Home>", self.scan_new)
          
        # setup options for directory ask
        self.dir_opt = {}
        self.dir_opt['initialdir'] = os.environ["HOME"] + '\\'
        self.dir_opt['mustexist'] = False
        self.dir_opt['parent'] = self.root
        self.dir_opt['title'] = 'Please select directory'
         
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
    
