from castervoice.lib.merge.selfmod.tree_rule.invalid_tree_node_path_error import InvalidTreeNodePathError


class TreeNode(object):
    def __init__(self, spec, action, children=[], extras=[], defaults={}):
        """
        An action with child actions. These child actions can form a tree
        structure with this node and their child nodes.

        :param spec: (str) the spec for this node
        :param action: (ActionBase) the action for this node
        :param extras: extras for this node's action
        :param defaults: defaults for this node's action
        :param children: (list) child nodes of this node
        """
        self._spec = spec
        self._action = action
        self._extras = extras
        self._defaults = defaults
        self._children = {}
        for child in children:
            self._children[child.get_spec()] = child

    def get_spec(self):
        return self._spec

    def get_action(self):
        return self._action

    def get_extras(self):
        return list(self._extras)

    def get_defaults(self):
        return self._defaults.copy()

    def get_children(self):
        return self._children.copy()

    @staticmethod
    def get_nodes_along_path(nodes, active_path):

        if len(active_path) == 0:
            return nodes

        active_path = list(active_path)
        selecting_spec = active_path.pop(0)
        for node in nodes:
            if selecting_spec == node.get_spec():
                return TreeNode.get_nodes_along_path(node.get_children().values(), active_path)
        raise InvalidTreeNodePathError(active_path + [selecting_spec])
