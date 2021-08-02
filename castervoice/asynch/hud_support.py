
import sys, subprocess, json
from pathlib import Path
from dragonfly import CompoundRule, MappingRule, get_current_engine

try:  # Style C -- may be imported into Caster, or externally
    BASE_PATH = str(Path(__file__).resolve().parent.parent)
    if BASE_PATH not in sys.path:
        sys.path.append(BASE_PATH)
finally:
    from castervoice.lib import settings

from castervoice.lib import control
from castervoice.lib.rules_collection import get_instance

def start_hud():
    hud = control.nexus().comm.get_com("hud")
    try:
        hud.ping()
    except ConnectionRefusedError:  # pylint: disable=undefined-variable
        subprocess.Popen([settings.SETTINGS["paths"]["PYTHONW"],
                          settings.SETTINGS["paths"]["HUD_PATH"]])


def show_hud():
    hud = control.nexus().comm.get_com("hud")
    hud.show_hud()


def hide_hud():
    hud = control.nexus().comm.get_com("hud")
    hud.hide_hud()


def show_rules():
    """
    Get a list of active grammars loaded into the current engine,
    including active rules and their attributes.  Send the list
    to HUD GUI for display.
    """
    grammars = []
    engine = get_current_engine()
    for grammar in engine.grammars:
        if any([r.active for r in grammar.rules]):
            rules = []
            for rule in grammar.rules:
                if rule.active and not rule.name.startswith('_'):
                    if isinstance(rule, CompoundRule):
                        specs = [rule.spec]
                    elif isinstance(rule, MappingRule):
                        specs = sorted(["{}::{}".format(x, rule._mapping[x]) for x in rule._mapping])
                    else:
                        specs = [rule.element.gstring()]
                    rules.append({
                        "name": rule.name,
                        "exported": rule.exported,
                        "specs": specs
                    })
            grammars.append({"name": grammar.name, "rules": rules})
    grammars.extend(get_instance().serialize())
    hud = control.nexus().comm.get_com("hud")
    hud.show_rules(json.dumps(grammars))


def hide_rules():
    """
    Instruct HUD to hide the frame with the list of rules.
    """
    hud = control.nexus().comm.get_com("hud")
    hud.hide_rules()
