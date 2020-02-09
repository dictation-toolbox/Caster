from unittest import TestCase

from castervoice.lib.util.bidi_graph import BiDiGraph


class TestBiDiGraph(TestCase):
    def test_get_node_1(self):
        """
        Tests that each node added is connected to the other
        nodes added with it.
        """
        graph = BiDiGraph()
        graph.add("a", "b")
        self.assertItemsEqual(["b"], graph.get_node("a"))
        self.assertItemsEqual(["a"], graph.get_node("b"))

    def test_get_node_2(self):
        """
        Tests that each node added is connected to the other
        nodes added with it, but not nodes added separately.
        """
        graph = BiDiGraph()
        graph.add("a", "b")
        graph.add("a", "c")
        graph.add("a", "d")
        self.assertItemsEqual(["b", "c", "d"], graph.get_node("a"))
        self.assertItemsEqual(["a"], graph.get_node("b"))
        self.assertItemsEqual(["a"], graph.get_node("c"))
        self.assertItemsEqual(["a"], graph.get_node("d"))

    def test_get_all_nodes(self):
        """
        Tests the content of get_all_nodes.
        """
        graph = BiDiGraph()
        graph.add("a", "b", "c")
        keys = []
        values = []
        for n in graph.get_all_nodes():
            keys.append(n[0])
            values.extend(n[1])
        self.assertItemsEqual(["a", "b", "c"], keys)
        self.assertItemsEqual(["a", "a", "b", "b", "c", "c"], values)
