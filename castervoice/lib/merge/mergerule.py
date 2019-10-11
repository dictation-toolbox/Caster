import collections

from dragonfly import MappingRule, Function
import re
from castervoice.lib import printer, available_commands_tracker
from castervoice.lib.merge.ccrmerging2.pronounceable import Pronounceable


class MergeRule(Pronounceable):

    mapping = {}
    extras = []
    defaults = {}

    '''MergeRules which define `pronunciation` will use
    the pronunciation string rather than their class name
    for their respective enable/disable commands'''
    pronunciation = None

    def __init__(self, name=None, mapping=None, extras=None, defaults=None):
        self.name = name or self.get_rule_class_name()
        self._mapping = mapping or self.mapping.copy()
        extras_list = extras or self.extras
        self._extras = dict([(element.name, MergeRule._copy_extra(element))
                            for element in extras_list])
        self._defaults = defaults or self.defaults.copy()
        #
        self._format_actions()

    def merge(self, other):
        new_mapping = self.get_mapping()
        new_mapping.update(other.get_mapping())

        new_extras = self.get_extras()
        new_extras.extend(other.get_extras())

        new_defaults = self.get_defaults()
        new_defaults.update(other.get_defaults())

        return MergeRule(mapping=new_mapping,
                         extras=new_extras,
                         defaults=new_defaults)

    def to_mapping_rule(self):
        return MappingRule(mapping=self.get_mapping(),
                           extras=self.get_extras(),
                           defaults=self.get_defaults())

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
        for spec, action in self._mapping.items():
            # pylint: disable=no-member
            if hasattr(action, "rdescript") and action.rdescript is None:
                self._mapping[spec].rdescript = self._create_rdescript(spec)

    def get_mapping(self):
        return self._mapping.copy()

    def get_extras(self):
        return self._extras.values()

    def get_defaults(self):
        return self._defaults.copy()

    def get_pronunciation(self):
        return self.pronunciation if self.pronunciation is not None else self.name

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
        # TODO: bring back metarule
        ordered_dict["list available commands"] = Function(lambda: printer.out(act.get_available_commands()))

        extras_copy = self.get_extras()
        defaults_copy = self.get_defaults()

        class PreparedRule(MappingRule):
            mapping = ordered_dict
            extras = extras_copy
            defaults = defaults_copy

        return PreparedRule()

    def get_rule_class_name(self):
        return self.__class__.__name__

    @staticmethod
    def _get_next_id():
        if not hasattr(MergeRule._get_next_id, "id"):
            MergeRule._get_next_id.id = 0
        MergeRule._get_next_id.id += 1
        return MergeRule._get_next_id.id

    @staticmethod
    def _copy_extra(extra):
        return extra  # TODO
