import collections

from dragonfly import MappingRule, Pause, Function
import re
from castervoice.lib import printer, available_commands_tracker
from castervoice.lib.merge.ccrmerging2.pronounceable import Pronounceable


class MergeRule(MappingRule, Pronounceable):
    @staticmethod
    def _get_next_id():
        if not hasattr(MergeRule._get_next_id, "id"):
            MergeRule._get_next_id.id = 0
        MergeRule._get_next_id.id += 1
        return MergeRule._get_next_id.id

    mapping = {"hello world default macro": Pause("10")}
    '''MergeRules which define `pronunciation` will use
    the pronunciation string rather than their class name
    for their respective enable/disable commands'''
    pronunciation = None

    def __init__(self,
                 name=None,
                 mapping=None,
                 extras=None,
                 defaults=None,
                 exported=None):

        MappingRule.__init__(self, name, mapping, extras, defaults, exported)

        self._format_actions()

    def _create_rdescript(self, spec):
        rule_name = self.name
        for unnecessary in ["Non", "Rule", "Ccr", "CCR"]:
            rule_name = rule_name.replace(unnecessary, "")
        extras = ""
        named_extras = re.findall(r"<(.*?)>", spec)
        if named_extras:
            extras = ", %(" + ")s, %(".join(named_extras) + ")s"
        return "%s: %s%s" % (rule_name, spec, extras)

    '''Generates an "rdescript" for actions in this rule which don't have them.'''
    def _format_actions(self):
        for spec, action in self.mapping.items():
            #pylint: disable=no-member
            if hasattr(action, "rdescript") and action.rdescript is None:
                self.mapping[spec].rdescript = self._create_rdescript(spec)


    ''' "copy" getters used for safe merging;
    "actual" versions used for transformers'''

    def mapping_copy(self):
        return self._mapping.copy()
     
    def mapping_actual(self):
        """
        This should be done away with.
        :return:
        """
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
        return MergeRule(
            "Merged" + str(MergeRule._get_next_id()),
            mapping,
            extras,
            defaults,
            self._exported and other._exported)

    def get_pronunciation(self):
        return self.pronunciation if self.pronunciation is not None else self.name

    def copy(self):
        return MergeRule(self.name, self._mapping.copy(), self._extras.values(),
                         self._defaults.copy(), self._exported)

    def prepare_for_merger(self):
        """
        The OrderedDict is an optimization for Kaldi engine,
        won't make a difference to other engines.

        This is also the appropriate place to add the "list available commands"
        command, since this happens post-merge.

        :return: MergeRule
        """

        unordered_specs = set(self._mapping.keys())
        ordered_specs = sorted(unordered_specs)

        ordered_dict = collections.OrderedDict()
        for spec in ordered_specs:
            ordered_dict[spec] = self._mapping[spec]

        act = available_commands_tracker.get_instance()
        act.set_available_commands("\n".join(ordered_specs))
        ordered_dict["list available commands"] = Function(lambda: printer.out(act.get_available_commands()))

        return MergeRule(self.name, ordered_dict, self._extras.values(),
                         self._defaults.copy(), self._exported)

    def get_rule_class_name(self):
        return self.__class__.__name__
