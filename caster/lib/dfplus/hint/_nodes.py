from dragonfly import (Grammar, MappingRule, Function)

from caster.lib import control, settings, utilities, ccr
from caster.lib.dfplus.hint.hintnode import NodeRule
from caster.lib.dfplus.hint.nodes import css


def update(name, value):
    # settings
    control.nexus().node_rule_active(name, value)
    ccr.set_active()
    ccr.refresh()
    print 4

_mapping={}
for node in [# register nodes here in order to get them into ccr
                 css.getCSSNode()
                 ]:
    if node.text in settings.SETTINGS["ccr"]["modes"]:
        utilities.report("CCR naming conflict found between: config"+node.text+".txt and " \
                         +node.text+".py, favoring CCR module, ignoring "+node.text+".py" \
                         +" (Please delete config"+node.text+".txt) and remove "+node.text \
                         +" from the settings.json file to change this.")
        continue
    control.nexus().add_node_rule(NodeRule(node, None, control.nexus().intermediary, False))
    _mapping["enable "+node.text]=Function(update, name=node.text, value=True)
    _mapping["disable "+node.text]=Function(update, name=node.text, value=False)
    # settings

if len(_mapping)>0:
    grammar = Grammar("NodeActivation")
    grammar.add_rule(MappingRule(mapping=_mapping, name="NodeActivation"))
    grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
