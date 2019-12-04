from castervoice.lib.ctrl.mgr.errors.base_class_error import DontUseBaseClassError


class BaseGrammarContainer(object):

    def set_non_ccr(self, rcn, grammar):
        raise DontUseBaseClassError(self)

    def set_ccr(self, ccr_grammars):
        raise DontUseBaseClassError(self)

    def wipe_ccr(self):
        raise DontUseBaseClassError(self)
