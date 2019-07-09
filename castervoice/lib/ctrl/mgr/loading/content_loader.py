'''
Attempts to de-import and re-import a Python file with
a MappingRule or MergeRule in it.
'''
import importlib, os, glob
from sys import path
import traceback
from castervoice.lib import settings
from castervoice.lib.ctrl.mgr.loading.initial_content import FullContentSet

class ContentLoader(object):
    
    '''
    Load all once when Caster starts. Afterwards, unload/reload only what is requested.
    Pass result off to GrammarManager.
    '''
    def load_everything(self):
        rules = []
        transformers = []
        hooks = []
        
        '''
        Starter Caster Content
        '''
        base_path = settings.SETTINGS["paths"]["BASE_PATH"]
        
        rules.extend(self.import_directory("get_rule", base_path + "/TODO_THIS_PATH --- the CCR RULES path"))
        rules.extend(self.import_directory("get_rule", base_path + "/TODO_THIS_PATH --- the APP rules path"))
        transformers.extend(self.import_directory("get_transformer", base_path + "/TODO_THIS_PATH"))
        hooks.extend(self.import_directory("get_hook", base_path + "/TODO_THIS_PATH"))
        
        '''
        User Content -- should come later to override starter content
        '''
        user_dir = settings.SETTINGS["paths"]["USER_DIR"]
        
        rules.extend(self.import_directory("get_rule", user_dir + "/rules"))
        transformers.extend(self.import_directory("get_transformer", user_dir + "/transformers"))
        hooks.extend(self.import_directory("get_hook", user_dir + "/hooks"))
        
        return FullContentSet(rules, transformers, hooks)
        
    def import_file(self, lib_name, fn_name):
        lib = None
        try:
            lib = importlib.import_module(lib_name)
        except Exception as e:
            print("Could not load '{}'. Module has errors: {}".format(lib_name, traceback.format_exc()))
            return None
        
        # get them and add them to nexus
        fn = None
        try:
            fn = getattr(lib, fn_name)
        except AttributeError:
            msg = "No method named '{}' was found on '{}'. Did you forget to implement it?"
            print(msg.format(fn_name, lib_name))
            return None
        
        return fn()
    
    '''TODO'''
    def unimport_file(self, lib_name):
        pass
    
    def import_directory(self, fn_name, fpath):
        result = []
        
        # check for existence of user dir
        if not os.path.isdir(fpath):
            msg = "No directory '{}' was found. Did you configure your USER_DIR correctly in {}?"
            print(msg.format(fpath, settings.get_filename()))
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
            lib = self.import_file(lib_name, fn_name)
            if lib is not None:
                result.append(lib)
    
        return result