from dragonfly import ActionBase

from castervoice.lib.merge.selfmod.tree_rule.invalid_tree_node_path_error import InvalidTreeNodePathError


class TreeNode(object):
    def __init__(self, spec, action, extras=[], defaults={}, children=[]):
        """
        An action with child actions. These child actions can form a tree
        structure with this node and their child nodes.

        :param spec: (str) the spec for this node
        :param action: (ActionBase) the action for this node
        :param extras: extras for this node's action
        :param defaults: defaults for this node's action
        :param children: (list) child nodes of this node
        """
        err = str(spec) + ", " + str(action) + ", " + str(children)
        assert isinstance(spec, basestring), "Node spec must be string: " + err
        assert isinstance(action, ActionBase), "Node base must be ActionBase: " + err
        assert len(children) == 0 or isinstance(children[0], TreeNode), "Children must be nodes: " + err

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

    def navigate_to_active_children(self, active_path):
        """
        Follows the active path through the tree, returns the children
        of the last-activated node.

        :param active_path: (array of strings) the path to the active node
        :return: (array of FlattenedTreeNode)
        """

        if len(active_path) == 0:
            raise InvalidTreeNodePathError("EMPTY PATH")

        if len(active_path) == 1:
            if active_path[0] == self._spec:
                return self._children.values()
            else:
                raise InvalidTreeNodePathError(active_path)

        if active_path[0] in self._children:
            child_node = self._children[active_path[0]]
            active_path = list(active_path)
            active_path.pop(0)
            return child_node.navigate_to_active_children(active_path)
        else:
            raise InvalidTreeNodePathError(active_path)
