import inspect
import socket
import sys
from subprocess import Popen
from xmlrpclib import ServerProxy

from dragonfly import Function

from castervoice.lib import settings, utilities, text_window
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.actions import RegisteredAction as R

def close_ccr():
    proxy = ServerProxy('http://localhost:10011')
    proxy.shutdown()

def list_ccr():
    
    Popen(["pythonw", text_window.__file__])
    
    config = utilities.load_toml_file(settings.SETTINGS["paths"]["CCR_CONFIG_PATH"])
    message=''
    already_seen = []
    for modname, module in sys.modules.iteritems():
        if modname.startswith('castervoice'):
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and obj.__module__.startswith('castervoice.lib.ccr'):
                    # print (obj.__name__)
                    # print('---')
                    if not issubclass(obj, MergeRule):
                        continue
                    rule_name = obj.pronunciation
                    if (not rule_name):
                        if name.endswith('Rule'):
                            name = name[:-4]
                        rule_name = name
                    if rule_name in already_seen:
                        continue
                    if rule_name in config["global"] and config["global"][rule_name]:
                        already_seen.append(rule_name)
                        message += '-----\nRule %s\n' % rule_name
                        for k, v in obj.mapping.iteritems():
                            desc = '?'
                            if hasattr(v, 'rdescript'):
                                desc = v.rdescript
                            message += '%s = %s\n' % (k, desc)
    proxy = ServerProxy('http://localhost:10011')
    proxy.message(message)
    

class DocumentationRule(MergeRule):
    
    mapping = {
        "show CCR documentation":
            R(Function(list_ccr), rdescript="Show CCR documentation"),       
        "close CCR documentation":
            R(Function(close_ccr), rdescript="Close CCR documentation"),
    }