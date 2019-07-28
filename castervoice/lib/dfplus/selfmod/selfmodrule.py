from dragonfly.grammar.elements import Dictation

from castervoice.lib import printer
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.selfmod.sm_config import SelfModStateSavingConfig
from castervoice.lib.dfplus.state.actions2 import NullAction


class BaseSelfModifyingRule(MergeRule):

    def __init__(self, config_path, name=None):
        """
        SelfModifyingRule is a kind of rule which gets its command set changed
        on-the-fly based on some kind of user interaction. Child classes
        must implement their own version of the _refresh and
        _deserialize methods.

        :param name: str
        """
        self._smr_mapping = {"spec which gets replaced": NullAction()}
        # extras and defaults may not get replaced:
        self._smr_extras = [IntegerRefST("n", 1, 50), Dictation("s")]
        self._smr_defaults = {"n": 1, "s": ""}

        self._config = SelfModStateSavingConfig(config_path)
        self._config.load()
        self._deserialize()

        MergeRule.__init__(self, name, self._smr_mapping, self._smr_extras, self._smr_defaults)

        self._reload_shim = None
        self._hooks_runner = None

    def set_reload_shim(self, reload_shim):
        """
        The reload shim has the ability to tell the GrammarManager
        (or other manager class) to attempt to discard the current
        in-memory instance of the selfmod rule and attempt to reload
        from disk.

        :param reload_shim: SelfModReloadingShim
        """
        self._reload_shim = reload_shim

    def set_hooks_runner(self, hooks_runner):
        """
        The hooks runner can run selfmod reset-time hooks if this is set.

        :param hooks_runner: HooksRunner
        """
        self._hooks_runner = hooks_runner

    def reset(self):
        class_name = self.__class__.__name__
        if self._reload_shim is None:
            printer.out("Reload shim is not set for {}. Rule cannot hot-reset, will only reset with engine.".format(
                class_name))
            return
        self._reload_shim.signal_reload(class_name)

    def _deserialize(self):
        """
        This should ONLY be called by the constructor, nowhere else.

        Deserialize ALL state loaded from self._config into self._smr_mapping,
        self._smr_extras, and self._smr_defaults.

        Child classes should implement this.
        """
        # TODO: throw error if this base method is called
        pass

    def _refresh(self, *args):
        """
        Modifies state in some way, then calls self.reset().

        Child classes should implement this.

        :param args: any
        :return:
        """
        # TODO: throw error if this base method is called
        pass
