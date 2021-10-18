from dragonfly import ActionBase
from castervoice.lib.ctrl.mgr.validation.combo.base_combo_validator import BaseComboValidator
from castervoice.lib.merge.selfmod.tree_rule.tree_node import TreeNode
from castervoice.lib.merge.selfmod.tree_rule.tree_rule import TreeRule


class TreeRuleValidator(BaseComboValidator):

    def validate(self, rule, details):
        if not isinstance(rule, TreeRule):
            return None

        return TreeRuleValidator._validate_node(rule._root_node)

    @staticmethod
    def _validate_node(node):
        spec = node.get_spec()
        action = node.get_action()
        children = node.get_children()
        err = str(spec) + ", " + str(action) + ", " + str(children)

        invalidations = []
        if not isinstance(spec, str):
            invalidations.append("node spec must be string ({})".format(err))
        if not isinstance(action, ActionBase):
            invalidations.append("node base must be ActionBase ({})".format(err))
        for ck in children.keys():
            if not isinstance(children[ck], TreeNode):
                invalidations.append("children must be nodes ({})".format(err))
        return None if len(invalidations) == 0 else ", ".join(invalidations)
