class BiDiGraph(object):
    def __init__(self):
        self._nodes = {}

    def add(self, *nodes):
        """
        Adds nodes to the graph. All nodes in the added group are
        assumed to be connected to each other.

        This structure is not thread safe and provides mutable access
        to its substructures.

        :param nodes: a group of objects which are all hashable
        """
        node_range = range(0, len(nodes))
        for i in node_range:
            node = nodes[i]
            if node not in self._nodes.keys():
                self._nodes[node] = set()
            for k in node_range:
                if i != k:
                    self._nodes[node].add(nodes[k])

    def get_node(self, node):
        return frozenset() if node not in self._nodes else self._nodes[node]

    def get_all_nodes(self):
        return [(node, self._nodes[node]) for node in self._nodes]
