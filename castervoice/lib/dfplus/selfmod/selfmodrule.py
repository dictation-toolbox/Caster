from dragonfly.grammar.elements import Dictation

from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge.mergepair import MergeInf
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.selfmod import smr_shim
from castervoice.lib.dfplus.selfmod.sm_config import SelfModStateSavingConfig
from castervoice.lib.dfplus.state.actions2 import NullAction

'''
Rather than being "self modifying", SelfModifyingRule should become
"RuleFactoryRule", have a backing data structure of some sort that gets mutated,
and then be allowed to call "register_rule" on the GM with the new versions of
itself periodically.


- RFR should create MergeRules.
- RFR should be allowed to modify its base mappings, , then use those to generate a new rule,
    new rule always having the same name so GM handles it right.
    
Too much for now, shim it instead.
'''


class BaseSelfModifyingRule(MergeRule):

    def __init__(self, config_path, name=None, refresh=True):
        """
        SelfModifyingRule is a kind of rule which gets its command set changed
        on-the-fly based on some kind of user interaction. Child classes
        must implement their own version of the _refresh, _serialize, and
        _deserialize methods.

        :param name: str
        :param refresh:
        """
        self._smr_mapping = {"spec which gets replaced": NullAction()}
        # extras and defaults may not get replaced:
        self._smr_extras = [IntegerRefST("n", 1, 50), Dictation("s")]
        self._smr_defaults = {"n": 1, "s": ""}

        self._config = SelfModStateSavingConfig(config_path)
        self._config.load()
        self._deserialize()

        MergeRule.__init__(self, name, self._smr_mapping, self._smr_extras, self._smr_defaults)

        if refresh:
            self._refresh()

    def reset(self):
        self._serialize()
        smr_shim.get_instance().signal_reload(self.__class__)

    def _serialize(self):
        """
        This should ONLY be called by the 'reset' method, nowhere else.

        Serialize ALL state, save to self._config.

        Child classes should implement this.
        """
        pass

    def _deserialize(self):
        """
        This should ONLY be called by the constructor, nowhere else.

        Deserialize ALL state loaded from self._config into self._smr_mapping,
        self._smr_extras, and self._smr_defaults.

        Child classes should implement this.
        """
        pass

    def _refresh(self, *args):
        """
        Modifies state in some way, then calls self.reset().

        Child classes should implement this.

        :param args: any
        :return:
        """
        self.reset({"default record rule spec": NullAction()})
