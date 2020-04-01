import os
import sys

if sys.version_info[0] < 3:
    from SimpleXMLRPCServer import SimpleXMLRPCServer   # pylint: disable=import-error
else:
    from xmlrpc.server import SimpleXMLRPCServer  # pylint: disable=no-name-in-module
    
from inspect import getmembers, isfunction

modules = []
server = SimpleXMLRPCServer(("127.0.0.1", 8000), logRequests=False, allow_none=True)
quit = 0

SCRIPTS_PATH = sys.argv[1]

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

print("\nCaster Sikuli Bridge [started]\n")
print("  Loading commands from: {} ...".format(SCRIPTS_PATH))

if SCRIPTS_PATH not in sys.path:
    sys.path.append(SCRIPTS_PATH)
for s in [x[0] for x in os.walk(SCRIPTS_PATH)]:
    if s.endswith(".sikuli") and not s.endswith("xmlrpc_server.sikuli"):
        mdl_name = s.split(".sikuli")[0].split("\\")[-1]
        exec("import " + mdl_name)
        exec("l = getmembers(" + mdl_name + ", isfunction)")
        for d in l: # pylint: disable=undefined-variable
            if d[0].startswith("export_"):
                registered_function_name = mdl_name + "_" + d[0].replace("export_", "")
                modules.append(registered_function_name)
                exec("server.register_function(" + mdl_name + "." + d[0] + ", '" +
                      registered_function_name + "')")

print("  Loaded. Available commands:\n")
for fn_name in modules:
    print("    {}".format(str(fn_name).replace("_", " ")))
print("")

# examples
def add(self, x, y):
    return x + y

try:
    while not quit:
        server.handle_request()
except KeyboardInterrupt:
    print('Exiting')
