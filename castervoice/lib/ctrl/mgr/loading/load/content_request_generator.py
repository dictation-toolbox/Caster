import re
import os
import six
if six.PY2:
    from io import open

from castervoice.lib.ctrl.mgr.loading.load.content_request import ContentRequest
from castervoice.lib.ctrl.mgr.loading.load.content_type import ContentType


class ContentRequestGenerator(object):
    """
    Generates a set of requests from a path.
    """

    def get_all_content_modules(self, directory):
        relevant_modules = []
        for dirpath, dirnames, filenames in self._walk(directory):
            for filename in filenames:
                file_path = dirpath + os.sep + filename
                content_type, content_class_name = self._scan_file(file_path)
                if content_type is not None:
                    module_name = filename[:-3]
                    request = ContentRequest(content_type,
                                             dirpath,
                                             module_name,
                                             content_class_name)
                    relevant_modules.append(request)
        return relevant_modules

    def _walk(self, directory):
        """File i/o broken out for testability"""
        return os.walk(directory)

    def _get_file_lines(self, file_path):
        """File i/o broken out for testability"""
        content = None
        with open(file_path, encoding="utf8") as f:
            content = f.readlines()
        return content

    def _scan_file(self, file_path):
        """
        Reads the whole file, classifies it as rule, transformer, hook, or none.
        Also finds a list of potential names for the loadable content class.
        :param file_path: str
        :return: str
        """
        if not file_path.endswith(".py"):
            return None, None
        if file_path.endswith("__init__.py"):
            return None, None

        content = self._get_file_lines(file_path)

        rule_func = "def {}():".format(ContentType.GET_RULE)
        transformer_func = "def {}():".format(ContentType.GET_TRANSFORMER)
        hook_func = "def {}():".format(ContentType.GET_HOOK)

        content_type = None
        content_class_name = None
        for line in content:
            if line.strip().startswith("#") or line.isspace():
                continue
            # should only be ONE 'get_<thing>' function
            if content_type is None:
                if rule_func in line:
                    content_type = ContentType.GET_RULE
                    # if it's a rule, keep looking for the class name
                    continue
                elif transformer_func in line:
                    content_type = ContentType.GET_TRANSFORMER
                    break
                elif hook_func in line:
                    content_type = ContentType.GET_HOOK
                    break
            else:
                ccn = ContentRequestGenerator._extract_class_name(line)
                if ccn is not None:
                    content_class_name = ccn
        return content_type, content_class_name

    @staticmethod
    def _extract_class_name(line):
        class_name_match = re.search("return (.+?),", line)
        if class_name_match is not None and len(class_name_match.groups()) == 1:
            result = class_name_match.group(1)
            result = result.replace("[", "").replace("(", "")
            return result
        return None

