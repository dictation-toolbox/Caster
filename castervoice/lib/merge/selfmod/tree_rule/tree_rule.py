from dragonfly import Function
from castervoice.lib import settings
from castervoice.lib.merge.ccrmerging2.hooks.events.node_change_event import NodeChangeEvent
from castervoice.lib.merge.selfmod.selfmodrule import BaseSelfModifyingRule


class TreeRule(BaseSelfModifyingRule):

    _PATH = "path"

    def __init__(self, tree_name, tree_root):
        self._root_node = tree_root
        self._tree_name = tree_name
        super(settings.SETTINGS["paths"]["SM_{}_TREE_PATH_".format(tree_name.upper())])

    def _deserialize(self):
        # get active path from config
        config_copy = self._config.get_copy()
        active_path = []
        if TreeRule._PATH in config_copy:
            active_path = list(config_copy[TreeRule._PATH])

        # if no navigation, use root node, otherwise navigate the tree
        active_nodes = [self._root_node]
        if len(active_path) > 0:
            children = self._root_node.navigate_to_active_children(self._active_path)
            # if navigated out to the leaves, use root node
            if len(children) > 0:
                active_nodes = children

        # create mapping/etc. from active nodes
        self._smr_mapping = {}
        self._smr_extras = []
        self._smr_defaults = {}
        for tree_node in active_nodes:
            spec = tree_node.get_spec()
            action = tree_node.get_action()
            action_and_node_change = action + Function(lambda: self._refresh(spec))
            self._smr_mapping[spec] = action_and_node_change
            self._smr_extras.extend(tree_node.get_extras())
            self._smr_defaults.update(tree_node.get_defaults())
        # cancel by TreeRule name: resets tree to root node
        self._smr_mapping["cancel {}".format(self._tree_name)] = Function(lambda: self._refresh())

        # run node change hooks, if configured
        if self._hooks_runner is not None:
            event = NodeChangeEvent(self._tree_name, active_path, [n.get_spec() for n in active_nodes])
            self._hooks_runner.execute(event)

    def _refresh(self, *args):
        config_copy = self._config.get_copy()
        active_path = []
        if TreeRule._PATH in config_copy:
            active_path = list(config_copy[TreeRule._PATH])

        if len(args) > 0:
            active_path.append(args[0])
        else:
            active_path = []

        config_copy[TreeRule._PATH] = active_path
        self._config.replace(config_copy)
        self.reset()

    def get_pronunciation(self):
        return self._root_node.get_spec()
