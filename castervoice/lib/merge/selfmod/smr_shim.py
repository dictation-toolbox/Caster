from castervoice.lib import printer
from castervoice.lib.merge.selfmod.tree_rule.invalid_tree_node_path_error import InvalidTreeNodePathError


class SelfModReloadingShim(object):
    """
    SelfModReloadingShim adds a safety net around reloading selfmodrules
    from disk, as well as limiting access to the nexus / gm functionality.
    """

    def __init__(self, reload_fn):
        self._reload_fn = reload_fn

    def signal_reload(self, rule_class_name):
        printer.out("Reloading {}...".format(rule_class_name))
        try:
            self._reload_fn(rule_class_name)
        except InvalidTreeNodePathError:
            printer.out("{} reload failed: tree path was invalidated.".format(rule_class_name))
            return
        printer.out("{} reloaded.".format(rule_class_name))
