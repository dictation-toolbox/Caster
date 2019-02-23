import SimpleXMLRPCServer
from SimpleXMLRPCServer import *
import sys
from inspect import getmembers, isfunction

SCRIPTS_PATH = sys.argv[0].split("\\xmlrpc_server.sikuli")[0]
BASE_PATH = sys.argv[0].split("MacroSystem")[0] + "MacroSystem"

modules = []
server = SimpleXMLRPCServer(("127.0.0.1", 8000), allow_none=True)
quit = 0


def ping():
    return 1


def list_functions():
    global modules
    return modules


def terminate():
    global quit
    quit = 1
    return 1


server.register_function(list_functions, "list_functions")
server.register_function(terminate, "terminate")

if SCRIPTS_PATH not in sys.path:
    sys.path.append(SCRIPTS_PATH)
for s in [x[0] for x in os.walk(SCRIPTS_PATH)]:
    if s.endswith(".sikuli") and not s.endswith("xmlrpc_server.sikuli"):
        mdl_name = s.split(".")[0].split("\\")[-1]
        exec ("import " + mdl_name)
        exec ("l = getmembers(" + mdl_name + ", isfunction)")
        for d in l:
            if d[0].startswith("export_"):
                registered_function_name = mdl_name + "_" + d[0].replace("export_", "")
                modules.append(registered_function_name)
                exec ("server.register_function(" + mdl_name + "." + d[0] + ", '" +
                      registered_function_name + "')")

print("Caster Sikuli Bridge\n\nlist of available commands " + str(modules))


# examples
def add(self, x, y):
    return x + y


try:
    while not quit:
        server.handle_request()
except KeyboardInterrupt:
    print('Exiting')
