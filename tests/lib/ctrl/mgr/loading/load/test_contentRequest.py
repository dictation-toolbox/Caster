from unittest import TestCase

from castervoice.lib.ctrl.mgr.loading.load.content_request import ContentRequest
from castervoice.lib.ctrl.mgr.loading.load.content_type import ContentType


class TestContentRequest(TestCase):

    def test_module_package_resolution(self):
        """
        ContentRequest resolves module/package name conflicts:
        if the module name and the package name are the same,
        the package name's specificity is increased.
        """
        cr = ContentRequest(ContentType.GET_RULE, "asdf/same_name", "same_name", "SameNameRule")
        self.assertTrue(cr.module_name == "same_name.same_name")