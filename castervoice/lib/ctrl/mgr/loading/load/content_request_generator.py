import glob
import os

from castervoice.lib.ctrl.mgr.loading.load.content_request import ContentRequest
from castervoice.lib.ctrl.mgr.loading.load.content_type import ContentType


class ContentRequestGenerator(object):
    """
    Generates a set of requests from a path.
    """

    @staticmethod
    def get_all_content_modules(directory):
        relevant_modules = []
        for dirpath, dirnames, filenames in os.walk(directory):
            for fn in filenames:
                file_path = dirpath + os.linesep + fn
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

    # def generate(self, content_type, *args):
    #     requests = {}
    #     for directory in args:
    #         # check for existence of directory
    #         if not os.path.isdir(directory):
    #             msg = "No directory '{}' was found. Could not load content from {}."
    #             print(msg.format(directory, directory))
    #             continue
    #
    #         # get names of all python files in dir
    #         python_files = glob.glob(directory + "/*.py")
    #         module_names = [
    #             os.path.basename(f)[:-3]
    #             for f in python_files
    #             if not f.endswith('__init__.py')
    #         ]
    #
    #         for module_name in module_names:
    #             requests[module_name] = ContentRequest(content_type, directory, module_name)
    #
    #     return [requests[r] for r in requests.keys()]
