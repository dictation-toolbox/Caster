'''
Created on Jan 26, 2019

@author: synkarius
'''
from sys import path
import importlib, os, glob
from castervoice.lib import settings
import traceback

class UserContentManager(object):
    def __init__(self):
        # self.rules = self.import_user_dir("get_rule", settings.SETTINGS["paths"]["USER_DIR"] + "/rules")
        # self.filters = self.import_user_dir("get_filter", settings.SETTINGS["paths"]["USER_DIR"] + "/filters")
        self.caster_dir = os.path.realpath(__file__).rsplit(os.path.sep + "castervoice", 1)[0].replace("\\", "/") + "/"
        self.user_dir = settings.SETTINGS["paths"]["USER_DIR"] + "/"
        path.append(self.user_dir)
        self.user_rules_loaded = []
        self.search_depth = 3

    def load_rules(self):
        self.import_dir(self.user_dir + "rules/", "rules")
        self.import_dir(self.user_dir + "filters/", "filters")
        self.import_dir(self.caster_dir + "castervoice/apps/", "castervoice.apps")
        self.import_dir(self.caster_dir + "castervoice/lib/ccr/", "castervoice.lib.ccr")

    def import_dir(self, path, namespace):
        modules = self.find_files(path)
        for lib_name in modules:
            self.import_module(namespace, lib_name)

    def find_files(self, path):
        #returns a list of Python files
        python_files = []
        for i in range(self.search_depth):
            python_files.extend(glob.glob(path + ("*/"*i) + "*.py"))
        return [
            f.replace("\\", "/").replace(path, "").replace(".py", "").replace("/", ".")
            for f in python_files
            if not f.endswith('__init__.py')]

    def import_module(self, namespace, lib_name):
        try:
            full_name = "%s.%s" % (namespace, lib_name)
            lib = importlib.import_module(full_name)
        except Exception as e:
            print("Could not load '{}'. Module has errors: {}".format(lib_name, traceback.format_exc()))

    # def import_user_dir(self, fn_name, fpath):
    #     result = []

    #     # check for existence of user dir
    #     if not os.path.isdir(fpath):
    #         msg = "No directory '{}' was found. Did you configure your USER_DIR correctly in {}?"
    #         print(msg.format(fpath, settings.get_filename()))
    #         return result
    #     path.append(fpath)

    #     # get names of all python files in dir
    #     python_files = glob.glob(fpath + "/*.py")
    #     modules = [
    #         os.path.basename(f)[:-3]
    #         for f in python_files
    #         if not f.endswith('__init__.py')
    #     ]
    #     for lib_name in modules:
    #         # try to import the user rules one by one
    #         lib = None
    #         try:
    #             lib = importlib.import_module(lib_name)
    #         except Exception as e:
    #             print("Could not load '{}'. Module has errors: {}".format(lib_name, traceback.format_exc()))
    #             continue

    #         # get them and add them to nexus
    #         fn = None
    #         try:
    #             fn = getattr(lib, fn_name)
    #         except AttributeError:
    #             msg = "No method named '{}' was found on '{}'. Did you forget to implement it?"
    #             print(msg.format(fn_name, lib_name))
    #             continue


    #         result.append(fn())

    #     return result