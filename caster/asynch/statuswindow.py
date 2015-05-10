from SimpleXMLRPCServer import SimpleXMLRPCServer
from caster.asynch.mouse.grids import TkTransparent
from caster.lib import settings

__author__ = 'dave'

class StatusWindow(TkTransparent):
    def __init__(self):
        ''' do imports '''

    def setup_XMLRPC_server(self):
        self.server_quit = 0
        self.server = SimpleXMLRPCServer(("127.0.0.1", settings.STATUS_LISTENING_PORT), allow_none=True)
        self.server.register_function(self.xmlrpc_kill, "kill")