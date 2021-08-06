import sys, subprocess, json
import imp

from dragonfly import CompoundRule, MappingRule, get_current_engine

import six
if six.PY2:
    from castervoice.lib.util.pathlib import Path
else:
    from pathlib import Path  # pylint: disable=import-error

try:  # Style C -- may be imported into Caster, or externally
    BASE_PATH = str(Path(__file__).resolve().parent.parent)
    if BASE_PATH not in sys.path:
        sys.path.append(BASE_PATH)
finally:
    from castervoice.lib import settings
    
from castervoice.lib import printer
from castervoice.lib import control
from castervoice.lib.rules_collection import get_instance

def start_hud():
    hud = control.nexus().comm.get_com("hud")
    try:
        hud.ping()
    except Exception:
        subprocess.Popen([settings.SETTINGS["paths"]["PYTHONW"],
                          settings.SETTINGS["paths"]["HUD_PATH"]])


def show_hud():
    hud = control.nexus().comm.get_com("hud")
    hud.show_hud()


def hide_hud():
    hud = control.nexus().comm.get_com("hud")
    hud.hide_hud()


def clear_hud():
    hud = control.nexus().comm.get_com("hud")
    hud.clear_hud()


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


class HudPrintMessageHandler(printer.BaseMessageHandler):
    """
    Hud message handler which prints formatted messages to the gui Hud. 
    Add symbols as the 1st character in strings utilizing printer.out
    
    @ Purple arrow - Bold Text - Important Info
    # Red arrow - Plain text - Caster Info
    $ Blue arrow - Plain text - Commands/Dictation
    """

    def __init__(self):
        super(HudPrintMessageHandler, self).__init__()
        self.hud = control.nexus().comm.get_com("hud")
        self.exception = False
        try:
            imp.find_module('PySide2') # remove imp dropping python 2
            if get_current_engine().name != "text":
                self.hud.ping() # HUD running?
        except Exception as e:
            self.exception = True
            printer.out("Hud not available. \n{}".format(e))

    def handle_message(self, items):
        if self.exception is False:
            # The timeout with the hud can interfere with the dragonfly speech recognition loop.
            # This appears as a stutter in recognition.
            # Exceptions are tracked so this stutter only happens to end user once.
            # Make exception if the hud is not available/python 2/text engine
            try:
                self.hud.send("\n".join([str(m) for m in items]))
            except Exception as e:
                # If an exception, print is managed by SimplePrintMessageHandler
                self.exception = True
                printer.out("Hud not available. \n{}".format(e))
                raise("")
        else:
            raise("")