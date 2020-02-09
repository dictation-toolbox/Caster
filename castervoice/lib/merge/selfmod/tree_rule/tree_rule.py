import os

from dragonfly import Function
from castervoice.lib import settings
from castervoice.lib.ctrl.mgr.errors.tree_rule_config_error import TreeRuleConfigurationError
from castervoice.lib.ctrl.mgr.rule_formatter import _set_the_rdescript 
from castervoice.lib.merge.ccrmerging2.hooks.events.node_change_event import NodeChangeEvent
from castervoice.lib.merge.selfmod.selfmodrule import BaseSelfModifyingRule
from castervoice.lib.merge.selfmod.tree_rule.tree_node import TreeNode


class TreeRule(BaseSelfModifyingRule):

    _PATH = "path"

    def __init__(self, tree_name, tree_root):
        self._root_node = tree_root
        self._tree_name = tree_name
        super(TreeRule, self).__init__(TreeRule._get_tree_rule_config_path(tree_name))

    @staticmethod
    def _get_tree_rule_config_path(tree_name):
        formatted_path_name = "SM_{}_TREE_PATH".format(tree_name.upper().replace(" ", "_"))
        if formatted_path_name not in settings.SETTINGS["Tree_Node_Path"]:
            msg = "Path '{}' was not found in the 'Tree_Node_Path' section of settings.toml. Did you add it?"
            raise TreeRuleConfigurationError(msg.format(formatted_path_name))
        config_path = settings.settings(["Tree_Node_Path", formatted_path_name])
        return config_path

    def _deserialize(self):
        # get active path from config
        config_copy = self._config.get_copy()
        active_path = []
        if TreeRule._PATH in config_copy:
            active_path = list(config_copy[TreeRule._PATH])

        # get speakable nodes along path of tree's branches
        active_nodes = TreeNode.get_nodes_along_path([self._root_node], active_path)

        # create mapping/etc. from active nodes
        self._smr_mapping = {}
        self._smr_extras = []
        self._smr_defaults = {}

        for tree_node in active_nodes:
            spec = tree_node.get_spec()
            action = tree_node.get_action()
            _set_the_rdescript(action, spec, self.__class__.__name__)
            action_and_node_change = action + Function(TreeRule._create_spec_fn(self._refresh, spec))
            self._smr_mapping[spec] = action_and_node_change
            self._smr_extras.extend(tree_node.get_extras())
            self._smr_defaults.update(tree_node.get_defaults())
        # cancel by TreeRule name: resets tree to root node
        self._smr_mapping["cancel {}".format(self._tree_name)] = Function(lambda: self._refresh())

        # run node change hooks, if configured
        if self._hooks_runner is not None:
            event = NodeChangeEvent(self._tree_name, active_path, [n.get_spec() for n in active_nodes])
            self._hooks_runner.execute(event)

    @staticmethod
    def _create_spec_fn(fn, spec):
        return lambda: fn(spec)

    def _refresh(self, *args):
        config_copy = self._config.get_copy()
        active_path = []
        if TreeRule._PATH in config_copy:
            active_path = list(config_copy[TreeRule._PATH])

        if len(args) > 0:
            active_path.append(args[0])
        else:
            active_path = []

        self._detect_leaf_node_reached(active_path)
        self._config.replace({TreeRule._PATH: active_path})
        self.reset()

    def _detect_leaf_node_reached(self, active_path):
        """
        Detects if a leaf node's spec has been spoken.
        If it has, resets the tree back to the root node.
        """
        current_node = self._root_node
        for node_spec in active_path:
            children = current_node.get_children()
            if node_spec in children:
                current_node = children[node_spec]

        if len(current_node.get_children()) == 0:
            del active_path[:]
