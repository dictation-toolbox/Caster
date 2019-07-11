import importlib
import traceback
from sys import modules as MODULES
from sys import path

from castervoice.lib import settings
from castervoice.lib.ctrl.mgr.loading.content_type import ContentType
from castervoice.lib.ctrl.mgr.loading.initial_content import FullContentSet


class ContentLoader(object):

    def __init__(self, content_request_generator):
        self._content_request_generator = content_request_generator

    '''
    ContentLoader loads all starter and user content when Caster starts.
    It can also reload modules by name.
    -
    Load all once when Caster starts. Afterwards, unload/reload only what is requested.
    Pass result off to GrammarManager.
    '''

    def load_everything(self):

        # Generate all requests for both starter and user locations
        base_path = settings.SETTINGS["paths"]["BASE_PATH"]
        user_dir = settings.SETTINGS["paths"]["USER_DIR"]

        rule_requests = self._content_request_generator.generate(ContentType.GET_RULE,
                                                                 base_path + "/TODO_THIS_PATH --- the CCR RULES path",
                                                                 base_path + "/TODO_THIS_PATH --- the APP rules path",
                                                                 user_dir + "/user_rules")
        transformer_requests = self._content_request_generator.generate(ContentType.GET_TRANSFORMER,
                                                                        base_path + "/TODO_THIS_PATH",
                                                                        user_dir + "/user_transformers")
        hook_requests = self._content_request_generator.generate(ContentType.GET_HOOK,
                                                                 base_path + "/TODO_THIS_PATH",
                                                                 user_dir + "/user_hooks")

        '''Attempt loading all content'''
        rules = self._process_requests(rule_requests)
        transformers = self._process_requests(transformer_requests)
        hooks = self._process_requests(hook_requests)

        return FullContentSet(rules, transformers, hooks)

    def idem_import_module(self, module_name, fn_name):
        '''
        Returns the content requested from the specified module.
        '''
        module = None
        if module_name in MODULES:
            module = MODULES[module_name]
            module = self._reimport_module(module)
        else:
            module = self._import_module(module_name, fn_name)

        if module is None:
            return None

        # get them and add them to nexus
        fn = None
        try:
            fn = getattr(module, fn_name)
        except AttributeError:
            msg = "No method named '{}' was found on '{}'. Did you forget to implement it?"
            print(msg.format(fn_name, module_name))
            return None

        return fn()

    def _process_requests(self, requests):
        result = []

        for request in requests:
            if request.directory not in path:
                path.append(request.directory)
            content_item = self.idem_import_module(request.module_name, request.content_type)
            if content_item is not None:
                result.append(content_item)

        return result

    def _import_module(self, module_name):
        '''
        Imports a module for the first time.
        '''
        try:
            return importlib.import_module(module_name)
        except Exception as e:
            print("Could not import '{}'. Module has errors: {}".format(module_name, traceback.format_exc()))
            return None

    def _reimport_module(self, module):
        '''
        Reimports an already imported module. Python 2/3 compatible method.
        '''
        try:
            reload
        except NameError:
            # Python 3
            from imp import reload

        reloaded_module = None
        try:
            reloaded_module = reload(module)
        except:
            msg = "An error occurred while importing '{}': {}"
            print(msg.format(str(module), traceback.format_exc()))
            return None

        return reloaded_module
