from dragonfly import MappingRule, Grammar, Config, Section, Item, Dictation, Mimic
from castervoice.lib import settings, utilities
from castervoice.lib.actions import Text, Key

_grammar = Grammar("dev gen")


class ConfigDev(Config):
    def __init__(self, name):
        Config.__init__(self, name)
        self.cmd = Section("Language section")
        self.cmd.map = Item(
            {
                "mimic <text>": Mimic(extra="text"),
            },
            namespace={
                "Key": Key,
                "Text": Text,
            })
        self.cmd.extras = Item([Dictation("text")])
        self.cmd.defaults = Item({})


def generate_rule(path):
    configuration = ConfigDev("dev")
    configuration.load(path)
    return MappingRule(
        exported=True,
        mapping=configuration.cmd.map,
        extras=configuration.cmd.extras,
        defaults=configuration.cmd.defaults)


# Create and load this module's grammar.
def refresh():
    global _grammar
    _grammar.unload()
    while len(_grammar.rules) > 0:
        _grammar.remove_rule(_grammar.rules[0])
    try:
        rule = generate_rule(settings.SETTINGS["paths"]["CONFIGDEBUGTXT_PATH"])
        _grammar.add_rule(rule)
        _grammar.load()
    except Exception:
        utilities.simple_log()
