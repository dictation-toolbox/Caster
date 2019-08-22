import datetime
import importlib
import traceback
from sys import modules as MODULES
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

    def load_everything(self):
        # Generate all requests for both starter and user locations
        base_path = settings.SETTINGS["paths"]["BASE_PATH"]
        user_dir = settings.SETTINGS["paths"]["USER_DIR"]

        starter_content_requests = self._content_request_generator.get_all_content_modules(base_path)
        user_content_requests = self._content_request_generator.get_all_content_modules(user_dir)

        # user content should trump starter content
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
            if request.content_type == ContentType.GET_RULE:
                rule_requests.append(request)
            elif request.content_type == ContentType.GET_TRANSFORMER:
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
        if module_name in MODULES:
            module = MODULES[module_name]
            module = self._reimport_module(module)
        else:
            module = self._import_module(module_name)  # , fn_name

        if module is None:
            return None

        # get them and add them to nexus
        fn = None
        try:
            fn = getattr(module, fn_name)
        except AttributeError:
            msg = "No method named '{}' was found on '{}'. Did you forget to implement it?"
            printer.out(msg.format(fn_name, module_name))
            return None
        except:
            msg = "Error loading module '{}'."
            printer.out(msg.format(module_name))
            return None

        return fn()

    def _process_requests(self, requests):
        result = []

        for request in requests:
            print("log {} {} {}".format(1, datetime.datetime.today(), request.module_name))
            if request.directory not in path:
                path.append(request.directory)
            content_item = self.idem_import_module(request.module_name, request.content_type)
            if content_item is not None:
                result.append(content_item)
            print("log {} {} {}".format(2, datetime.datetime.today(), request.module_name))

        return result

    def _import_module(self, module_name):
        """
        Attempts to import a module by name.
        :param module_name: string
        :return: (module) module
        """

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
