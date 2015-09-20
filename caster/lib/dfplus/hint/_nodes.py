from dragonfly import (Grammar, MappingRule, Function)

from caster.lib import control, settings, utilities, ccr
from caster.lib.dfplus.hint.hintnode import NodeRule
from caster.lib.dfplus.hint.nodes import css


def update(name, value):
    # settings
    try:
        control.nexus().node_rule_active(name, value)
        ccr.set_active()
        ccr.refresh()
    except Exception:
        utilities.simple_log()

_mapping={}
for node in [# register nodes here in order to get them into ccr
                css.getCSSNode()
                 ]:
    if node.spec.lower() in settings.SETTINGS["ccr"]["modes"]:
        utilities.report("CCR naming conflict found between: config"+node.spec+".txt and " \
                         +node.spec+".py, favoring CCR module, ignoring "+node.spec+".py" \
                         +" (Please delete config"+node.spec+".txt) and remove "+node.spec \
                         +" from the settings.json file to change this.")
        continue
    if node.spec in settings.SETTINGS["nodes"] and settings.SETTINGS["nodes"][node.spec]:
        node.active = True
    control.nexus().merger.add_selfmodrule(NodeRule(node, control.nexus().intermediary), node.spec)
    control.nexus().add_node_rule(NodeRule(node, control.nexus().intermediary))
    _mapping["enable "+node.spec]=Function(update, name=node.spec, value=True)
    _mapping["disable "+node.spec]=Function(update, name=node.spec, value=False)
     

if len(_mapping)>0:
    grammar = Grammar("NodeActivation")
    grammar.add_rule(MappingRule(mapping=_mapping, name="NodeActivation"))
    grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
