from dragonfly.grammar.elements import Dictation

from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge.mergepair import MergeInf
from castervoice.lib.dfplus.merge.mergerule import MergeRule
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

    def __init__(self, name=None, refresh=True):
        """
        SelfModifyingRule is a kind of rule which gets its command set changed
        on-the-fly based on some kind of user interaction. Child classes
        must implement their own version of the `refresh` method.

        :param name:
        :param refresh:
        """
        MergeRule.__init__(self, name)
        if refresh:
            self._refresh()

    def _refresh(self, *args):
        """
        Does stuff to get mapping, then calls self.reset(), passing in new mapping.
        Child classes should implement this.

        :param args: any
        :return:
        """
        self.reset({"default record rule spec": NullAction()})

    def reset(self, mapping):

        """
        options
            1) create a new type based off of the mapping -- won't hold state
            2)

        PROBLEM: GrammarManager instantiates classes itself when they're registered,
            but doing that, there's no way to hold state
            - can you put the state on the new class?

        Force all "selfmod" rules to write their state to disk?
            - yes, this is the solution

        So... each SelfModRule will have the shim, which can signal its class name for a reload, even
        though no changes may have actually occurred to the file.
        Reloading the class will force it to read its state from disk again.
        This will be the equivalent of mutating itself.

        1. Find a place for this new state in the .caster dir
            a. add and setting
            b. auto-make the dir with the other auto-made dirs
        2.

        """

        extras = self.extras if self.extras else [IntegerRefST("n", 1, 50), Dictation("s")]
        defaults = self.defaults if self.defaults else { "n": 1, "s": "" }




