from castervoice.lib.merge.selfmod.selfmodrule import BaseSelfModifyingRule
from castervoice.lib.merge.selfmod.smr_shim import SelfModReloadingShim


class SelfModRuleConfigurer(object):
    """
    Configures a self modifying rule both for
    hot-reset and hook events execution.
    """

    def __init__(self):
        self._smr_shim = None
        self._hooks_runner = None

    def set_reload_fn(self, reload_fn):
        self._smr_shim = SelfModReloadingShim(reload_fn)

    def set_hooks_runner(self, hooks_runner):
        self._hooks_runner = hooks_runner

    def configure(self, selfmodrule):
        if isinstance(selfmodrule, BaseSelfModifyingRule):
            selfmodrule.set_reload_shim(self._smr_shim)
            selfmodrule.set_hooks_runner(self._hooks_runner)
