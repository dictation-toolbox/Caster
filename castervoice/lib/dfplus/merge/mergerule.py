'''
Created on Sep 1, 2015

@author: synkarius
'''
from dragonfly import MappingRule, Pause, Function
# from castervoice.lib.dfplus.state.short import R
import re

class MergeRule(MappingRule):
    @staticmethod
    def _get_next_id():
        if not hasattr(MergeRule._get_next_id, "id"):
            MergeRule._get_next_id.id = 0
        MergeRule._get_next_id.id += 1
        return MergeRule._get_next_id.id

    @staticmethod
    def get_merge_name():  # returns unique str(int) for procedural rule names
        return str(MergeRule._get_next_id())

    mapping = {"hello world default macro": Pause("10")}
    '''MergeRules which define `pronunciation` will use
    the pronunciation string rather than their class name
    for their respective enable/disable commands'''
    pronunciation = None
    '''MergeRules which define `non` will instantiate
    their paired non-CCR MergeRule and activate it
    alongside themselves'''
    non = None
    '''MergeRules which define `mcontext` with a
    Dragonfly AppContext become non-global; this
    is the same as adding a context to a Grammar'''
    mcontext = None
    '''app MergeRules MUST define `mwith` in order to
    define what else they can merge with -- this is an
    optimization to prevent pointlessly large global
    CCR copies; mwith is a list of get_pronunciation()s.
    If a rule is added with no mwith, mwith will be set
    to CCRMerger.CORE
    '''
    mwith = None

    def __init__(self,
                 name=None,
                 mapping=None,
                 extras=None,
                 defaults=None,
                 exported=None,
                 ID=None,
                 composite=None,
                 compatible=None,
                 mcontext=None,
                 mwith=None):

        self.ID = ID if ID is not None else MergeRule._get_next_id()
        self.compatible = {} if compatible is None else compatible
        '''composite is the IDs of the rules which this MergeRule is composed of: '''
        self.composite = composite if composite is not None else set([self.ID])
        self._mcontext = self.__class__.mcontext
        if self._mcontext is None: self._mcontext = mcontext
        self._mwith = self.__class__.mwith
        if self._mwith is None: self._mwith = mwith

        if mapping is not None:
            mapping["display available commands"] = Function(
                lambda: self._display_available_commands())

        MappingRule.__init__(self, name, mapping, extras, defaults, exported)
        self.format_actions()


    def __eq__(self, other):
        if not isinstance(other, MergeRule):
            return False
        return self.ID == other.ID

    def create_rdescript(self, command, raction):
            rule_name = self.name
            for unnecessary in ["Non", "Rule", "Ccr", "CCR"]:
                rule_name = rule_name.replace(unnecessary, "")
            extras = ""
            named_extras = re.findall(r"<(.*?)>", command)
            if named_extras:
                extras = ", %(" + ")s, %(".join(named_extras) + ")s"
            return "%s: %s%s" % (rule_name, command, extras)

    def format_actions(self):
        for command, action in self.mapping.items():
            #pylint: disable=no-member
            if hasattr(action, "rdescript") and action.rdescript is None:
                self.mapping[command].rdescript = self.create_rdescript(command, action)


    ''' "copy" getters used for safe merging;
    "actual" versions used for filter functions'''

    def mapping_copy(self):
        return self._mapping.copy()

    def mapping_actual(self):
        return self._mapping

    def extras_copy(self):
        return self._extras.copy()

    def extras_actual(self):
        return self._extras

    def defaults_copy(self):
        return self._defaults.copy()

    def defaults_actual(self):
        return self._defaults

    def merge(self, other):
        mapping = self.mapping_copy()
        mapping.update(other.mapping_copy())
        extras_dict = self.extras_copy()
        extras_dict.update(
            other.extras_copy())  # not just combining lists avoids duplicates
        extras = extras_dict.values()
        defaults = self.defaults_copy()
        defaults.update(other.defaults_copy())
        context = self._mcontext if self._mcontext is not None else other.get_context(
        )  # one of these should always be None; contexts don't mix here
        return MergeRule(
            "Merged" + MergeRule.get_merge_name() + self.get_pronunciation()[0] +
            other.get_pronunciation()[0],
            mapping,
            extras,
            defaults,
            self._exported and other._exported,  # no ID
            composite=self.composite.union(other.composite),
            mcontext=context)

    def get_pronunciation(self):
        return self.pronunciation if self.pronunciation is not None else self.name

    def copy(self):
        return MergeRule(self.name, self._mapping.copy(), self._extras.values(),
                         self._defaults.copy(), self._exported, self.ID, self.composite,
                         self.compatible, self._mcontext, self._mwith)

    def compatibility_check(self, other):
        if other.ID in self.compatible:
            return self.compatible[other.ID]  # lazily
        compatible = True
        for key in self._mapping.keys():
            if key in other.mapping_actual().keys():
                compatible = False
                break
        self.compatible[other.ID] = compatible
        other.compatible[self.ID] = compatible
        return compatible

    def incompatible_IDs(self):
        return [ID for ID in self.compatible if not self.compatible[ID]]

    def get_context(self):
        return self._mcontext

    def set_context(self, context):
        self._mcontext = context

    def get_merge_with(self):
        return self._mwith

    def set_merge_with(self, mwith):
        self._mwith = mwith

    def _display_available_commands(self):
        for spec in self.mapping_actual().keys():
            print(spec)  # do something fancier when the ui is better
