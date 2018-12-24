from dragonfly import (MappingRule, Config, Section, Item, Mimic, Function, Dictation, Grammar)

from caster.lib import (utilities, settings)
from caster.lib.actions import (Key, Text)
from caster.lib.dfplus.state.short import R

# Playground Grammar - Do not edit - Rebuilds playground.txt

_grammar = Grammar("playground")


class PlayGroundGen(Config):
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
    configuration = PlayGroundGen("sandbox")
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
        rule = generate_rule(settings.SETTINGS["paths"]["PLAYGROUNDTXT_PATH"])
        _grammar.add_rule(rule)
        _grammar.load()
        print('Playground successfully rebuilt')
    except Exception:
        print('Playground failed to rebuild.')
        utilities.simple_log()

grammar = Grammar('playground helper')

# Playground Helper Grammar

def run_remote_debugger():
    utilities.remote_debug("playgroundhelper.py")


class PlaygroundHelpers(MappingRule):
    mapping = {

        "rebuild playground": # Rebuilds grammars for this file.
            R(Function(refresh, rdescript="Playground: Rebuilding PlayGround Grammars...")),
        "run remote debugger": # You will need to set up a remote debugger for your editor.
            R(Function(run_remote_debugger, rdescript="Playground: Initializing debugger...")),
    }

def load():
    global grammar
    grammar.add_rule(PlaygroundHelpers())
    grammar.load()
load()
