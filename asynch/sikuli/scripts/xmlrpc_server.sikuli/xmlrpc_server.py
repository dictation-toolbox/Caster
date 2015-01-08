import SimpleXMLRPCServer
from SimpleXMLRPCServer import *
import sys

available_function_names = []

SCRIPTS_PATH = sys.argv[0].split("\\xmlrpc_server.sikuli")[0]
BASE_PATH = sys.argv[0].split("MacroSystem")[0] + "MacroSystem"

if SCRIPTS_PATH not in sys.path:
    sys.path.append(SCRIPTS_PATH)
for s in [x[0] for x in os.walk(SCRIPTS_PATH)]:
    if s.endswith(".sikuli") and not s.endswith("xmlrpc_server.sikuli"):
        mdl_name = s.split(".")[0].split("\\")[-1]
        exec("import " + mdl_name)
        # at this point, module names still have underscores
        available_function_names.append(mdl_name)
        print "importing " + mdl_name


class MathHandler(SimpleXMLRPCRequestHandler):
    def _dispatch(self, method, params):
        try:
            # We are forcing the 'export_' prefix on methods that are
            # callable through XML-RPC to prevent potential security
            # problems
            func = getattr(self, 'export_' + method)
        except AttributeError:
            raise Exception('method "%s" is not supported' % method)
        else:
            return apply(func, params)

    def log_message(self, format, *args):
        pass
    def export_ping(self):
        return 1
    def export_fclick(self):
        print "attempting to click"
        click("1420309222009.png")
        click("1420309222009.png")
        return 1
    def export_add(self, x, y):
        return x + y

server = SimpleXMLRPCServer(("localhost", 8000), MathHandler)

try:
    print 'Use Control-C to exit'
    server.serve_forever()
except KeyboardInterrupt:
    print 'Exiting'
