import os
import traceback
from sys import path as syspath

from castervoice.lib import settings, printer
from castervoice.lib.ctrl.mgr.errors.module_qualification_error import ModuleQualificationError
from castervoice.lib.ctrl.mgr.loading.load.content_root import ContentRoot
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

    def __init__(self, content_request_generator, module_load_fn, module_reload_fn, modules_accessor):
        self._content_request_generator = content_request_generator
        self._module_load_fn = module_load_fn
        self._module_reload_fn = module_reload_fn
        self._modules_accessor = modules_accessor

    def load_everything(self, rules_config):
        # Generate all requests for both starter and user locations
        base_path = settings.settings(["paths", "BASE_PATH"])
        user_dir = settings.settings(["paths", "USER_DIR"])

        starter_content_requests = self._content_request_generator.get_all_content_modules(base_path)
        user_content_requests = self._content_request_generator.get_all_content_modules(user_dir)

        # user content should trump starter content
        syspath.append(user_dir)
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

    def idem_import_module(self, request):
        """
        Returns the content requested from the specified module.
        """

        # import the module
        try:
            fully_qualified_module_name = ContentLoader._fully_qualify_module_name(request)
        except ModuleQualificationError:
            msg = "Invalid user content request path: '{}'. Skipping '{}'."
            printer.out(msg.format(request.directory, request.module_name))
            return None

        if self._modules_accessor.has_module(fully_qualified_module_name):
            module = self._modules_accessor.get_module(fully_qualified_module_name)
            module = self._reimport_module(module)
        else:
            module = self._import_module(fully_qualified_module_name)

        if module is None:
            return None

        # get them and add them to nexus
        try:
            fn = getattr(module, request.content_type)
        except AttributeError:
            msg = "No method named '{}' was found on '{}'. Did you forget to implement it?"
            printer.out(msg.format(request.content_type, request.module_name))
            return None
        except Exception as e:
            msg = "Error loading module '{}'."
            printer.out(msg.format(request.module_name))
            return None

        return fn()

    def _process_requests(self, requests):
        result = []

        for request in requests:
            content_item = self.idem_import_module(request)
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
            return self._module_load_fn(module_name)
        except Exception as e:
            printer.out("Could not import '{}'. Module has errors: {}".format(module_name, traceback.format_exc()))
            return None

    def _reimport_module(self, module):
        try:
            return self._module_reload_fn(module)
        except Exception as e:
            msg = "An error occurred while importing '{}': {}"
            printer.out(msg.format(str(module), traceback.format_exc()))
            return None

    @staticmethod
    def _fully_qualify_module_name(request):
        if ContentRoot.STARTER in request.directory:
            root = ContentRoot.STARTER
        elif ContentRoot.USER_DIR in request.directory:
            root = ContentRoot.USER_DIR
        else:
            raise ModuleQualificationError()

        tokens = request.directory.split(os.sep)
        root_index = tokens.index(root)
        tokens_for_fully_qualified_module = tokens[root_index:]
        tokens_for_fully_qualified_module.append(request.module_name)
        return ".".join(tokens_for_fully_qualified_module)
