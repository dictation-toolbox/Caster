import unittest

from dragonfly.actions.action_base import ActionBase

from castervoice.lib.dfplus.hint.hintnode import HintNode, NodeRule
from castervoice.lib.dfplus.state.actions2 import NullAction
from castervoice.lib.tests.unit.nexus import TestNexus


class FText(ActionBase):
    ''' just a do-nothing class '''

    def __init__(self, _):
        ActionBase.__init__(self)


def get_test_node():
    H = HintNode
    _align = [
        H("start", FText("start")),
        H("end", FText("end")),
        H("left", FText("left")),
        H("right", FText("right")),
        H("center", FText("center")),
        H("justify", FText("justify"))
    ]
    n = H("FText", FText("FText"), [
        H("align", FText("-align: "), _align),
        H("align last", FText("-align-last: "), _align),
        H("decoration", FText("-decoration: "), [
            H("none", FText("none")),
            H("underline", FText("underline")),
            H("overline", FText("overline")),
            H("line through", FText("line-through")),
            H("blink", FText("blink"))
        ]),
        H("emphasis", FText("-emphasis: "), [
            H("none", FText("none")),
            H("accent", FText("accent")),
            H("dot", FText("dot")),
            H("circle", FText("circle")),
            H("disc", FText("disc")),
            H("before", FText("before")),
            H("after", FText("after"))
        ]),
        H("indent", FText("-indent: "))
    ])
    return n


class TestNode(TestNexus):

    def setUp(self):
        TestNexus.setUp(self)
        self.node = get_test_node()

    def test_node_length(self):
        self.assertEqual(len(self.node), 29)

    def test_node_fillout(self):
        nr = NodeRule(self.node, self.nexus)

        mapping = {}
        self.node.fill_out_rule(mapping, [], {}, nr)
        self.assertEqual(len(mapping), 6)

        self.node.explode_depth = 0
        mapping = {}
        self.node.fill_out_rule(mapping, [], {}, nr)
        self.assertEqual(len(mapping), 1)


class TestNodeRule(TestNode):
    def setUp(self):
        TestNode.setUp(self)
        self.noderule = NodeRule(self.node, self.nexus)

    def test_change_node(self):
        self.assertIs(self.noderule.node, self.noderule.master_node)
        ''' "align" should be in the mapping before, but not after'''
        self.assertIn("align", self.noderule.mapping_actual())
        self.noderule.mapping_actual()["align"].execute()
        self.assertNotIn("align", self.noderule.mapping_actual())
        ''' "center" should be in the mapping before, but not after'''
        self.assertIn("center", self.noderule.mapping_actual())
        self.noderule.mapping_actual()["center"].execute()
        self.assertNotIn("center", self.noderule.mapping_actual())
        ''' node should have reset at this point '''
        self.assertIs(self.noderule.node, self.noderule.master_node)

    def test_defaulting(self):
        self.assertIn("align", self.noderule.mapping_actual())
        self.noderule.mapping_actual()["align"].execute()
        defaulter = NullAction()
        defaulter.set_nexus(self.nexus)
        ''' the noderule should default here and reset '''
        defaulter.execute()
        self.assertIn("align", self.noderule.mapping_actual())

if __name__ == '__main__':
    unittest.main()
