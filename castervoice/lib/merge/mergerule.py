import collections

from dragonfly import Function, MappingRule

from castervoice.lib import available_commands_tracker, printer
from castervoice.lib.ctrl.mgr.rule_formatter import _set_rdescripts
from castervoice.lib.merge.ccrmerging2.pronounceable import Pronounceable


class MergeRule(MappingRule, Pronounceable):

    mapping = {}
    extras = []
    defaults = {}

    '''MergeRules which define `pronunciation` will use
    the pronunciation string rather than their class name
    for their respective enable/disable commands'''
    pronunciation = None

    def __init__(self, name=None, mapping=None, extras=None, defaults=None):
        _name = name or self.get_rule_class_name()
        _mapping = mapping or self.mapping.copy()
        _extras = extras or self.extras[:]
        _defaults = defaults or self.defaults.copy()
        _set_rdescripts(_mapping, _name)
        #
        super(MergeRule, self).__init__(name=_name,
                                        mapping=_mapping,
                                        extras=_extras,
                                        defaults=_defaults)

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

    def get_mapping(self):
        return self._mapping.copy()

    def get_extras(self):
        return list(self._extras.values())

    def get_defaults(self):
        return self._defaults.copy()

    def get_pronunciation(self):
        return self.pronunciation if self.pronunciation is not None else self._name

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
