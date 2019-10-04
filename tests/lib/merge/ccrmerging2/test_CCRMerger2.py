from unittest import TestCase

from mock import Mock

from castervoice.lib.ctrl.nexus import Nexus
from castervoice.lib.merge.ccrmerging2.transformers.transformers_runner import TransformersRunner


class TestCCRMerger2(TestCase):

    def setUp(self):
        order_fn = lambda: ["Alphabet", "Numbers"]
        selfmodrule_configurer = Mock()
        transformers_config = Mock()
        transformers_runner = TransformersRunner(transformers_config)
        self.merger = Nexus._create_merger(order_fn, selfmodrule_configurer, transformers_runner)

    def test_merge_empty(self):
        """
        Merger should run through empty list without errors.
        """
        self.merger.merge([])
