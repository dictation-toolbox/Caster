'''
Created on Jan 26, 2019

@author: synkarius
'''

from sys import path
import importlib, os, glob
from castervoice.lib import settings

# TODO: fix accidentally deleted images... 
# TODO: check to see if the import itself launches a separate dragonfly context

class UserContentManager(object):
    
    def __init__(self):
        self.rules = self.import_user_dir("get_rule", settings.SETTINGS["USER_DIR"] + "/rules")
        self.filters = self.import_user_dir("get_filter", settings.SETTINGS["USER_DIR"] + "/filters")
        self.sikulix = None # TODO
        
#     def add_rules_to_nexus(self):
#         ''''''
#         
#     def add_rules_and_filters_to_nexus(self, merger):
#         for rule in self.rules:
#             mer
#         for rule_filter in self.filters:
#             merger.add_filter(rule_filter)

    def import_user_dir(self, fn_name, fpath):
        result = []
        
        # check for existence of user dir
        if not os.path.isdir(fpath):
            msg = "No directory '{}' was found. Did you configure your USER_DIR correctly?"
            print(msg.format(fpath))
            return result
        path.append(fpath)
        
        # get names of all python files in dir
        python_files = glob.glob(fpath + "/*.py")
        modules = [
            os.path.basename(f)[:-3]
            for f in python_files
            if not f.endswith('__init__.py')
        ]
        for lib_name in modules:
            # try to import the user rules one by one
            lib = None
            try:
                lib = importlib.import_module(lib_name)
            except Exception as e:
                print("Could not load '{}'. Module has errors: {}".format(lib_name, e))
                return None
            
            # get them and add them to nexus
            fn = None
            try:
                fn = getattr(lib, fn_name)
            except AttributeError:
                msg = "No method named '{}' was found on '{}'. Did you forget to implement it?"
                print(msg.format(fn_name, lib_name))
                return None
            
            
            result.append(fn())
    
        return result