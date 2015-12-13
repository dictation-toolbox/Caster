import unittest

from dragonfly.actions.action_text import Text

from caster.lib.dfplus.hint.hintnode import HintNode, NodeRule
from caster.lib.tests.unit.nexus import TestNexus


def get_test_node():
    H = HintNode
    _align = [H("start", Text("start")), H("end", Text("end")), H("left", Text("left")),
              H("right", Text("right")), H("center", Text("center")), H("justify", Text("justify"))]
    n = H("text", Text("text"), [
                       H("align", Text("-align: "), _align),
                       H("align last", Text("-align-last: "), _align),
                       H("decoration", Text("-decoration: "), [
                                           H("none", Text("none")),
                                           H("underline", Text("underline")),
                                           H("overline", Text("overline")),
                                           H("line through", Text("line-through")),
                                           H("blink", Text("blink"))
                                           ]),
                      H("emphasis", Text("-emphasis: "), [
                                        H("none", Text("none")),
                                        H("accent", Text("accent")),
                                        H("dot", Text("dot")),
                                        H("circle", Text("circle")),
                                        H("disc", Text("disc")),
                                        H("before", Text("before")),
                                        H("after", Text("after"))
                                        ]),
                      H("indent", Text("-indent: "))])
    return n

class TestNode(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.node = get_test_node()
    
    def test_node_length(self):
        self.assertEqual(len(self.node), 29)
        
    def test_node_fillout(self):
        nr = NodeRule(self.node)
        
        mapping={}
        self.node.fill_out_rule(mapping, [], {}, nr)
        self.assertEqual(len(mapping), 6)
        
        self.node.explode_depth = 0
        mapping={}
        self.node.fill_out_rule(mapping, [], {}, nr)
        self.assertEqual(len(mapping), 1)


class TestNodeRule(TestNexus, TestNode):
    
    def setUp(self):
        TestNode.setUp(self)
        TestNexus.setUp(self)
        self.noderule = NodeRule(self.node)
#         self.nexus.merger.
     
    def test_change_node(self):
        "text_action is a Text + NodeChange + ContextSeeker"
        text_action = self.noderule.mapping_actual()["text"]
        
        ''''''
                                
