from dragonfly import MappingRule, Pause, Function
import re, os, sys
from castervoice.lib import printer


class MergeRule(MappingRule):
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
                 exported=None,
                 location=None):

        if mapping is not None:
            mapping["display available commands"] = Function(
                lambda: self._display_available_commands())

        MappingRule.__init__(self, name, mapping, extras, defaults, exported)

        self._format_actions()
        
        if location is None:
            location = self._determine_file_location()
        self.location = location
    
    '''TODO: unit test this
    Should get the location on disk of the child class which calls this method.
    '''
    def _determine_file_location(self):
        filename = sys.modules[self.__module__].__file__
        location = os.path.realpath(filename)
        return location

    def create_rdescript(self, command, raction):
            rule_name = self.name
            for unnecessary in ["Non", "Rule", "Ccr", "CCR"]:
                rule_name = rule_name.replace(unnecessary, "")
            extras = ""
            named_extras = re.findall(r"<(.*?)>", command)
            if named_extras:
                extras = ", %(" + ")s, %(".join(named_extras) + ")s"
            return "%s: %s%s" % (rule_name, command, extras)

    '''Generates an "rdescript" for actions in this rule which don't have them.'''
    def format_actions(self):
        for command, action in self.mapping.items():
            #pylint: disable=no-member
            if hasattr(action, "rdescript") and action.rdescript is None:
                self.mapping[command].rdescript = self.create_rdescript(command, action)


    ''' "copy" getters used for safe merging;
    "actual" versions used for transformers'''

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
            "Merged" + str(MergeRule._get_next_id()),
            mapping,
            extras,
            defaults,
            self._exported and other._exported,
            context,
            "no location for merged rules")

    def get_pronunciation(self):
        return self.pronunciation if self.pronunciation is not None else self.name

    def copy(self):
        return MergeRule(self.name, self._mapping.copy(), self._extras.values(),
                         self._defaults.copy(), self._exported, self._mcontext, self.location)

    def _display_available_commands(self):
        for spec in self.mapping_actual().keys():
            printer.out(spec)
