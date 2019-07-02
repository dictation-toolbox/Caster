'''
Created on Jan 26, 2019

@author: synkarius
'''
from sys import path
import importlib, os, glob, shutil
from castervoice.lib import settings
import traceback

from os.path import isdir, walk, join


def copy_filters():
    filter_user = os.path.join(settings.SETTINGS["paths"]["USER_DIR"], "filters/examples")
    if os.path.isdir(os.path.join(filter_user)) is False:
        filter_example = settings.SETTINGS["paths"]["FILTER_RULES_DEFAULTS_PATH"]
        shutil.copytree(filter_example, filter_user)


copy_filters()


def copy_rules():
    rules_user = os.path.join(settings.SETTINGS["paths"]["USER_DIR"], "rules/examples")
    if os.path.isdir(os.path.join(rules_user)) is False:
        rules_example = settings.SETTINGS["paths"]["RULES_RULES_DEFAULTS_PATH"]
        shutil.copytree(rules_example, rules_user)


copy_rules()


class UserContentManager(object):
    def __init__(self):
        # self.rules = self.import_user_dir("get_rule", settings.SETTINGS["paths"]["USER_DIR"] + "/rules")
        # self.filters = self.import_user_dir("get_filter", settings.SETTINGS["paths"]["USER_DIR"] + "/filters")
        self.caster_dir = os.path.realpath(__file__).rsplit(os.path.sep + "castervoice", 1)[0].replace("\\", "/")
        self.user_dir = settings.SETTINGS["paths"]["USER_DIR"]
        path.append(self.user_dir)
        self.ignore = ["__init__"]
        self.search_depth = 4

    def load_rules(self):
        self.import_dir(join(self.user_dir, "rules"), "rules", user=True)
        self.import_dir(join(self.user_dir, "filters"), "filters")
        self.import_dir(join(self.caster_dir, "castervoice", "apps"), "castervoice.apps")
        self.import_dir(join(self.caster_dir, "castervoice", "lib", "ccr"), "castervoice.lib.ccr")

    def import_dir(self, path, namespace, user=False):
        if user:
            walk(path, self.gen_inits, None)
        modules = self.find_files(path, user)
        for lib_name in modules:
            self.import_module(namespace, lib_name)

    def find_files(self, path, user=False):
        #returns a list of Python files
        python_files = []
        for i in range(self.search_depth):
            python_files.extend(glob.glob(join(path, (("*" + os.path.sep)*i), "*.py")))
        modules = [
            f.replace(path + os.path.sep, "").replace(".py", "").replace(os.path.sep, ".")
            for f in python_files
            if not self.should_ignore(f)]
        if user:
            names = [f.rsplit(".", 1)[-1] for f in modules]
            self.ignore.extend(names)
        return modules

    def import_module(self, namespace, lib_name):
        try:
            full_name = "%s.%s" % (namespace, lib_name)
            lib = importlib.import_module(full_name)
        except Exception as e:
            print("Could not load '{}'. Module has errors: {}".format(lib_name, traceback.format_exc()))

    def should_ignore(self, filename):
        for match in self.ignore:
            if filename.endswith("%s.py" % match):
                return True
        if os.path.sep + "examples" in filename:
            return True
        else:
            return False

    def gen_inits(self, arg, dirname, fnames):
        if not "__init__.py" in fnames:
            print "Created __init__.py in : %s" % dirname
            with open(join(dirname, "__init__.py"), 'a+') as f:
                    f.write('')


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