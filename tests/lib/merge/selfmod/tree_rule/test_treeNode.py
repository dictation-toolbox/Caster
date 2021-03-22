from unittest import TestCase

from castervoice.lib.actions import Text
from castervoice.lib.merge.selfmod.tree_rule.invalid_tree_node_path_error import InvalidTreeNodePathError
from castervoice.lib.merge.selfmod.tree_rule.tree_node import TreeNode

_TN = TreeNode
_TEST_NODES = _TN("zero", Text("L-0"), [
            _TN("one alpha", Text("L-1A"), [
                    _TN("two alpha", Text("L-2A"), [
                            _TN("three alpha", Text("L-3A")),
                            _TN("three bravo", Text("L-3B")),
                            _TN("three charlie", Text("L-3C"))
                        ]),
                    _TN("two bravo", Text("L-2B"))
                ]),
            _TN("one bravo", Text("L-1B")),
            _TN("one charlie", Text("L-1C"))
    ])


class TestTreeNode(TestCase):

    def test_get_nodes_along_path_success_depth_0(self):
        nodes = TreeNode.get_nodes_along_path([_TEST_NODES], [])

        self.assertEqual(1, len(nodes))
        self.assertSetEqual(set(["zero"]),
                            set([tn.get_spec() for tn in nodes]))

    def test_get_nodes_along_path_success_depth_1(self):
        nodes = TreeNode.get_nodes_along_path([_TEST_NODES], ["zero"])

        self.assertEqual(3, len(nodes))
        self.assertSetEqual(set(["one alpha", "one bravo", "one charlie"]),
                            set([tn.get_spec() for tn in nodes]))

    def test_get_nodes_along_path_success_depth_2(self):
        nodes = TreeNode.get_nodes_along_path([_TEST_NODES], ["zero", "one alpha"])

        self.assertEqual(2, len(nodes))
        self.assertSetEqual(set(["two alpha", "two bravo"]),
                            set([tn.get_spec() for tn in nodes]))

    def test_get_nodes_along_path_success_depth_3(self):
        nodes = TreeNode.get_nodes_along_path([_TEST_NODES], ["zero", "one alpha", "two alpha"])

        self.assertEqual(3, len(nodes))
        self.assertSetEqual(set(["three alpha", "three bravo", "three charlie"]),
                            set([tn.get_spec() for tn in nodes]))

    def test_get_nodes_along_path_success_depth_4(self):
        nodes = TreeNode.get_nodes_along_path([_TEST_NODES], ["zero", "one alpha", "two alpha", "three alpha"])

        self.assertEqual(0, len(nodes))
        self.assertSetEqual(frozenset(),
                            set([tn.get_spec() for tn in nodes]))

    def test_get_nodes_along_path_error(self):
        with self.assertRaises(InvalidTreeNodePathError) as context:
            TreeNode.get_nodes_along_path([_TEST_NODES], ["zero", "one alpha", "two alpha", "three delta"])
        # self.assertTrue("Broken TreeNode path:" in context.exception.message)
        self.assertTrue("Broken TreeNode path:" in str(context.exception))
