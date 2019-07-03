'''
Created on Jan 26, 2019

@author: synkarius
'''
from sys import path
import importlib, os, glob, shutil
from castervoice.lib import settings
import traceback

from os.path import isdir, walk, join

class UserContentManager(object):
    def __init__(self):
        self.caster_dir = settings.SETTINGS["paths"]["BASE_PATH"]
        self.user_dir = settings.SETTINGS["paths"]["USER_DIR"]
        path.append(self.user_dir)
        self.ignore = ["__init__"]
        self.search_depth = 4
        self.copy_examples()

    def load_rules(self):
        self.import_dir(join(self.user_dir, "rules"), "rules", user=True)
        self.import_dir(join(self.user_dir, "filters"), "filters")
        self.import_dir(join(self.caster_dir, "apps"), "castervoice.apps")
        self.import_dir(join(self.caster_dir, "lib", "ccr"), "castervoice.lib.ccr")
        self.import_dir(join(self.caster_dir, "lib", "dev"), "castervoice.lib.dev")
        # Imported from _caster for now
        # self.import_module("castervoice.asynch.sikuli", "sikuli")
        self.import_module("castervoice.asynch", "_hmc")

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

    def copy_examples(self):
        filter_target = os.path.join(self.user_dir, "filters", "examples")
        if not isdir(filter_target):
            filter_source = settings.SETTINGS["paths"]["FILTER_EXAMPLES_PATH"]
            shutil.copytree(filter_source, filter_target)

        rule_target = os.path.join(self.user_dir, "rules", "examples")
        if not isdir(rule_target):
            rules_source = settings.SETTINGS["paths"]["RULE_EXAMPLES_PATH"]
            shutil.copytree(rules_source, rule_target)
