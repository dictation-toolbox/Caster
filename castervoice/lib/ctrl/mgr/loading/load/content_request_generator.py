import glob
import os

from castervoice.lib.ctrl.mgr.loading.load.content_request import ContentRequest
from castervoice.lib.ctrl.mgr.loading.load.content_type import ContentType


class ContentRequestGenerator(object):
    """
    Generates a set of requests from a path.
    """

    def get_all_content_modules(self, directory):
        relevant_modules = []
        for dirpath, dirnames, filenames in os.walk(directory):
            for fn in filenames:
                file_path = dirpath + os.sep + fn
                content_type = ContentRequestGenerator._get_content_type(file_path)
                if content_type is not None:
                    module_name = fn[:-3]
                    relevant_modules.append(ContentRequest(content_type, dirpath, module_name))
        return relevant_modules

    @staticmethod
    def _get_content_type(file_path):
        """
        Reads the whole file, classifies it as rule, transformer, hook, or none.
        :param file_path: str
        :return: str
        """
        if not file_path.endswith(".py"):
            return None
        if file_path.endswith("__init__.py"):
            return None

        content = None
        with open(file_path) as f:
            content = f.readlines()
        for line in content:
            if line.startswith("#"):
                continue
            rule_func = "def {}():".format(ContentType.GET_RULE)
            transformer_func = "def {}():".format(ContentType.GET_TRANSFORMER)
            hook_func = "def {}():".format(ContentType.GET_HOOK)
            if rule_func in line:
                return ContentType.GET_RULE
            if transformer_func in line:
                return ContentType.GET_TRANSFORMER
            if hook_func in line:
                return ContentType.GET_HOOK
        return None
