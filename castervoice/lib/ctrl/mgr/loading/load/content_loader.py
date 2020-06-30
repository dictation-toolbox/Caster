import importlib
import os
import traceback
from sys import modules as _MODULES
from sys import path

from castervoice.lib import settings, printer
from castervoice.lib.ctrl.mgr.loading.load.content_type import ContentType
from castervoice.lib.ctrl.mgr.loading.load.initial_content import FullContentSet


class ContentLoader(object):
    """
    ContentLoader loads all starter and user content when Caster starts.
    It can also reload modules by name.
    -
    Load all once when Caster starts. Afterwards, unload/reload only what is requested.
    Pass result off to GrammarManager.
    """

    def __init__(self, content_request_generator):
        self._content_request_generator = content_request_generator

    def load_everything(self, rules_config):
        # Generate all requests for both starter and user locations
        base_path = settings.SETTINGS["paths"]["BASE_PATH"]
        user_dir = settings.SETTINGS["paths"]["USER_DIR"]
        user_rules_dir = user_dir + os.sep + "rules"

        starter_content_requests = self._content_request_generator.get_all_content_modules(base_path)
        user_content_requests = self._content_request_generator.get_all_content_modules(user_dir)

        # user content should trump starter content
        path.append(user_rules_dir)
        requests = {}
        for item in starter_content_requests:
            requests[item.module_name] = item
        for item in user_content_requests:
            requests[item.module_name] = item

        # categorize requests
        rule_requests = []
        transformer_requests = []
        hook_requests = []
        for module_name in requests:
            request = requests[module_name]
            if request.content_type == ContentType.GET_RULE and \
                    rules_config.load_is_allowed(request.content_class_name):
                rule_requests.append(request)
            elif request.content_type == ContentType.GET_TRANSFORMER and \
                    request.module_name == "text_replacer":
                transformer_requests.append(request)
            elif request.content_type == ContentType.GET_HOOK:
                hook_requests.append(request)

        # attempt to load all content
        rules = self._process_requests(rule_requests)
        transformers = self._process_requests(transformer_requests)
        hooks = self._process_requests(hook_requests)

        return FullContentSet(rules, transformers, hooks)

    def idem_import_module(self, module_name, fn_name):
        """
        Returns the content requested from the specified module.
        """
        module = None
        if module_name in _MODULES:
            module = _MODULES[module_name]
            module = self._reimport_module(module)
        else:
            module = self._import_module(module_name)

        if module is None:
            return None

        # get them and add them to nexus
        fn = None
        try:
            fn = getattr(module, fn_name)
        except AttributeError:
            msg = "No method named '{}' was found on '{}'. Did you forget to implement it?".format(fn_name, module_name)
            if ContentLoader._detect_pythonpath_module_name_in_use(module):
                msg = "{} module name is already in use: {}".format(module_name, module.__file__)
            printer.out(msg)
            return None
        except:
            msg = "Error loading module '{}'."
            printer.out(msg.format(module_name))
            return None

        return fn()

    @staticmethod
    def _detect_pythonpath_module_name_in_use(module):
        not_starter = "castervoice" not in module.__file__
        not_user = ".caster" not in module.__file__
        return not_starter and not_user

    def _process_requests(self, requests):
        result = []

        for request in requests:
            if request.directory not in path:
                path.append(request.directory)
        for request in requests:
            content_item = self.idem_import_module(request.module_name, request.content_type)
            if content_item is not None:
                result.append(content_item)

        return result

    def _import_module(self, module_name):
        """
        Attempts to import a module by name.
        :param module_name: string
        :return: (module) module
        """

        try:
            load_fn = self._get_load_fn()
            return load_fn(module_name)
        except Exception as e:
            printer.out("Could not import '{}'. Module has errors: {}".format(module_name, traceback.format_exc()))
            return None

    def _reimport_module(self, module):
        """
        Reimports an already imported module. Python 2/3 compatible method.
        """

        try:
            reload_fn = self._get_reload_fn()
            return reload_fn(module)
        except:
            msg = "An error occurred while importing '{}': {}"
            printer.out(msg.format(str(module), traceback.format_exc()))
            return None

    def _get_load_fn(self):
        """Importing broken out for testability"""
        return importlib.import_module

    def _get_reload_fn(self):
        """Importing broken out for testability"""
        try:
            reload
        except NameError:
            # Python 3
            from imp import reload
        return reload
